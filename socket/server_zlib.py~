from Brightness import Brightness as ParallelPrefixSum
import sys
import socket
import zlib
try:
    import json
except ImportError:
    import simplejson as json

HOST = "192.168.100.1"
#HOST = "127.0.0.1"
#PORT = 8097
BUFFER = 2048

if __name__ == "__main__":

    PORT = int(sys.argv[1])    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(0)


    while True:
        client_sock, client_addr = sock.accept()
        msg = ''
        while True:
            recv = client_sock.recv(BUFFER)

            msg += recv
            if '$$' in recv:
                break
        msg = msg[0:-2]

        msg = zlib.decompress(msg)

        func, jdata = msg.split('*')[0], msg.split('*')[1]
        data = json.loads(jdata)
        result = getattr(sys.modules[__name__], func)(data)
        output = zlib.compress(json.dumps(result), zlib.Z_BEST_COMPRESSION)+'$$'

        client_sock.send(output)
    sock.close()

    
