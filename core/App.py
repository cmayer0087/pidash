import logging
import os
import yaml
import locale

from PyQt5.QtGui import QGuiApplication, QWindow
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl

from .Connectors import LocalConnector, createConnector

class App(QGuiApplication):

    mainWindow: QWindow
    basePath: str

    def __init__(self, args):
        super().__init__(args)
        self.basePath = os.path.dirname(os.path.dirname(__file__)) + os.sep

        # Use system defined locale
        locale.setlocale(locale.LC_ALL, '')

        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"

        logging.basicConfig(level=logging.INFO)
        logging.info("Starting PiDash")

    def load(self):
        self._loadConfig()

        if "logging" in self.config:
            logging.getLogger().setLevel(self.config["logging"].get("level","INFO"))

        self._initMainWindow()

    def _initMainWindow(self):
        self.qmlEngine = QQmlApplicationEngine()

        self.datasources = self._createDataSources()
        self.qmlEngine.rootContext().setContextProperty("cons", self.datasources)

        if "dashboard" in self.config:
            for key in self.config["dashboard"]:
                self.qmlEngine.rootContext().setContextProperty(key, self.config["dashboard"][key])

        dashQmlFile = self._resolveConfigFile("dashboard.qml", "dashboard.example.qml")
        self.qmlEngine.load(QUrl.fromLocalFile(dashQmlFile))

        self.mainWindow = self.qmlEngine.rootObjects()[0]

    def _loadConfig(self):
        configFile = self._resolveConfigFile("config.yaml", "config.example.yaml")

        with open(configFile, "r") as stream:
            self.config = yaml.safe_load(stream)

    def _resolveConfigFile(self, relPath: str, altRelPath: str = ""):
        path = self.basePath + relPath
        if os.path.exists(path): 
            return path

        altPath = self.basePath + altRelPath
        if len(altRelPath) > 0 and os.path.exists(altPath):
            return altPath

        return ""

    def _createDataSources(self):
        data = {}
        
        data["local"] = LocalConnector()
        data["local"].startUpdateLoop()

        for conCfg in self.config.get("connectors",[]):
            kind = conCfg.get("type", "")
            name = conCfg.get("name", "")

            assert len(kind) > 0, "No type in connector configuration"
            assert len(name) > 0, "No name in connector configuration"

            con = createConnector(kind, name, conCfg)
            data[name] = con
            assert con != None, f"invalid connector type '{kind}'"
        
        return data