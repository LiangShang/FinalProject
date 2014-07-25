import sys
from exe_time import parse_m_s

__author__ = 'Sherlock'
import table

if __name__ == "__main__":

    performance_table = table.PerformanceTable()
    f = open("statistics", "r")

    for line in f:
        profile = line.split(" ")
        cpu = profile[0]
        memory = profile[1]
        sys_time_str = profile[3]
        user_time_str = profile[5]
        time = parse_m_s(sys_time_str) + parse_m_s(user_time_str)
        previous_time = performance_table.get(cpu, memory)
        if previous_time:
            performance_table.add(previous_time+time, cpu, memory)
        else:
            performance_table.add(time, cpu, memory)

    performance_table.pareto()
    command_names = sys.argv
    command_names[1] = command_names[1].replace('./', '')
    command_name = ""
    for i in range(1, len(command_names)):
        command_name += command_names[i]+" "
    performance_table.generate("performance of "+command_name)