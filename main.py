from command import run_command_with_docker, run_command
from time import parse_time

__author__ = 'Sherlock'

if __name__ == '__main__':
    command = "bash"
    a, b = run_command_with_docker(command, "ubuntu:14.04", "1", "2048")
    if a != 0:
        print "command '"+command+"' is wrong"
        print b
        exit()
    a, b = run_command("time pwd")
    print b
    total_time = parse_time(b)