import time
import socket
import subprocess
import numpy as np

experiment_type = 3 # 0 for tuning, 1 for t0, 2 for ponderomotive

if experiment_type == 0:
    center_pos = -68.2
    return_pos = center_pos - 0.1
    positions_base = [-67]
    positions_base_2 = [-67]
elif experiment_type == 1:
    center_pos = -69.25
    return_pos = center_pos - 0.1 # -100 # 75

    #positions_base = [-116.5, -116.5, -114.5, -112.5, -110.5, -108.5, -106.5, -104.5, -102.5, -100.5, -98.5, -96.5, -94.5, -92.5, -90.5, -88.5, -86.5, -84.5, -82.5, -81.5, -68.0, -60.5, -16.5]
    #positions_base_2 = [-16.5, -60.5, -68.0, -81.5, -82.5, -84.5, -86.5, -88.5, -90.5, -92.5, -94.5, -96.5, -98.5, -100.5, -102.5, -104.5, -106.5, -108.5, -110.5, -112.5, -114.5, -116.5, -116.5]
    center_list_p = list(np.arange(center_pos-2,center_pos+1.95,0.5))
    left_list_p = list(np.arange(center_pos-15,center_pos-2.05,1))
    right_list_p = list(np.arange(center_pos+2,center_pos+5.95,1)) + [center_pos+6]
    positions_base = [center_pos-50,center_pos-50,center_pos-30] + left_list_p + center_list_p + right_list_p + [center_pos+30,center_pos+50]

    center_list_n = list(np.arange(center_pos+2,center_pos-1.95, -0.5))
    left_list_n = list(np.arange(center_pos+6, center_pos+2.05, -1))
    right_list_n = list(np.arange(center_pos-2, center_pos-14.95, -1)) + [center_pos-15]
    positions_base_2 = [center_pos+50, center_pos+30] + left_list_n + center_list_n + right_list_n + [center_pos-30, center_pos-50, center_pos-50]
elif experiment_type == 2:
    center_pos = -85.25
    return_pos = center_pos - 10 + 0.1
    left_pos_p = list(np.arange(center_pos-3,center_pos-0.01,0.2))
    right_pos_p = list(np.arange(center_pos,center_pos+2.99,0.2))
    positions_base = [return_pos - 0.1] + [return_pos - 0.1] + left_pos_p + right_pos_p + [center_pos+3]
    #positions_base = [return_pos-0.1] + [return_pos-0.1] + [-71.75, -70.25, -68.75, -67.25, -65.75]
    #positions_base = [return_pos - 0.1] + [return_pos - 0.1] + [-70.25]

    left_pos_n = list(np.arange(center_pos+3,center_pos+0.01,-0.2))
    right_pos_n = list(np.arange(center_pos,center_pos-2.99,-0.2))
    positions_base_2 = left_pos_n + right_pos_n + [center_pos-3] + [return_pos - 0.1] + [return_pos - 0.1]
    #positions_base_2 = [-65.75, -67.25, -68.75, -70.25, -71.75] + [return_pos-0.1] + [return_pos-0.1]
    #positions_base_2 = [-70.25] + [return_pos - 0.1] + [return_pos - 0.1]
elif experiment_type == 3:
    center_pos = -69.25
    return_pos = center_pos - 0.1 # -100 # 75

    #positions_base = [-116.5, -116.5, -114.5, -112.5, -110.5, -108.5, -106.5, -104.5, -102.5, -100.5, -98.5, -96.5, -94.5, -92.5, -90.5, -88.5, -86.5, -84.5, -82.5, -81.5, -68.0, -60.5, -16.5]
    #positions_base_2 = [-16.5, -60.5, -68.0, -81.5, -82.5, -84.5, -86.5, -88.5, -90.5, -92.5, -94.5, -96.5, -98.5, -100.5, -102.5, -104.5, -106.5, -108.5, -110.5, -112.5, -114.5, -116.5, -116.5]
    center_list_p = list(np.arange(center_pos-10, center_pos+29.95,2.5)) + [center_pos+30]
    positions_base = [center_pos-100,center_pos-100,center_pos-50] + center_list_p + [center_pos+60,center_pos+100]

    center_list_n = list(np.arange(center_pos+30,center_pos-9.95, -2.5)) + [center_pos-10]
    positions_base_2 = [center_pos+100, center_pos+60] + center_list_n + [center_pos-50, center_pos-100, center_pos-100]

print(positions_base)
print(len(positions_base))
print(positions_base_2)
print(len(positions_base_2))
camCommand_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Searching for connection.\r\n")

camCommand_client.connect(("192.168.254.120", 6667))##########################
print("Camera commands connected.\r\n")

f = open("AcqStat.txt",'w')
f.write("1")
f.close()

if experiment_type == 1 or experiment_type == 2 or experiment_type == 3:
    realign_time = 20*60
else:
    realign_time = 1*60
#positions_arr = positions_base + positions_base_2 Establishes a search pattern using the basis
cur_type = 1

acqAnother = input("Enter 0 to exit, otherwise acquire:")
subprocess.Popen(['python',"ABBA_Camera_Script.py"])
set_time = time.time()
count = 0
while (acqAnother != '0'):
    if (cur_type == 1):
        cur_pos_arr = positions_base
        cur_type = 2
    else:
        cur_pos_arr = positions_base_2
        cur_type = 1

    for position in cur_pos_arr:
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
            time.sleep(0.25)

        recvSignal = 1

        camComm_buffer = ''

        time.sleep(0.25)
    
    count = count + 1
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

        print(count)
        count = 0
        acqAnother = input("Enter 0 to exit, otherwise acquire:")
        if acqAnother != "0":
            f = open("AcqStat.txt","w")
            f.write('2')
            f.close()
            time.sleep(0.25)
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