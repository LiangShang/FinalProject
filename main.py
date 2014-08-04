import argparse
from selecting.selecting import select_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', action='store', dest='max_time',
                        help='The maximum time expected to run the application, united by second')
    parser.add_argument('-m', '--money', action='store', dest="max_money",
                        help='The maximum money expected to run the application')
    parser.add_argument('--size', action='store', dest="size", required=True,
                        help='The size of the application')
    parser.add_argument('-p', '--parameters', action='append', dest='parameters', default=[],
                        help='the parameters of running the application, '
                             'if there are more than 2 parameters. please type in the format'
                             '-p <para1> -p <para2> ...')
    parser.add_argument('application', help='the application name')

    args = parser.parse_args()

    configs = select_config(
        max_money=float(args.max_money) if args.max_money else float('inf'),
        max_time=float(args.max_time) if args.max_time else float('inf'),
        application=args.application,
        size=int(args.size),
        learning_dir='learning/',
        selecting_dir='selecting/')

    if configs is None:
        print "no such configuration fits the requirements"
        exit()

    cpu, memory = configs[0][2], configs[0][3]

    import commands

    image = 'stackbrew/hipache'
    script = './' + args.application + ' ' + ' '.join(args.parameters)+ ' '+cpu + ' > result'
    commands.getoutput("echo '" + script + "' > learning/main_script")
    bash_script = 'sudo docker run --rm -v `pwd`/learning/:/Final -m ' + memory + ' --cpuset=0-' + str(
        int(cpu) - 1) + ' -w /Final ' + image + ' bash main_script'
    print bash_script
    commands.getoutput(bash_script)
    print "result is generate in file 'result', please check!"
    #commands.getoutput('rm script')

