import exe_time
from core.paramiko_script import execute_remote_command
from core.vm_manager import create_instance

if __name__ == '__main__':

    vm_ip = '192.168.59.103'
    username = 'docker'
    password = 'tcuser'

    command = 'scp Sherlock@192.168.59.3:/Users/Sherlock/Documents/Code/OpenStack/VagrantRoot/runner2.py runner2.py'

    output_str, err_str = execute_remote_command(vm_ip, username, password, command)

    #output_str, err_str = execute_remote_command(vm_ip, username, password, command)

    parse(output_str)
    #outpye_str should be like [overhead]\n[overhead]
    #write it to the file?
