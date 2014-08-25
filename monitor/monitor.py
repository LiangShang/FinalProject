import commands, sys, math, time
from cpu_monitor import CpuMonitor
from memory_monitor import MemoryMonitor
from cost_table import CostTable

total_cpu = 8
total_memory = 9223372036854775807l
idle_thres = 0.2
saturate_thres = 0.98

cpu_running = False
memory_running = False
def cpu_stop():
    global cpu_running, memory_monitor
    cpu_running = False
    memory_monitor.stop()


def memory_stop():
    global memory_running
    memory_running = False


def set_cpu(cpu):
    global uuid, cur_config
    cur_config['cpu'] = cpu
    commands.getoutput('docker cgroup '+uuid+' cpuset.cpus 0-'+ str(cpu-1))    

def set_memory(memory):
    global uuid, cur_config
    cur_config['memory'] = memory
    commands.getoutput('docker cgroup '+uuid+' memory.limit_in_bytes '+ str(memory))  
    

def memory_handler(total_memory, cur_memory_usage):
    global idle_thres, cur_config, cost_table
    saturate_thres = 0.8
    percent = float(cur_memory_usage)/float(total_memory) 
    if percent > saturate_thres + 0.05 or percent < saturate_thres - 0.05:
        return cost_table.find_memory(int(float(cur_memory_usage)/saturate_thres))
        #return int(float(cur_memory_usage)/saturate_thres)
    else:
        return cur_config['memory']


def cpu_handler(cpu_load):
   
    global cur_config, total_cpu, idle_thres, saturate_thres
    print '[cur_config]: ', cur_config
    if not cpu_load:
        return None
    thread_no = cpu_load[0].get('thread', None)
    if thread_no is None:
        return None
    # if current cpu in lxc is larger than the thread, then shrink to the thread number
    if thread_no < cur_config['cpu']:
        #set_cpu(thread_no)
        return thread_no
    total_load = 0  #sum(map(lambda x: x['load'], cpu_load))
    for l in cpu_load:
        tmp = l.get('load', None)
        if tmp:
            total_load += tmp    

    avg_load = total_load/cur_config['cpu']
    print 'cpu avg_load: ', avg_load
    # if the current load is saturated 
    if avg_load > saturate_thres:
        # if the threads of the application equals current cup number then cannot upgrade
        if thread_no == cur_config['cpu']:
            print 'thread equals lxc cpu'
            return thread_no
        # else increase the lxc's cpu number to thread
        elif thread_no < total_cpu:
            #set_cpu(thread_no)
            print 'arise cpu to ', thread_no
            return thread_no
        else:
            #set_cpu(total_cpu)
            return total_cpu
    # load for each cpu is too low
    elif avg_load < idle_thres:
        if cur_config['cpu'] == 1:
            print 'only one cpu in lxc'
            return 1
        else:
            cpu_no = 1 if math.ceil(total_load) == 0 else int(math.ceil(total_load))
            print 'lxc cpu thrink to ', cpu_no 
            #set_cpu(cpu_no)
            return cpu_no

    pass

if __name__ == '__main__':
    app_name = 'mandelbrot_set'
    cur_config = {'cpu': 1, 'memory': 1073741824}
    cost_table = CostTable('cost_table')
    # start the docker running application continuously to emulate online application
    uuid = commands.getoutput('docker ps -q')

    previous_cpu_load, cpu_load = [0], [[0]]
    previous_memory_load, memory_load = (0, 0), [0, 0]
    memory_monitor = MemoryMonitor(cgroup_dir='/group', stop_handler=memory_stop, load=memory_load)
    print 'momory monitor inited'
    cpu_monitor = CpuMonitor(app_name=app_name, stop_handler=cpu_stop, load=cpu_load)
    print 'cpu monitor inited'
    memory_monitor.start()
    cpu_monitor.start()

    cpu_running = True
    memory_running = True

    while cpu_running and memory_running:
        if previous_cpu_load != cpu_load[0]:
            cur_cpu_load = list(cpu_load[0])
            max_cpu = cpu_handler(cur_cpu_load)
            previous_cpu_load = cur_cpu_load
        else:
            max_cpu = int(cur_config['cpu'])

        cur_memory_load = (memory_load[0], memory_load[1])
        if previous_memory_load != cur_memory_load:
            max_memory = memory_handler(*cur_memory_load)
            previous_memory_load = cur_memory_load
        else:
            max_memory = cur_config['memory']
        max_cpu = int(cur_config['cpu']) if max_cpu is None else max_cpu
        #max_cpu, max_memory = cost_table.get_config(max_cpu, max_memory)
        set_cpu(max_cpu)
        set_memory(max_memory)

        commands.getoutput('echo '+str(time.time())+' '+ str(cur_config['cpu'])+' '+str(cur_config['memory']) +' >> record')
        time.sleep(1)
    # exit condition
    print 'detect termination'
    # calculate money


