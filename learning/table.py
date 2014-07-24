__author__ = 'Sherlock'

class PerformanceTable:

    table = {}
    cpu_range = []
    memory_range = []

    def add(self, time, cpu, memory):
        if cpu not in self.cpu_range:
            self.cpu_range.append(cpu)

        if memory not in self.memory_range:
            self.memory_range.append(memory)

        key = (cpu, memory)
        self.table[key] = time

    def pareto(self):
        """TODO: remove the records from self.table which costs the same time but more resources
                 If the cpu/memory no longer exists, delete that in cpu_range/memory_range too
        """
        pass

    def generate(self, file_name):
        """This function is to print self.table to a file with file_name"""
        self.memory_range.sort()
        self.cpu_range.sort()

        f = open(file_name, 'w')
        f.write("     ")
        for cpu in self.cpu_range:
            f.write("{:10d}".format(cpu))
        f.write("\n")
        for memory in self.memory_range:
            f.write("{:5d}".format(memory))
            for cpu in self.cpu_range:
                time = self.table.get((cpu, memory), None)
                if time is not None:
                    f.write("{:10.2f}".format(time))
                else:
                    f.write("{0}".format("      None"))
            f.write("\n")

        f.close()