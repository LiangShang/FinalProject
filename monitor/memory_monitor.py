import threading
import time
import commands


class MemoryMonitor(threading.Thread):
    def __init__(self, cgroup_dir, stop_handler, load, lxc_name=None):
        '''if lxc_name:
            self.lxc_name = lxc_name
        else:
            lxc_name = commands.getoutput('docker ps -q')
            while True:
                new_name = commands.getoutput('docker ps -q')
                if new_name != lxc_name:
                    self.lxc_name = new_name
                    break
                time.sleep(0.5)
        '''

        threading.Thread.__init__(self)
        self.thread_stop = False
        self.stop_handler = stop_handler
        self.cgroup_dir = cgroup_dir
        self.load = load

    def memory_dir(self, lxc_name):
        if self.cgroup_dir[-1] == '/':
            return self.cgroup_dir+'memory/lxc/'+lxc_name+'*'
        else:
            return self.cgroup_dir+'/memory/lxc/'+lxc_name+'*'        

    def run(self):
        while not self.thread_stop:
            lxc_name = commands.getoutput('docker ps -q')
            total_memory = commands.getoutput("docker cgroup {0} memory.limit_in_bytes".format(lxc_name))
            cur_memory_usage = commands.getoutput('docker cgroup {0} memory.usage_in_bytes'.format(lxc_name))
            percentage = float(cur_memory_usage)/float(total_memory)
            self.load[0] = total_memory
            self.load[1] = cur_memory_usage
            #self.memory_handler(total_memory, cur_memory_usage)
            #print '[memory monitor]: total memory: ', total_memory, ' usage: ', cur_memory_usage
            time.sleep(1)

    def stop(self):
        self.thread_stop = True
        self.stop_handler()


def test():
    thread1 = MemoryMonitor(1)
    thread1.start()
    time.sleep(10)
    thread1.stop()
    return

if __name__ == '__main__':
    pass
