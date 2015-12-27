import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import datetime
from configurationFile import ConfigurationFile
import socket


class GoogleSpreadsheetWorksheet(object):
    def __init__(self):
        self._spreadsheet = None
        self._worksheet = None

    def logTemperatureReading(self, temperatureNumber):
        if self.worksheet is not None:
            print temperatureNumber
            self.worksheet.update_cells(self.allCellsWithNewTemperatureReading(temperatureNumber))
        else:
            print str(temperatureNumber) + " - Could not OAuth2 authenticate with Google, or could not find spreadsheet with title " + self.googleSpreadsheetTitle
        pass

    def allCellsWithNewTemperatureReading(self, temperatureNumber):
        return self.titleCells + self.dateColumnCells + self.temperatureReadingColumnCellsWithNewTemperatureReading(temperatureNumber)

    @property
    def titleCells(self):
        dateColumnTitleCell = self.worksheet.acell(self.googleSpreadsheetDateColumnLetter + "1")
        readingColumnTitleCell = self.worksheet.acell(self.googleSpreadsheetTemperatureReadingColumnLetter + "1")
        dateColumnTitleCell.value = "Date"
        readingColumnTitleCell.value = self.hostName
        return [ dateColumnTitleCell, readingColumnTitleCell ]

    @property
    def dateColumnCells(self):
        cells = self.worksheet.range(self.googleSpreadsheetDateColumnLetter + "2:" + self.googleSpreadsheetTemperatureReadingColumnLetter + str(self.googleSpreadsheetMaximumReadings + 2))
        # TODO: fill in the dates.
        return cells

    def temperatureReadingColumnCellsWithNewTemperatureReading(self, temperatureNumber):
        cells = self.worksheet.range(self.googleSpreadsheetTemperatureReadingColumnLetter + "2:" + self.googleSpreadsheetTemperatureReadingColumnLetter + str(self.googleSpreadsheetMaximumReadings + 2))
        # TODO: fill in the readings.
        return cells

    @property
    def googleSpreadsheetTitle(self):
        return ConfigurationFile.instance().googleSpreadsheetTitle

    @property
    def hostName(self):
        return socket.gethostname()

    @property
    def googleOauthCredentialsJsonFileName(self):
        return ConfigurationFile.instance().googleOauthCredentialsJsonFileName

    @property
    def googleSpreadsheetDateColumnLetter(self):
        return ConfigurationFile.instance().googleSpreadsheetDateColumnLetter

    @property
    def googleSpreadsheetTemperatureReadingColumnLetter(self):
        return ConfigurationFile.instance().googleSpreadsheetTemperatureReadingColumnLetter

    @property
    def googleSpreadsheetMaximumReadings(self):
        return ConfigurationFile.instance().googleSpreadsheetMaximumReadings

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
                json_key = None
                with open(self.googleOauthCredentialsJsonFileName, "r") as jsonFile:
                    json_key = json.load(jsonFile)
                scope = ['https://spreadsheets.google.com/feeds']
                credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
                client = gspread.authorize(credentials)
                self._spreadsheet = client.open(self.googleSpreadsheetTitle)
            except:
                return None
        return self._spreadsheet
