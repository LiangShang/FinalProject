
import socket, random, sys


HOST = '192.168.100.1'
#PORT = 8095
BUFFER = 2048

if __name__ == '__main__':
    PORT = int(sys.argv[1])
    size = int(sys.argv[2])
    matrix = [random.randint(1, 10) for i in range(size)]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    string = 'ParallelPrefixSum*['
    for num in matrix:
        string += str(num)+", "
    string = string[0:-2]
    string += "]$" 
    #string = json.dumps(matrix) + '$'
    #print string
    sock.send(string)

    msg = ""
    while True:
        recv = sock.recv(BUFFER)
        msg += recv
        if "$" in recv:
            break

    
