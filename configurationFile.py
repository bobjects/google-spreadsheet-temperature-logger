import ConfigParser


class ConfigurationFile(object):
    Instance = None

    @classmethod
    def instance(cls):
        if cls.Instance is None:  # IGNORE:E0203
            cls.Instance = cls()  # IGNORE:W0201
        return cls.Instance

    @classmethod
    def clear(cls):
        cls.Instance = None

    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser({'useFahrenheit': 'false',
                                                     'useOneWireDevice': 'false'})
        self.read()
        self._useFahrenheit = None
        self._useOneWireDevice = None
        self._updatePeriodInSeconds = None
        self._googleSpreadsheetTitle = None
        self._googleOauthCredentialsJsonFileName = None

    @property
    def filePath(self):
        return "./google-spreadsheet-temperature-logger.conf"

    def read(self):
        self.parser.read(self.filePath)

    def getStringFromParser(self, section="google-spreadsheet-temperature-logger", option="", default=None):
        answer = default
        try:
            answer = self.parser.get(section, option)
        except ConfigParser.NoOptionError:
            print "got a NoOptionError exception"
        except ConfigParser.NoSectionError:
            print "got a NoSectionError exception"
        return answer

    def getBooleanFromParser(self, section="google-spreadsheet-temperature-logger", option="", default=None):
        answer = default
        try:
            answer = self.parser.getboolean(section, option)
        except ConfigParser.NoOptionError:
            print "got a NoOptionError exception"
        except ConfigParser.NoSectionError:
            print "got a NoSectionError exception"
        return answer

    def getIntFromParser(self, section="google-spreadsheet-temperature-logger", option="", default=None):
        answer = default
        try:
            answer = self.parser.getint(section, option)
        except ConfigParser.NoOptionError:
            print "got a NoOptionError exception"
        except ConfigParser.NoSectionError:
            print "got a NoSectionError exception"
        return answer

    @property
    def useFahrenheit(self):
        if self._useFahrenheit is None:
            self._useFahrenheit = self.getBooleanFromParser(option="useFahrenheit", default=False)
        return self._useFahrenheit

    @property
    def useOneWireDevice(self):
        if self._useOneWireDevice is None:
            self._useOneWireDevice = self.getBooleanFromParser(option="useOneWireDevice", default=False)
        return self._useOneWireDevice

    @property
    def updatePeriodInSeconds(self):
        if self._updatePeriodInSeconds is None:
            self._updatePeriodInSeconds = self.getIntFromParser(option="updatePeriodInSeconds", default=10)
        return self._updatePeriodInSeconds

    @property
    def googleSpreadsheetTitle(self):
        if self._googleSpreadsheetTitle is None:
            self._googleSpreadsheetTitle = self.getStringFromParser(option="googleSpreadsheetTitle", default="Temperature Log")
        return self._googleSpreadsheetTitle

    @property
    def googleOauthCredentialsJsonFileName(self):
        if self._googleOauthCredentialsJsonFileName is None:
            self._googleOauthCredentialsJsonFileName = self.getStringFromParser(option="googleOauthCredentialsJsonFileName", default="google-oauth-credentials.json")
        return self._googleOauthCredentialsJsonFileName

