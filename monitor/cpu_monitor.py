import threading
import time, os
import commands


class CpuMonitor(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, app_name, stop_handler, load):
        threading.Thread.__init__(self)
        self.app_name = app_name
        self.stop_handler = stop_handler
        self.load = load
        self.thread_stop = False

    def run(self):  # Overwrite run() method, put what you want the thread do here
        timeout_count = 0
        while not self.thread_stop:
            command = "top -c -n 1 | grep "+ self.app_name
            #print command
            f = os.popen(command)
            output = f.read()
            #print output
            if not output:
                timeout_count += 1
                print 'timeout_count: ', timeout_count
                if timeout_count > 10:
                    print 'CPU monitor suppose the applicaiton is not running'
                    self.stop()
                time.sleep(1)
                continue
            timeout_count = 0
            raw_strings = output.replace('\x1b(B\x1b[m\x1b(B\x1b[m', '').replace('\x1b(B\x1b[m\x1b[39;49m', '').split('\n')
            cpu_load = []
            #print raw_strings
            for string in raw_strings:
                if string == '':
                    continue
                #print '[string.split():] ', string.split(' ')
                cpu_info = {}
                i = 0
                strings = string.split(' ') 
                for s in strings:
                    if i == 8:
                        try:
                            cpu_info['load'] = float(s)/100
                        except:
                            break
                    if s != '':
                        i += 1  
                cur, i = -1, 0
                while i != 1:
                    if strings[cur] != '':
                        i += 1
                    cur -= 1
                try: 
                    cpu_info['thread'] = int(strings[cur])
                except:
                    continue
                cpu_load.append(cpu_info)
            #print 'cpu_load: ', cpu_load
            self.load[0] = cpu_load
            time.sleep(1)

    def stop(self):
        self.thread_stop = True
        self.stop_handler()



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
    h = lambda x:  x
    m = CpuMonitor('matrix_mul', h)
    m.start()
