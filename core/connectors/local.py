import time
import psutil
import socket
from threading import Thread
from enum import Enum

from PyQt5.QtCore import QDateTime, QObject, pyqtSignal, pyqtProperty

class LocalConnector(QObject):

    dateTimeChanged = pyqtSignal(QDateTime)
    cpuUsageChanged = pyqtSignal(int)
    memUsageChanged = pyqtSignal(int)
    memTotalChanged = pyqtSignal(int)
    memFreeChanged = pyqtSignal(int)
    hostnameChanged = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

        self._dateTime = QDateTime()
        self._cpuUsage = 0
        self._memUsage = 0
        self._memTotal = 0
        self._memFree = 0
        self._hostname = ""

    def startUpdateLoop(self):
        self.updateThread = Thread(target=self._updateLoop, daemon=True)
        self.updateThread.start()

    def _updateLoop(self):
        while True:
            self.dateTime = QDateTime.currentDateTime()
            self.cpuUsage = psutil.cpu_percent()
            self.hostname = socket.gethostname()

            memInfo = psutil.virtual_memory()
            self.memUsage = memInfo.percent
            self.memTotal = memInfo.total
            self.memFree = memInfo.available
            
            time.sleep(0.5)

    @pyqtProperty(QDateTime, notify=dateTimeChanged)
    def dateTime(self):
        return self._dateTime

    @dateTime.setter
    def dateTime(self, value):
        self._dateTime = value
        self.dateTimeChanged.emit(value)

    @pyqtProperty(int, notify=cpuUsageChanged)
    def cpuUsage(self):
        return self._cpuUsage

    @cpuUsage.setter
    def cpuUsage(self, value):
        if self._cpuUsage == value: return
        self._cpuUsage = value
        self.cpuUsageChanged.emit(value)

    @pyqtProperty(int, notify=memUsageChanged)
    def memUsage(self):
        return self._memUsage

    @memUsage.setter
    def memUsage(self, value):
        if self._memUsage == value: return
        self._memUsage = value
        self.memUsageChanged.emit(value)

    @pyqtProperty(int, notify=memTotalChanged)
    def memTotal(self):
        return self._memTotal

    @memTotal.setter
    def memTotal(self, value):
        if self._memTotal == value: return
        self._memTotal = value
        self.memTotalChanged.emit(value)

    @pyqtProperty(int, notify=memFreeChanged)
    def memFree(self):
        return self._memFree

    @memFree.setter
    def memFree(self, value):
        if self._memFree == value: return
        self._memFree = value
        self.memFreeChanged.emit(value)

    @pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        if self._hostname == value: return
        self._hostname = value
        self.hostnameChanged.emit(value)
