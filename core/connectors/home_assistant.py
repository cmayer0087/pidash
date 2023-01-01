import logging
import time
import websocket
import ssl
import simplejson as json
from threading import Thread

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

class HomeAssistantConnector(QObject):

    entitiesChanged = pyqtSignal(dict)

    def __init__(self, host, port, accessToken, useSSL):
        QObject.__init__(self)
        self._host = host
        self._port = port
        self._accessToken = accessToken
        self._useSSL = useSSL
        self._logger = logging.getLogger("hass")
        self._msgId = 0
        self._requestCurrentStateMsgId = 0
        self._autoReconnectIntervalInSecs = 5

        self._entities = {}

    def connect(self):
        proto = "wss" if self._useSSL else "ws"
        url = f"{proto}://{self._host}:{self._port}/api/websocket"
        self._client = websocket.WebSocketApp(url, on_open=self._onOpen, on_message=self._onMessage)
        self._workerThread = Thread(target=self._keep_connected_forever, args=(True,), daemon=True)
        self._workerThread.start()

    def _keep_connected_forever(self, ignoreBadSSLCerts):
        while True:
            try:
                sslopt = {"cert_reqs":ssl.CERT_NONE} if ignoreBadSSLCerts else None
                self._client.run_forever(sslopt=sslopt)
                self._logger.info(f"Connection closed (reconnect in {self._autoReconnectIntervalInSecs} seconds)")
            except Exception as ex:
                self._logger.Info(f"Connection closed (reconnect in {self._autoReconnectIntervalInSecs} seconds): " + str(ex))

            time.sleep(self._autoReconnectIntervalInSecs)

    def _onOpen(self, ws):
        self._logger.info("Connected to homeassistant")

    def _onMessage(self, ws, message):
        try:
            self._logger.debug("Message recieved: " + str(message))
            data = json.loads(message)

            msgType = data.get("type", "")
            if msgType == "auth_required": self._sendAuth()
            if msgType == "auth_ok": self._onAuthOk()

            if msgType == "event": 
                if data["event"]["event_type"] == "state_changed": self._onStateChangedEvent(data)

            if msgType == "result":
                if data["id"] == self._requestCurrentStateMsgId: self._onCurrentEntityStatesResult(data)

        except Exception as ex:
            self._logger.exception("error while processing message: " + str(ex))

    def _sendAuth(self):
        self._logger.info("Sending Authentication")
        self._client.send(json.dumps({"type": "auth", "access_token": self._accessToken}))

    def _onAuthOk(self):
        self._subscribeToEvents()
        self._requestCurrentEntityStates()

    def _onStateChangedEvent(self, data):
        newState = data["event"]["data"]["new_state"]
        self._saveEntityState(newState)

    def _onCurrentEntityStatesResult(self, data):
        for state in data["result"]:
            self._saveEntityState(state)

    def _saveEntityState(self, newState):
        if newState["entity_id"] not in self._entities:
            self._entities[newState["entity_id"]] = HomeAssistantEntityState()
            self._entities[newState["entity_id"]].moveToThread(QGuiApplication.instance().thread())
            self.entitiesChanged.emit(self._entities)

        self._entities[newState["entity_id"]].state = newState["state"]
        self._entities[newState["entity_id"]].attrs = newState["attributes"]

    def _subscribeToEvents(self):
        self._send({
            "id": self._getNextMsgId(),
            "type": "subscribe_events", 
            "event_type": "state_changed"
        })

    def _requestCurrentEntityStates(self):
        self._requestCurrentStateMsgId = self._getNextMsgId()
        self._send({
            "id": self._requestCurrentStateMsgId,
            "type": "get_states"
        })

    @pyqtProperty('QVariantMap', notify=entitiesChanged)
    def entities(self):
        return self._entities

    @entities.setter
    def entities(self, value):
        self._entities = value

    def _send(self, data):
        if type(data) is not str:
            data = json.dumps(data)

        self._client.send(data)
        self._logger.debug("Message sent: " + data)

    def callService(self, domain, service, data):
        self._send({
            "id": self._getNextMsgId(),
            "type": "call_service",
            "domain": domain,
            "service": service,
            "service_data": data
        })

    def publishMQTT(self, topic, payload):
        data = { "topic": topic, "payload": json.dumps(payload)}
        self.callService("mqtt","publish", data)

    def _getNextMsgId(self):
        self._msgId += 1
        return self._msgId

    @pyqtSlot(str, str)
    def setClimatePresetMode(self, entityId, presetMode):
        data = { "entity_id" : entityId, "preset_mode": presetMode}
        self.callService("climate", "set_preset_mode", data)

    @pyqtSlot(str, str)
    def setHumidifierPresetMode(self, entityId, presetMode):
        data = { "entity_id": entityId, "mode": presetMode }
        self.callService("humidifier", "set_mode", data)

    @pyqtSlot(str)
    def startVacuum(self, entityId):
        data = { "entity_id": entityId }
        self.callService("vacuum", "start", data)

    @pyqtSlot(str)
    def stopVacuum(self, entityId):
        data = { "entity_id": entityId }
        self.callService("vacuum", "stop", data)

    @pyqtSlot(str, list, int)
    def startVaccumSegmentsClean(self, topicPrefix, segmentIds, iterations):
        payload = {
            "segment_ids": segmentIds,
            "iteration": iterations,
            "customOrder": True
        }
        self.publishMQTT(topicPrefix + "/MapSegmentationCapability/clean/set", payload)

class HomeAssistantEntityState(QObject):

    stateChanged = pyqtSignal(str)
    attrsChanged = pyqtSignal(dict)

    def __init__(self):
        QObject.__init__(self)
        self._attrs = {}
        self._state = None

    @pyqtProperty("QVariantMap", notify=attrsChanged)
    def attrs(self):
        return self._attrs

    @attrs.setter
    def attrs(self, value):
        self._attrs = value
        self.attrsChanged.emit(value)

    @pyqtProperty(str, notify=stateChanged)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state == value: return
        self._state = value
        self.stateChanged.emit(value)
