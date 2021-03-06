__author__ = 'Sherlock'


class PerformanceTable:

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
            line_strings = line.split(" ")
            memory = line_strings.pop(0)
            memories.append(memory)
            i = 0
            for string in line_strings:
                if string != "":
                    string = string.strip("\n")
                    if string != 'None':
                        self.add(float(string), cpus[i], memory)
                    i += 1

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

    def generate(self, file_name):
        self.memory_range.sort(cmp=lambda x, y: len(x)<len(y) | cmp(x, y))
        self.cpu_range.sort()
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
                    f.write("{:10.5f}".format(time))
                else:
                    f.write("{0}".format("      None"))
            f.write("\n")

        f.close()

    def get_configs(self, configs, max_time, config_sorted):
        if config_sorted:
            for config in configs:
                time = self.table.get(config, None)
                if time and time < max_time:
                    print time
                    print max_time
                    return config
        else:
            max_time_available = -1
            ideal_config = None
            for config in configs:
                time = self.table.get(config, None)
                if time and time < max_time:
                    if max_time_available < 0:
                        max_time_available = time
                    if time > max_time_available:
                        max_time_available = time
                        ideal_config = config
            return ideal_config