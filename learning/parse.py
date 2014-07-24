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
        total_time = parse_m_s(sys_time_str) + parse_m_s(user_time_str)
        performance_table.add(total_time, cpu, memory)

    performance_table.generate("result")