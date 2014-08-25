#!/usr/bin/python
import argparse
import os
from performance_table import PerformanceTable
from cost_table import CostTable
from time_cost_mapping import TimeCostMapping


def select_config(max_money, max_time, application, size, draw=False,
                  learning_dir='../learning/', selecting_dir='./'):
    #First should find the config from the existing csv file. This is TODO
    # 1) check whether the csv exists
    # 2) check csv to get the same size and less time and money
    # 3) if find more than one, the results should be sorted by price


    cost_table = CostTable(selecting_dir+"cost_table")
    run_application = './'+application  # run_application is './matrix_mul'
    file_name = learning_dir + "performance of " + application + " " + str(size)
    changed = False
    if not os.path.isfile(file_name):
        print "please use learning.sh in directory learning first"
        print "now try to run the learning module"
        print "running the command", "cd "+learning_dir+"; bash learning.sh " + run_application + " " + str(size)
        os.system("cd "+learning_dir+"; bash learning.sh " + run_application + " " + str(size))
        changed = True

    performance_table = PerformanceTable(file_name)

    mapping = TimeCostMapping(cost_table=cost_table,
                              performance_table=performance_table)
    if changed:
        print "update file: ", application+'.csv'
        mapping.update_csv(selecting_dir+application+'.csv', size)

    if draw:
        mapping.draw()

    return mapping.get_config(max_money, max_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--time', action='store', dest='max_time',
                        help='The maximum time expected to run the application, united by second')

    parser.add_argument('-m', '--money', action='store', dest="max_money",
                        help='The maximum money expected to run the application')

    parser.add_argument('--draw', dest="draw", action='store_true', default=False,
                        help='Draw the pareto frontier, python-matplotlib required')

    parser.add_argument('--size', action='store', dest="size", required=True,
                        help='The size of the application')

    parser.add_argument('application', help='the application name')

    args = parser.parse_args()

    result = select_config(
        max_money=float(args.max_money) if args.max_money else float('inf'),
        max_time=float(args.max_time) if args.max_time else float('inf'),
        application=args.application,  # args.application is 'matrix_mul'
        size=int(args.size),
        draw=args.draw)

    for r in result:
        print 'cost:', round(r[0], 2), \
              'time:', round(r[1], 2), \
              'cpu cores:', r[2], \
              'memory:', r[3]


