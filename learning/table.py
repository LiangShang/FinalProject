__author__ = 'Sherlock'

MAX_TIME = 3
class PerformanceTable:

    table = {}
    times = {}
    cpu_range = []
    memory_range = []

    def get(self, cpu, memory):
        return self.table.get((cpu, memory), None)

    def add(self, time, cpu, memory):
        if cpu not in self.cpu_range:
            self.cpu_range.append(cpu)

        if memory not in self.memory_range:
            self.memory_range.append(memory)

        key = (cpu, memory)
        previous_times = self.table.get(key, None)
        if previous_times is None:  # first time the key appears
            self.table[key] = [time]
        else:
            if len(previous_times) < MAX_TIME:
                self.table[key].append(time)
            else:
                self.table[key].sort()
                if time > self.table[key][0]:
                    self.table[key][0] = time

    def average(self):
        for key in self.table.keys():
            print self.table[key]
            self.table[key] = sum(self.table[key]) / len(self.table[key])

    def pareto(self):
        """TODO: remove the records from self.table which costs the same time but more resources
                 If the cpu/memory no longer exists, delete that in cpu_range/memory_range too
        """
        for memory in self.memory_range:
            min_time = -1
            for cpu in self.cpu_range:
                time = self.table.get((cpu, memory), None)
                if time:
                    if min_time < 0:
                        min_time = time
                    elif time >= min_time :
                        self.table[(cpu, memory)] = None
                    else:
                        min_time = time
        for cpu in self.cpu_range:
            min_time = -1
            for memory in self.memory_range:
                time = self.table.get((cpu, memory), None)
                if time:
                    if min_time < 0:
                        min_time = time
                    elif time >= min_time :
                        self.table[(cpu, memory)] = None
                    else:
                        min_time = time



    def generate(self, file_name):
        """This function is to print self.table to a file with file_name"""
        self.memory_range.sort(cmp=lambda x, y: len(x)<len(y) | cmp(x, y))
        self.cpu_range.sort()

        file_name = file_name.strip()
        f = open(file_name, 'w')
        f.write("     ")
        for cpu in self.cpu_range:
            f.write("{0:10d}".format(int(cpu)))
        f.write("\n")
        for memory in self.memory_range:
            f.write("{0:5s}".format(memory))
            for cpu in self.cpu_range:
                time = self.table.get((cpu, memory), None)
                if time is not None:
                    f.write("{0:10.5f}".format(time))
                else:
                    f.write("{0}".format("      None"))
            f.write("\n")

        f.close()
