import commands

if __name__ == '__main__':

    with open('online_record', 'r') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split(' ')
            cpu = int(data[1])
            size = int(data[2]) 
            c = 'docker run -v `pwd`:/Final --rm -m 1024m --cpuset=0-'+str(cpu-1)+' -w /Final  ubuntu_python bash -c \'(time timeout 5m '+line+') 2>tmp\''
            print c
            commands.getoutput(c)
             
            c = 'echo '+ str(cpu) + ' '+ str(size) +' >>throughput_1024MB_mand'
            print c
            commands.getoutput(c)
            c = 'head -n 2 tmp | tail -n 1 >> throughput_1024MB_mand'
            print c
            commands.getoutput(c)

    with open('online_record', 'r') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split(' ')
            cpu = int(data[1])
            size = int(data[2]) 
            c = 'docker run -v `pwd`:/Final --rm -m 2048m --cpuset=0-'+str(cpu-1)+' -w /Final  ubuntu_python bash -c \'(time timeout 5m '+line+') 2>tmp\''
            print c
            commands.getoutput(c)
             
            c = 'echo '+ str(cpu) + ' '+ str(size) +' >>throughput_2048MB_mand'
            print c
            commands.getoutput(c)
            c = 'head -n 2 tmp | tail -n 1 >> throughput_2048MB_mand'
            print c
            commands.getoutput(c)

    with open('online_record', 'r') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split(' ')
            cpu = int(data[1])
            size = int(data[2]) 
            c = 'docker run -v `pwd`:/Final --rm -m 3072m --cpuset=0-'+str(cpu-1)+' -w /Final  ubuntu_python bash -c \'(time timeout 5m '+line+') 2>tmp\''
            print c
            commands.getoutput(c)
             
            c = 'echo '+ str(cpu) + ' '+ str(size) +' >>throughput_3072MB_mand'
            print c
            commands.getoutput(c)
            c = 'head -n 2 tmp | tail -n 1 >> throughput_3072MB_mand'
            print c
            commands.getoutput(c)

    with open('online_record', 'r') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split(' ')
            cpu = int(data[1])
            size = int(data[2]) 
            c = 'docker run -v `pwd`:/Final --rm -m 4096m --cpuset=0-'+str(cpu-1)+' -w /Final  ubuntu_python bash -c \'(time timeout 5m '+line+') 2>tmp\''
            print c
            commands.getoutput(c)
             
            c = 'echo '+ str(cpu) + ' '+ str(size) +' >>throughput_4096MB_mand'
            print c
            commands.getoutput(c)
            c = 'head -n 2 tmp | tail -n 1 >> throughput_4096MB_mand'
            print c
            commands.getoutput(c)
