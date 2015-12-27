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
            self.resizeWorksheetIfNeeded()
            self.worksheet.update_cells(self.allCellsWithNewTemperatureReading(temperatureNumber))
        else:
            print str(temperatureNumber) + " - Could not OAuth2 authenticate with Google, or could not find spreadsheet with title " + self.googleSpreadsheetTitle
        pass

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
        # TODO:  This technique of retrieving all cells and moving the values around is way too slow and bandwidth intensive for a realistic
        # number of readings.  We need to do something else.  But what?  insert_row() doesn't sound good, because there may be other hosts that
        # are simultaneously, but asynchronously to us, updating the same worksheet.  There doesn't seem to be an insert_cell().
        cells = self.worksheet.range(self.googleSpreadsheetDateColumnLetter + "2:" + self.googleSpreadsheetDateColumnLetter + str(self.googleSpreadsheetMaximumReadings + 2))
        for i in reversed(range(1, self.googleSpreadsheetMaximumReadings)):
            cells[i].value = cells[i - 1].value
        cells[0].value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cells

    def temperatureReadingColumnCellsWithNewTemperatureReading(self, temperatureNumber):
        # TODO:  see TODO note for dateColumnCells().
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
