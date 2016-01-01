import subprocess
import os
import glob
import re
from temperatureReading import TemperatureReading


class OneWireDeviceTemperatureReading(TemperatureReading):
    def acquireCelsius(self):
        if not os.path.isdir(self.deviceBaseDirectory()):
            os.system("sudo modprobe w1-gpio")
            os.system("sudo modprobe w1-therm")
        if self.deviceFileName() is not None:
            with open(self.deviceFileName(), 'r') as deviceFile:
                deviceFileContents = deviceFile.read()
                regex = re.compile(".*t=([\d]*).*", re.DOTALL)
                match = regex.match(deviceFileContents)
                if match is not None:
                    return float(match.group(1)) / 1000.0
                else:
                    print "The one-wire device did not report a temperature."
                    return 0
        else:
            print "No one-wire devices found."
            return 0

    def deviceBaseDirectory(self):
        return "/sys/bus/w1/devices"

    def deviceDirectory(self):
        try:
            return glob.glob(self.deviceBaseDirectory() + '/28*')[0]
        except:
            return None

    def deviceFileName(self):
        if self.deviceDirectory() is not None:
            return self.deviceDirectory() + "/w1_slave"
        else:
            return None
