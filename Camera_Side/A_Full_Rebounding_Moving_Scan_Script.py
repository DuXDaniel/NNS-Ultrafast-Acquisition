import time
import socket
import subprocess
import numpy as np

positions_init = list(np.arange(-100, -50, 0.5))
positions_base = []

cur_x_pos = 0
cur_z_pos = 0

for val in positions_init:
    positions_base.append(-300)
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

realign_time = 3600
movement_time = 600
positions_arr = positions_base # Establishes a search pattern using the basis

count = 0
num_x_moves = 0
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

    for i in np.arange(0,14):
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
    
    cumultime = time.time()
    if ((cumultime - set_time) > realign_time and position != -300):
        acqAnother = input("Enter 0 to exit, otherwise acquire:")
        # counter = counter - 1
        set_time = time.time()

    if (acqAnother == '0'):
        break

    cumultime = time.time()
    if ((cumultime - set_time) > movement_time and position != -300):
        # Moving stage
        print("Moving stage")
        hFoundWnd = self.FocusTheDesiredWnd()
        if(hFoundWnd != 0):
            self.ClickMouse(1584+15,52+15)

            # x move
            cur_x_pos = cur_x_pos - 0.005
            self.ClickMouse(1648+58,183+12)
            self.PressKey('+{VK_HOME}')
            self.PressKey(str(cur_x_pos))
            
            # z move
            if (num_x_moves == 5):
                cur_z_pos = cur_z_pos - 0.010
                self.ClickMouse(1648+58,246+12)
                self.PressKey('+{VK_HOME}')
                self.PressKey(str(cur_z_pos))
                num_x_moves = 0
                
            self.ClickMouse(1757+50,145+12)
            num_x_moves = num_x_moves + 1
        else:
            print("Cannot find microscope control. Exiting.")
            break

print("ABBA scan complete.\r\n")

f = open("AcqStat.txt",'w')
f.write("-1")
f.close()

try:
    camCommand_client.shutdown(socket.SHUT_RDWR)
except:
    pass

print("Socket close operation complete.\r\n")