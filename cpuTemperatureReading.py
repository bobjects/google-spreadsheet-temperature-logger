from temperatureReading import TemperatureReading


class CPUTemperatureReading(TemperatureReading):
    def acquireCelsius(self):
        return self.parseRawString(self.procFileContents)

    @property
    def procFileName(self):
        return ""

    @property
    def procFileContents(self):
        try:
            with open(self.procFileName, "r") as procFile:
                return procFile.read()
        except:
            return ""

    def parseRawString(self, aString):
        # by default, we assume that the proc file reports the temp as thousandths of a degree
        # celsius, with only one line in the file.  Override as needed.
        return float(aString) / 1000.0
