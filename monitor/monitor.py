import commands
from monitor.cpu_monitor import CpuMonitor
from monitor.memory_monitor import MemoryMonitor


def memory_handler():
    pass

def cpu_handler():
    pass

if __name__ == '__main__':

    app_name = 'Adp_cpu'
    # start the docker running application continuously to emulate online application
    cur_config = {'cpu': 1}
    uuid = commands.getoutput('docker run -d')

    memory_monitor = MemoryMonitor(cgroup_dir='/group', memory_handler=memory_handler)
    cpu_monitor = CpuMonitor(app_name=app_name, cpu_handler=cpu_handler)
    memory_monitor.start()
    cpu_monitor.start()

    # exit condition
