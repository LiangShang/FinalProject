__author__ = 'Sherlock'
import matplotlib.pyplot as plt

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
        #self.pareto_frontier.sort(cmp=lambda x, y: cmp(x[1], y[1]))  # sort by time

    def get_config(self, money, time):
        # according to the time, find the config with minimum cost
        result = None
        for a in self.pareto_frontier:
            if a[1] <= time:
                result = a
                break
        if not result or result[0] > money:
            return None
        return result[2]

    def draw(self):
        costs = [a[0] for a in self.mapping]
        times = [a[1] for a in self.mapping]
        plt.xlabel("Cost")
        plt.ylabel("Execution Time")
        plt.plot(costs, times, '.')
        pareto_costs = [a[0] for a in self.pareto_frontier]
        pareto_times = [a[1] for a in self.pareto_frontier]
        plt.plot(pareto_costs, pareto_times, 'k', lw=2)
        plt.show()
