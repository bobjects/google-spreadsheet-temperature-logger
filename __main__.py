import time
from temperatureReadingFactory import TemperatureReadingFactory
from configurationFile import ConfigurationFile


def main():
    while True:
        temperature = TemperatureReadingFactory().create().acquire()
        # TODO: need to implement the google spreadsheet part.  For now, just print the temperature.
        print temperature
        time.sleep(ConfigurationFile.instance().updatePeriodInSeconds)


if __name__ == "__main__":
    main()
