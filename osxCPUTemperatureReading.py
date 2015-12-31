import subprocess
import re
from cpuTemperatureReading import CPUTemperatureReading

class OSXCPUTemperatureReading(CPUTemperatureReading):
    def acquireCelsius(self):
        # We just use the istats command line tool for now:  https://github.com/Chris911/iStats
        try:
            stdout = subprocess.check_output(["istats"])
        except OSError:
            print "Could not execute istats.  Is it installed?"
            return 0
        regex = re.compile(".*CPU temp: ([\d\.]*).*", re.DOTALL)
        match = regex.match(stdout)
        if match is not None:
            return float(match.group(1))
        else:
            print "istats did not report a CPU temperature."
        return 0


