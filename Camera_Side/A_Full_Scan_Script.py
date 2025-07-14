import time
import socket
import subprocess
import numpy as np

positions_base = list(np.arange(-300, 120, 20)) #[-300, -295, -250, -200, -150, -100, -50, 0]

camCommand_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Searching for connection.\r\n")

camCommand_client.connect(("192.168.254.120", 6667))##########################
print("Camera commands connected.\r\n")

f = open("AcqStat.txt",'w')
f.write("1")
f.close()

subprocess.Popen(['python',"ABBA_Camera_Script.py"])

realign_time = 1800 #850
positions_arr = positions_base # Establishes a search pattern using the basis

count = 0
acqAnother = input("Enter 0 to exit, otherwise acquire:")
set_time = time.time()
counter = 0
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
    
    cumultime = time.time()
    if ((cumultime - set_time) > realign_time):
        acqAnother = input("Enter 0 to exit, otherwise acquire:")
        # counter = counter - 1
        set_time = time.time()

    if (acqAnother == '0'):
        break

    for i in np.arange(0,60):
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

print("ABBA scan complete.\r\n")

f = open("AcqStat.txt",'w')
f.write("-1")
f.close()

try:
    camCommand_client.shutdown(socket.SHUT_RDWR)
except:
    pass

print("Socket close operation complete.\r\n")