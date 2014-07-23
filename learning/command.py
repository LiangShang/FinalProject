from learning.time import parse_time

__author__ = 'Sherlock'
import commands


def run_command(com):
    status, output = commands.getstatusoutput(com)
    return status, output


def run_command_with_docker(com, container, cpu, memory):
    command_to_exe = "docker run -i -t --rm -m "+str(memory)+"k --cpuset="+str(cpu)+" "+container+" "+com
    print command_to_exe
    return run_command(command_to_exe)


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
