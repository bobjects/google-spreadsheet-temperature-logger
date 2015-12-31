import re
import platform
from configurationFile import ConfigurationFile
from oneWireDeviceTemperatureReading import OneWireDeviceTemperatureReading
from raspberryPiCPUTemperatureReading import RaspberryPiCPUTemperatureReading
from linuxBoxCPUTemperatureReading import LinuxBoxCPUTemperatureReading
from osxCPUTemperatureReading import OSXCPUTemperatureReading
from unknownPlatformCPUTemperatureReading import UnknownPlatformCPUTemperatureReading


class TemperatureReadingFactory(object):
    def create(self):
        if self.useOneWireDevice:
            return OneWireDeviceTemperatureReading(self.useFahrenheit)
        if self.isRaspberryPi:
            return RaspberryPiCPUTemperatureReading(self.useFahrenheit)
        elif self.isOSX:
            return OSXCPUTemperatureReading(self.useFahrenheit)
        elif self.isLinuxBox:
            return LinuxBoxCPUTemperatureReading(self.useFahrenheit)
        else:
            return UnknownPlatformCPUTemperatureReading(self.useFahrenheit)

    @property
    def isRaspberryPi(self):
        try:
            with open("/proc/cpuinfo", "r") as procFile:
                fileContents = procFile.read()
                regex = re.compile(".*BCM2708.*", re.DOTALL)
                regex2 = re.compile(".*BCM2709.*", re.DOTALL)
                return (regex.match(fileContents) is not None) or (regex2.match(fileContents) is not None)
        except:
            return False

    @property
    def isOSX(self):
        return platform.system() == "Darwin"

    @property
    def isLinuxBox(self):
        return (not self.isRaspberryPi) and platform.system() == "Linux"

    @property
    def useOneWireDevice(self):
        return ConfigurationFile.instance().useOneWireDevice

    @property
    def useFahrenheit(self):
        return ConfigurationFile.instance().useFahrenheit
