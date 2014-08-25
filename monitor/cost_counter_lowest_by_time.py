import sys
from cost_table import CostTable

def parse_m_s(m_s_str):

    minute, second = m_s_str.split("m")
    second = second[0:-2]
    #print minute, second

    return float(second) + float(minute)*60


def get_cost_and_throughput(file_name, memory):
    global cost_table

    with open(file_name, 'r') as f:
        results = []
        size = 0
        time = 1.0
        threads = 0
        for line in f:
            if line[0:4] == 'real':
                time = parse_m_s(line.split('\t')[1])
                cost = cost_table.get(threads, memory) * time
                throughput = size*size/time
                results.append((cost, throughput, time))
            else:
                size = int(line.split(' ')[1])
                threads = line.split(' ')[0]
        return results
    

if __name__ == '__main__':

    file_name_1024 = '../application/throughput_1024MB_mand'
    file_name_2048 = '../application/throughput_2048MB_mand'
    file_name_3072 = '../application/throughput_3072MB_mand'
    file_name_4096 = '../application/throughput_4096MB_mand'
    cost_table = CostTable('cost_table')
    r_1024 = get_cost_and_throughput(file_name_1024, str(1024*1024*1024))
    r_2048 = get_cost_and_throughput(file_name_2048, str(2*1024*1024*1024))
    r_3072 = get_cost_and_throughput(file_name_3072, str(3*1024*1024*1024))  
    r_4096 = get_cost_and_throughput(file_name_4096, str(4*1024*1024*1024))
    results = []
    f = lambda x, y : x if x[0] <= y[0] else y
    for i in range(len(r_1024)):
        r = f(f(f(r_1024[i], r_2048[i]), r_3072[i]),r_4096[i])
        results.append(r)
    
    with open(sys.argv[1], 'w') as f:
        total_price = 0
        total_time = 0
        for r in results:
            total_price += r[0]
            total_time += r[2]
            f.write(str(r[1])+'\n')
        print 'total_price: ', total_price
        print 'total_time: ', total_time
            
