__author__ = 'Sherlock'


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

    def pareto(self):
        """TODO: remove the records from self.table which costs the same time but more resources
                 If the cpu/memory no longer exists, delete that in cpu_range/memory_range too
        """
        self.average()
        pass

    def generate(self, file_name):
        """This function is to print self.table to a file with file_name"""
        self.memory_range.sort(cmp=lambda x, y: len(x)<len(y) | cmp(x, y))
        self.cpu_range.sort()

        f = open(file_name, 'w')
        f.write("     ")
        for cpu in self.cpu_range:
            f.write("{:10d}".format(int(cpu)))
        f.write("\n")
        for memory in self.memory_range:
            f.write("{:5s}".format(memory))
            for cpu in self.cpu_range:
                time = self.table.get((cpu, memory), None)
                if time is not None:
                    f.write("{:10.3f}".format(time))
                else:
                    f.write("{0}".format("      None"))
            f.write("\n")

        f.close()