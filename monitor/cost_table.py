__author__ = 'Sherlock'


class CostTable:

    table = {}
    times = {}
    cpu_range = []
    memory_range = []

    def __init__(self, file_name):

        f = open(file_name)
        cpu_str = f.readline()
        cpus = []
        for string in cpu_str.split(" "):
            if string != "":
                cpus.append(string.strip("\n"))
        # load the learnt statistics to the table

        memories = []
        for line in f:
            line_strings = line.strip("\n").split(" ")
            memory = line_strings.pop(0)
            memories.append(int(memory))
            i = 0
            for string in line_strings:
                if string != "":
                    if string != 'None':
                        
                        self.add(float(string), cpus[i], memory)
                    i += 1

    def find_memory(self, m):
        memories = [int(memory) for memory in self.memory_range]
        n = len(memories)
        less_cur, more_cur = 0, n-1
        for i in range(n):
            if memories[i] == m:
                return m
            elif memories[i] < m:
                less_cur = i
            else:
                more_cur = i
                break
        if (m - memories[less_cur])*7 < (memories[more_cur] - m):
            return memories[less_cur]
        else:
            return memories[more_cur]


    def get(self, cpu, memory):
        return self.table.get((cpu, memory), None)

    def add(self, time, cpu, memory):
        if cpu not in self.cpu_range:
            self.cpu_range.append(cpu)

        if memory not in self.memory_range:
            self.memory_range.append(memory)

        key = (cpu, memory)
        self.table[key] = time
        app_time = self.times.get(key, None)
        if app_time:
            self.times[key] = int(app_time) + 1
        else:
            self.times[key] = 1

    def average(self):
        for key in self.table.keys():
            app_time = self.times[key]
            self.table[key] = self.table[key]/app_time

    def sort(self):
        self.memory_range.sort(cmp=lambda x, y: len(x) < len(y) | cmp(x, y))
        self.cpu_range.sort()

    def generate(self, file_name):
        self.sort()
        f = open(file_name, "w")
        f.write("     ")
        for cpu in self.cpu_range:
            f.write("{:10d}".format(int(cpu)))
        f.write("\n")
        for memory in self.memory_range:
            f.write("{:5s}".format(memory))
            for cpu in self.cpu_range:
                time = self.table.get((cpu, memory), None)
                if time is not None:
                    f.write("{:10.2f}".format(time))
                else:
                    f.write("{0}".format("      None"))
            f.write("\n")

        f.close()

    def get_config(self, max_cpu, max_memory, cost_per_time):
        memory = self.find_memory(max_memory)
        n = len(self.cpu_range) 
        cpus = map(int, self.cpu_range)
        cpu_location = n
        smaller_location = 0
        for i in range(n):
            if cpus[i] < max_cpu:
                smaller_location = i
            elif cpus[i] == max_cpu:
                cpu_location = i
                break
        # If max_cpu is in the range
        if cpu_location == n :
            # if max_cpu is more than the maximum in range
            if cpus[n-1] < max_cpu:
                cpu_location = n-1
            # else max_cpu not hit
                cpu_location = smaller_location
        # Now cpu_location is reasonable
        for i in range(cpu_location, -1, -1):
            cost = self.get(self.cpu_range[1], str(memory))
            print "cost: ", cost
            if cost and cost <= cost_per_time:
                return cpus[1], memory
        # Get out of loop means no hit on the price, then memory should be shrunk
        memories = map(int, self.memory_range)
        m = len(memories)
        memory_location = m
        for i in range(m):
            if memories[i] == memory:
                memory_location = i
        for j in range(memory_location-1, -1, -1):
            tmp_memory = memories[j]
            for i in range(cpu_location, -1, -1):
                cost = self.get(self.cpu_range[1], str(memory))
                print "cost: ", cost
                if cost and cost <= cost_per_time:
                    return cpus[1], memory
        #Hit here means no config fits
        return None, None

        pass

