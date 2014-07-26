import argparse
import os
from performance_table import PerformanceTable
from cost_table import CostTable

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--time', action='store', dest='max_time',
                    help='The maximum time expected to run the application, united by second')

parser.add_argument('-m', '--money', action='store', dest="max_money",
                    help='The maximum money expected to run the application')

parser.add_argument('application', help='the application name')

args = parser.parse_args()

print args.application


# Find the configuration according to the money
cost_table = CostTable("cost_table")
configs = [(cpu, memory)
           for cpu in cost_table.cpu_range
           for memory in cost_table.memory_range]
configs_sorted = False

if args.max_money:
    max_money = float(args.max_money)
    configs = cost_table.get_configs(max_money)
    configs_sorted = True
    if not configs:
        print "Cannot run such application with the money: " + args.max_money
        exit()

# Find the configuration according to the time
if args.max_time:

    max_time = float(args.max_time)

    file_name = args.application
    if file_name[0:2] == "./":
        file_name = "../learning/performance of " + file_name[2:]
    if not os.path.isfile(file_name):
        print "please use learning.sh in directory learning first"
        exit()

    performance_table = PerformanceTable(file_name)
    configs = performance_table.get_configs(configs, max_time, configs_sorted)

    if not configs:
        print "Cannot run such application with the money" \
              + args.max_money + " and the time: " + args.max_time
        exit()

    print "find config: " + str(configs)