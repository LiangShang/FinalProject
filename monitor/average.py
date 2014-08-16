import sys
if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        throughputs = []
        avgs = []
        i = 0
        for line in f:
            if i == 10:
                avgs.append(sum(throughputs)/len(throughputs))
                throughputs = []
                i = 0
            try:
                throughputs.append(float(line))  
                i += 1
            except: 
                continue

        #throughputs.sort()
        #throughputs = throughputs[2:-2]
        avgs.append(sum(throughputs)/len(throughputs))
        print avgs
