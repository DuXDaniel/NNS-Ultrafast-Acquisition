import time
import socket
import subprocess

positions_base = [0]#[-150, -125, -100, -90, -85, -84, -83, -82, -81, -80, -79, -78, -77, -76, -75, -70, -65, -60, -50, 0, 50, 100, 150, 200, 250, 300]
# [-150, -50, 0, 50, 100, 150, 200, 250, 300]
positions_base_2 = [0]#[300, 250, 200, 150, 100, 50, 0, -50, -60, -65, -70, -75, -76, -77, -78, -79, -80, -81, -82, -83, -84, -85, -90, -100, -125, -150]
# [300, 250, 200, 150, 100, 50, 0, -50, -150]
return_pos = -100 # -100 # 75

camCommand_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Searching for connection.\r\n")

camCommand_client.connect(("192.168.254.120", 6667))##########################
print("Camera commands connected.\r\n")

f = open("AcqStat.txt",'w')
f.write("1")
f.close()

subprocess.Popen(['python',"ABBA_Camera_Script.py"])

realign_time = 10*60
positions_arr = positions_base + positions_base_2 # Establishes a search pattern using the basis

acqAnother = input("Enter 0 to exit, otherwise acquire:")
set_time = time.time()
while (acqAnother != '0'):
    for position in positions_arr:
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

        recvSignal = 1

        camComm_buffer = ''

        time.sleep(0.5)
    cumultime = time.time()
    if ((cumultime - set_time) > realign_time):
        camComm_buffer = '1'
        camComm_buffer += str(return_pos)

        try:
            camCommand_client.send(camComm_buffer.encode())
        except:
            break

        try:
            camComm_buffer = camCommand_client.recv(1024).decode()
        except:
            break

        acqAnother = input("Enter 0 to exit, otherwise acquire:")
        set_time = time.time()

print("ABBA scan complete.\r\n")

f = open("AcqStat.txt",'w')
f.write("-1")
f.close()

try:
    camCommand_client.shutdown(socket.SHUT_RDWR)
except:
    pass

print("Socket close operation complete.\r\n")