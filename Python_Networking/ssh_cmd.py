import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    '''1. function that connect to an SSH server and runs a single command.'''

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    '''2. we set the policy to accept the SSH key for the SSH server we are connecting  to and make connection.'''
    client.connect(ip, port=port, username=user, password=passwd)


    _, stdout, stderr = client.exec_command(cmd)
    '''3. assuming the connection is made we run the command that we pass to in the cell to the ssh_command function'''
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Otput ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    '''4. use this module to get username from the current enviroment,but since our username is different on two machines, we explicitly
    ask for the username on the command line.'''
    # user = get.pass.getuser()
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    port = input('Enter port or <CR>: ')
    cmd = input('Enter command: ')
    ssh_command(ip, port, user, password, cmd)
    '''5. run and send to be executed'''