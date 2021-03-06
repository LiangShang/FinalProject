import sys

def parse_m_s(m_s_str):

    minute, second = m_s_str.split("m")
    second = second[0:-2]
    #print minute, second

    return float(second) + float(minute)*60


if __name__ == '__main__':

    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        throughputs = []
        size = 0
        time = 1.0
        threads = 0
        for line in f:
            if line[0:4] == 'real':
                time = parse_m_s(line.split('\t')[1])
                throughputs.append((threads, time))
            else:
                size = int(line.split(' ')[1])
                threads = line.split(' ')[0]


    total = 0
    #prices = {'2':35, '4':45, '6':65, '8':75}  # 1024MB
    #prices = {'2':53, '4':70, '6':95, '8':115}  # 2048MB
    prices = {'2':70, '4':100, '6':145, '8':165}  # 2048MB
    for t in throughputs:
        total += t[1]*prices[t[0]]
    print total
            
