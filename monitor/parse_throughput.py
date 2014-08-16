import sys

def parse_m_s(m_s_str):

    minute, second = m_s_str.split("m")
    second = second[0:-2]
    #print minute, second

    return float(second) + float(minute)*60


if __name__ == '__main__':

    file_name = sys.argv[1]
    target_name = sys.argv[2]
    with open(file_name, 'r') as f:
        throughputs = []
        size = 0
        concurrency = 0
        time = 1.0
        for line in f:
            if line[0:4] == 'real':
                time = parse_m_s(line.split('\t')[1])
                throughputs.append((concurrency, size*size/time))
            else:
                size = int(line.split(' ')[1])
                concurrency = int(line.split(' ')[0])

    with open(target_name, 'w') as f:
        #throughputs.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        for c, t in throughputs:
            #f.write(str(c)+' '+str(t)+'\n')
            f.write(str(t)+'\n')
