import tkinter as tk
import paramiko as p
import time

# SSH Parameters ############################################
server   = "192.168.1.5"
username = "pi"
password = "Lionel2truck"
cmd      = "echo 'n' >> /home/pi/.config/pianobar/ctl"
#############################################################

# SSH Initialization ########################################
ssh = p.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(p.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
#############################################################

def sendCMD(command):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( command )
    print(ssh_stdin, ssh_stdout, ssh_stderr)

sendCMD(cmd)
time.sleep(3)
sendCMD(cmd)

print("success") #debugging only
