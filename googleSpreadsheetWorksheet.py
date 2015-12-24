import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import datetime
from configurationFile import ConfigurationFile


class GoogleSpreadsheetWorksheet(object):
    def __init__(self):
        self._spreadsheet = None
        self._worksheet = None

    def logTemperatureReading(self, temperatureNumber):
        if self.worksheet is not None:
            # TODO: Need to actually write out the reading.  For now, just print it.
            print temperatureNumber
        else:
            print str(temperatureNumber) + " - Could not OAuth2 authenticate with Google, or could not find spreadsheet with title " + self.spreadsheetTitle
        pass

    @property
    def spreadsheetTitle(self):
        return ConfigurationFile.instance().googleSpreadsheetTitle

    @property
    def googleOauthCredentialsJsonFileName(self):
        return ConfigurationFile.instance().googleOauthCredentialsJsonFileName

    @property
    def worksheet(self):
        if self._worksheet is None:
            try:
                self._worksheet = self.spreadsheet.get_worksheet(0)
            except:
                return None
        return self._worksheet

    @property
    def spreadsheet(self):
        if self._spreadsheet is None:
            try:
                json_key = json.load(open(self.googleOauthCredentialsJsonFileName))
                scope = ['https://spreadsheets.google.com/feeds']
                credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
                # TODO:  commented out for now, until we have real JSON-resident credentials.
                # client = gspread.authorize(credentials)
                # self._spreadsheet = client.open(self.spreadsheetTitle)
            except:
                return None
        return self._spreadsheet
