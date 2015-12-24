import time
from temperatureReadingFactory import TemperatureReadingFactory
from configurationFile import ConfigurationFile
from googleSpreadsheetWorksheet import GoogleSpreadsheetWorksheet


def main():
    while True:
        temperature = TemperatureReadingFactory().create().acquire()
        GoogleSpreadsheetWorksheet().logTemperatureReading(temperature)
        time.sleep(ConfigurationFile.instance().updatePeriodInSeconds)


if __name__ == "__main__":
    main()
