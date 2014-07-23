import paramiko, base64

def execute_remote_command(host_address, username, password, command):

    # connect to the host
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host_address, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)

    print "Executing %s on host: %s" % (command, host_address)

    # if output and standard error hasn't been read off before
    # buffer is full the host will hang
    output = None
    error = None
    output_str = ""
    error_str = ""

    while output != "":
        output = stdout.readline()
        # print output while reading
        if output:
            print output
            output_str += output

    while error != "":
        error = stderr.readline()
        error_str += error

    # print error at the end
    print error_str if error_str else "Execution completed"

    ssh.close()

    return [output_str, error_str]


if __name__ == '__main__':
    output_str, err_str = execute_remote_command('192.168.59.103', 'docker', 'tcuser', 'ls')
    print output_str
