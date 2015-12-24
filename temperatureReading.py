class TemperatureReading(object):
    def __init__(self, useFahrenheit=False):
        self.useFahrenheit = useFahrenheit

    def acquire(self):
        if self.useFahrenheit:
            return self.acquireFahrenheit()
        else:
            return self.acquireCelsius()

    def acquireCelsius(self):
        return 0

    def acquireFahrenheit(self):
        return self.acquireCelsius() * 9.0 / 5.0 + 32.0
