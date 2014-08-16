from cost_table import CostTable

def count(record_name, cost_table_name):
    money = 0
    cost_table = CostTable(cost_table_name)
    with open(record_name, 'r') as f:
        
        info = f.readline().strip("\n").split(" ")
        former_time, former_cpu, former_memory = float(info[0]), str(int(float(info[1]))), info[2]
        for line in f:
            info = line.strip("\n").split(' ')
            now_time = float(info[0])
            price = cost_table.get(former_cpu, former_memory)
            if price is None:
                price = cost_table.get(former_cpu, str(1024*1024*1024))
                #continue
                #break
            #if (now_time - former_time) >5 :
                #print info, str(now_time - former_time)
            money += price * (now_time - former_time)
            former_time = now_time
            former_cpu, former_memory = str(int(float(info[1]))), info[2]

    return money


if __name__ == '__main__':
    print count('record', 'cost_table')
