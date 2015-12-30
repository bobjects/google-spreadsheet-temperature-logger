from cpuTemperatureReading import CPUTemperatureReading


class OSXCPUTemperatureReading(CPUTemperatureReading):
    def acquireCelsius(self):
        # TODO
        # We will just use the istat command line tool:  https://github.com/Chris911/iStats
        return 0


