import threading
import time
import commands


class MemoryMonitor(threading.Thread):
    def __init__(self, cgroup_dir, memory_handler, lxc_name=None):
        if lxc_name:
            self.lxc_name = lxc_name
        else:
            lxc_name = commands.getoutput('docker ps -q')
            while True:
                new_name = commands.getoutput('docker ps -q')
                if new_name != lxc_name:
                    self.lxc_name = new_name
                    break
                time.sleep(0.5)

        threading.Thread.__init__(self)
        self.thread_stop = False
        self.memory_handler = memory_handler
        if cgroup_dir[-1] == '/':
            self.memory_dir = cgroup_dir+'memory/lxc/'+self.lxc_name+'*'
        else:
            self.memory_dir = cgroup_dir+'/memory/lxc/'+self.lxc_name+'*'

    def run(self):
        while not self.thread_stop:
            total_memory = commands.getoutput("cd {0}; cat memory_limit_in_bytes".format(self.memory_dir))
            cur_memory_usage = commands.getoutput('cd {0}; cat usage_in_bytes'.format(self.memory_dir))
            percentage = float(cur_memory_usage)/total_memory
            self.memory_handler(percentage)
            time.sleep(1)

    def stop(self):
        self.thread_stop = True


def test():
    thread1 = MemoryMonitor(1)
    thread1.start()
    time.sleep(10)
    thread1.stop()
    return

if __name__ == '__main__':
    pass