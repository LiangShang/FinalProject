import sys
from configuration import memories, cpus
from learning.exe_command import run_command_with_docker, run_command
from learning.exe_time import parse_time
from table import PerformanceTable

__author__ = 'Sherlock'

if __name__ == '__main__':

    table = PerformanceTable()

    command = sys.argv[1]
    image = "stackbrew/hipache"

    for memory in memories:
        for cpu in cpus:
            a, b = run_command_with_docker(" python exe_time.py "+command, image, cpu, memory)
            if a != 0:
                print "command '"+command+"' is wrong"
                print b
                exit()
            total_time = b
            table.add(time=total_time, cpu=cpu, memory=memory)

    table.pareto()
    table.generate("Performance\ Table of "+command)
