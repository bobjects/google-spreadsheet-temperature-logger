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
            try:
                self.resizeWorksheetIfNeeded()
            except:
                print "An error occurred while resizing the worksheet.  The worksheet was not updated with this temperature reading."
            try:
                cells = self.allCellsWithNewTemperatureReading(temperatureNumber)
                # TODO: update_cells() takes a long time.  Is there a faster way?  I think this is supposed to BE the faster way.
                self.worksheet.update_cells(cells)
            except:
                print "An error occurred while updating the worksheet cells.  The worksheet was not updated with this temperature reading."
        else:
            print str(temperatureNumber) + " - Could not OAuth2 authenticate with Google, or could not find spreadsheet with title " + self.googleSpreadsheetTitle

    def resizeWorksheetIfNeeded(self):
        if self.worksheet.row_count < (self.googleSpreadsheetMaximumReadings + 2):
            self.worksheet.resize(self.googleSpreadsheetMaximumReadings + 2)

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
        cells = self.worksheet.range(self.googleSpreadsheetDateColumnLetter + "2:" + self.googleSpreadsheetDateColumnLetter + str(self.googleSpreadsheetMaximumReadings + 2))
        for i in reversed(range(1, self.googleSpreadsheetMaximumReadings)):
            cells[i].value = cells[i - 1].value
        cells[0].value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cells

    def temperatureReadingColumnCellsWithNewTemperatureReading(self, temperatureNumber):
        cells = self.worksheet.range(self.googleSpreadsheetTemperatureReadingColumnLetter + "2:" + self.googleSpreadsheetTemperatureReadingColumnLetter + str(self.googleSpreadsheetMaximumReadings + 2))
        for i in reversed(range(1, self.googleSpreadsheetMaximumReadings)):
            cells[i].value = cells[i - 1].value
        cells[0].value = temperatureNumber
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
