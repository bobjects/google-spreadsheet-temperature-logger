from cpuTemperatureReading import CPUTemperatureReading


class UnknownPlatformCPUTemperatureReading(CPUTemperatureReading):
    def acquireCelsius(self):
        return 0


