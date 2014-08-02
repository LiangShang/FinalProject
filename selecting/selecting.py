#!/usr/bin/python
import argparse
import os
from performance_table import PerformanceTable
from cost_table import CostTable
from time_cost_mapping import TimeCostMapping

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--time', action='store', dest='max_time',
                    help='The maximum time expected to run the application, united by second')

parser.add_argument('-m', '--money', action='store', dest="max_money",
                    help='The maximum money expected to run the application')

parser.add_argument('--draw', dest="draw",
                    help='Draw the pareto frontier, python-matplotlib required')

parser.add_argument('--size', action='store', dest="size", required=True,
                    help='The size of the application')

parser.add_argument('application', help='the application name')

args = parser.parse_args()

print args.application + args.size


# Find the configuration according to the money
cost_table = CostTable("cost_table")
configs = [(cpu, memory)
           for cpu in cost_table.cpu_range
           for memory in cost_table.memory_range]

file_name = args.application  # args.application is 'matrix_mul'
application = './'+file_name  # application is './matrix_mul'
file_name = "../learning/performance of " + file_name + " " + args.size
if not os.path.isfile(file_name):
    print "please use learning.sh in directory learning first"
    print "now try to run the learning module"
    print "running the command", "cd ../learning; bash learning.sh " + args.application + " " + args.size

    #import commands
    #commands.getstatusoutput("cd ../learning; bash learning.sh " + args.application)
    import os
    os.system("cd ../learning; bash learning.sh " + application + " " + args.size)

performance_table = PerformanceTable(file_name)

mapping = TimeCostMapping(cost_table=cost_table,
                          performance_table=performance_table)

mapping.update_csv(args.application+'.csv', int(args.size))

max_money = float(args.max_money) if args.max_money else float('inf')
max_time = float(args.max_time) if args.max_time else float('inf')

result = mapping.get_config(max_money, max_time)

print result

if args.draw:
    mapping.draw()


