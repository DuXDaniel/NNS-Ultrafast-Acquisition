import time
import socket
import subprocess
import numpy as np

positions_init = list(np.arange(-100, -48, 1.5))
positions_base = []

for val in positions_init:
    cur_rebound = val
    positions_base.append(cur_rebound)
    positions_base.append(val)

print(positions_base)

camCommand_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Searching for connection.\r\n")

camCommand_client.connect(("192.168.254.120", 6667))##########################
print("Camera commands connected.\r\n")

f = open("AcqStat.txt",'w')
f.write("1")
f.close()

subprocess.Popen(['python',"ABBA_Camera_Script.py"])

realign_time = 1800
positions_arr = positions_base # Establishes a search pattern using the basis

count = 0
counter = 0
step_type = 0
while counter < len(positions_arr):
    position = positions_arr[counter]
    try:
        sendVal = "-1"
        camCommand_client.send(sendVal.encode())
    except:
        break

    camComm_buffer = ''

    print("Moving delay stage...\r\n")

    camComm_buffer = '1'
    camComm_buffer += str(position)

    try:
        camCommand_client.send(camComm_buffer.encode())
    except:
        break

    try:
        camComm_buffer = camCommand_client.recv(1024).decode()
    except:
        break

    if (step_type == 0):
        moveTime = input("Move specimen, turn on pump, and then hit enter.")
    else:
        moveTime = input("Turn the pump off and hit enter.")

    for i in np.arange(0,40):
        print("Waiting for acquisition.")
        
        f = open("AcqStat.txt","w")
        f.write('0')
        f.close()

        statLine = '0'

        while (statLine == '0'):
            f = open("AcqStat.txt",'r')
            statLine = f.readline()
            f.close()
            time.sleep(1)

        count = count + 1
        print(count)
        
    counter = counter + 1

    recvSignal = 1

    camComm_buffer = ''

    time.sleep(0.05)

    if step_type == 0:
        step_type = 1
    else:
        step_type = 0

print("ABBA scan complete.\r\n")

f = open("AcqStat.txt",'w')
f.write("-1")
f.close()

try:
    camCommand_client.shutdown(socket.SHUT_RDWR)
except:
    pass

print("Socket close operation complete.\r\n")