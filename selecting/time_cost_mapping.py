__author__ = 'Sherlock'
import csv


class TimeCostMapping:
    """mapping is the tuple with format (cost, time, (cpu, memory))"""
    mapping = []
    pareto_frontier = []

    def __init__(self, cost_table, performance_table):
        for memory in cost_table.memory_range:
            for cpu in cost_table.cpu_range:
                money = cost_table.table.get((cpu, memory), None)
                performance = performance_table.table.get((cpu, memory), None)
                if money and performance:
                    self.mapping.append((performance * money, performance, (cpu, memory)))

        # get the pareto_frontier
        self.mapping.sort(cmp=lambda x, y: cmp(x[0], y[0]))  # sort by cost
        min_time = float("inf")
        for a in self.mapping:
            if a[1] < min_time:
                self.pareto_frontier.append(a)
                min_time = a[1]
                # self.pareto_frontier.sort(cmp=lambda x, y: cmp(x[1], y[1]))  # sort by time

    def get_config(self, money, time):
        # according to the time, find the config with minimum cost
        result = []
        for a in self.pareto_frontier:
            if a[1] <= time and a[0] <= money:
                result.append((round(a[0],2),round(a[1],2))+a[2])
        return result

    def draw(self):
        import matplotlib.pyplot as plt

        costs = [a[0] for a in self.mapping]
        times = [a[1] for a in self.mapping]
        plt.ylabel("Cost")
        plt.xlabel("Execution Time")
        plt.plot(times, costs, '.')
        pareto_costs = [a[0] for a in self.pareto_frontier]
        pareto_times = [a[1] for a in self.pareto_frontier]
        plt.plot(pareto_times, pareto_costs, 'k', lw=2)
        plt.show()

    def update_csv(self, csv_name, size):
        csv_dict = {}
        try:
            csv_file = open(csv_name, 'r+')
        except:
            open(csv_name, 'w').close()
            csv_file = open(csv_name, 'r+')
        reader = csv.reader(csv_file)
        for cpu, memory, matrix_size, time, cost in reader:
            csv_dict[cpu, memory, matrix_size, time] = cost
        for record in self.mapping:
            csv_dict[record[2][0], record[2][0], size, record[1]] = record[0]

        csv_list = []
        for key, value in csv_dict.items():
            string = key + (round(float(value), 2),)
            csv_list.append(string)

        with open(csv_name, "wb") as csv_file:
            writer = csv.writer(csv_file)
            for data in csv_list:
                writer.writerow(data)
