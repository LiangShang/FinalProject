import sys

def parse_m_s(m_s_str):

    minute, second = m_s_str.split("m")
    second = second[0:-2]
    #print minute, second

    return float(second) + float(minute)*60


if __name__ == '__main__':

    file_name = sys.argv[1]
    #target_name = sys.argv[2]
    with open(file_name, 'r') as f:
        throughputs = []
        size = 0
        time = 1.0
        threads = 0
        for line in f:
            if line[0:4] == 'real':
                time = parse_m_s(line.split('\t')[1])
                throughputs.append(time)
            else:
                size = int(line.split(' ')[1])
                threads = int(line.split(' ')[0])
    print sum(throughputs)
    #with open(target_name, 'w') as f:
        #for t in throughputs:
            #f.write(str(t)+'\n')
