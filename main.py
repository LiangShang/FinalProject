import sys
from learning.lxc_config import memories, cpus
from learning.exe_command import run_command_with_docker, run_command
from learning.exe_time import parse_time
from learning.table import PerformanceTable

__author__ = 'Sherlock'

if __name__ == '__main__':

    table = PerformanceTable()

    if len(sys.argv) < 2:
        print "Usage: python main.py <command>"
        exit()

    command = sys.argv[1]
    image = "stackbrew/hipache"

    f = open("script", "w")
    f.write("time "+command)
    f.close()

    for memory in memories:
        for cpu in cpus:
            print "begin to calculate execution time with config: "+\
                  str(cpu)+" cpu(s) and "+str(memory)+"k memory"
            a, b = run_command_with_docker("bash /Final/script", image, cpu, memory)
            #a, b = run_command(" time ls")
            if a != 0:
                print "command '"+command+"' is wrong"
                print b
                exit()
            print b
            total_time = parse_time(b)
            print "finish calculation, write to table"
            table.add(time=total_time, cpu=cpu, memory=memory)

    table.pareto()
    table.generate("PerformanceTable of "+command)
