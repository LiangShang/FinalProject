
__author__ = 'Sherlock'
import commands


def run_command(com):
    status, output = commands.getstatusoutput(com)
    return status, output


def run_command_with_docker(com, container, cpu, memory):
    command_to_exe = "sudo docker run -i -v `pwd`:/Final --rm -m "+\
                     str(memory)+"k --cpuset="+str(cpu)+" "+container+" "+com
    print command_to_exe
    return run_command(command_to_exe)



