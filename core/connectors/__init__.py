from core.connectors.local import LocalConnector
from core.connectors.home_assistant import HomeAssistantConnector
 
from enum import Enum

class ConnectorTypes(Enum):
    Unknown = 0
    HomeAssistant = 1

def createConnector(kind:str, name:str, config:dict):
    if kind.casefold() == ConnectorTypes.HomeAssistant.name.casefold():
        assert len(config.get("host","")) > 0, "Invalid host in connector " + name
        assert len(config.get("accessToken")) > 0, "Invalid access_token in connector config " + name

        con = HomeAssistantConnector(config["host"], config.get("port", 8123), config["accessToken"], config.get("useSSL", True))
        con.connect()

        return con