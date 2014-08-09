import threading
import time
import commands


class CpuMonitor(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, app_name, cpu_handler):
        threading.Thread.__init__(self)
        self.app_name = app_name
        self.cpu_handler = cpu_handler
        self.thread_stop = False

    def run(self):  # Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            output = commands.getoutput("top -n 1 -d 0.5 | grep " + self.app_name)
            if output:
                i = 0
                for s in output.split(' '):
                    if i == 8:
                        cpu_load = float(s)
                        self.cpu_handler(cpu_load)
                    if s != '':
                        i += 1

    def stop(self):
        self.thread_stop = True



def test():
    thread1 = CpuMonitor(1)
    thread2 = CpuMonitor(2)
    thread1.start()
    thread2.start()
    time.sleep(10)
    thread1.stop()
    thread2.stop()
    return


if __name__ == '__main__':
    pass