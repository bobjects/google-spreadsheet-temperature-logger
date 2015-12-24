from cpuTemperatureReading import CPUTemperatureReading


class RaspberryPiCPUTemperatureReading(CPUTemperatureReading):
    @property
    def procFileName(self):
        return "/sys/class/thermal/thermal_zone0/temp"

