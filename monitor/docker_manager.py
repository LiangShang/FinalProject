import commands


def change_cpu(uuid, cpu_cores):
    commands.getoutput('docker cgroup '+uuid+' 0-'+str(int(cpu_cores)-1))


def change_memory(uuid, memory):
    commands.getoutput('docker cgroup '+uuid+' '+memory)