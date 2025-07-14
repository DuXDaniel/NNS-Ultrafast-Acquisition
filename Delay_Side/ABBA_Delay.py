import time
import socket
import subprocess
import os.path as path

delayConnected = 0

# Update the user on beginning initialization
print("Initializing server...\r\n")

# standard server startup code -. search Berkeley sockets or c++ sockets for more information
commCamCommand_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

commCamCommand_server.bind(('',6667))

# Update the user on listening for the connection to the delay value client and run client
print("Listening for incoming connections on ports 6667...\r\n")

# Connect to the camera run status client
commCamCommand_server.listen(1)
commCamCommand, comCamCommand_addr = commCamCommand_server.accept()
print("Camera data communicating through" + str(comCamCommand_addr) + "\r\n")

subprocess.Popen(['python','DelayStageCommScript.py'])

print("Delay stage connected.\n")

delayConnected = 1

print("Initializing delay communication loop.\r\n")

keepScanRunThread = 1

while (keepScanRunThread == 1):
    print("Awaiting incoming data.\n")
    try:
        camComm_buffer = commCamCommand.recv(128).decode()
    except:
        keepScanRunThread == 0
        break

    if (camComm_buffer != '' and camComm_buffer[0] == '1'):
        rundel = 1
    else:
        rundel = 0

    if (rundel == 1):
        delaydata = camComm_buffer[1:]

        camComm_buffer = ''

        curDistPoint = delaydata

        print("Data received and moving delay stage to position " + delaydata + "\n")

        f = open('movementCommFile.txt','w')
        f.write(str(curDistPoint) + "\n")
        f.write("0")
        f.close()
        
        if (path.exists("movementCommFile.txt")):
            f = open("movementCommFile.txt","r")
            f.readline()
            completionStatus = f.readline()
            completionValue = int(completionStatus)

        while (completionValue != 1):
            if (path.exists("movementCommFile.txt")):
                f = open("movementCommFile.txt","r")
                f.readline()
                completionStatus = f.readline()
                try:
                    completionValue = int(completionStatus)
                except:
                    completionValue = 0

            time.sleep(0.25)

        camComm_buffer = '1'

        try:
            commCamCommand.send(camComm_buffer.encode())
        except:
            keepScanRunThread == 0
            break
        
        cc_buffer = ''

    time.sleep(0.25)

print("Server shutdown initiated.\r\n")

# Requires setting connect text file to "2"
f = open("connectStatFile.txt","w")
f.write("2")
f.close()

delayConnected = 0

try:
    commCamCommand_server.shutdown(socket.SHUT_RDWR)
except:
    pass