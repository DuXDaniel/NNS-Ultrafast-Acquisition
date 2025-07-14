import sys
import pywinauto
import time
        
def PressKey(keypress):
    ###### Press on keyboard the passed request
    pywinauto.keyboard.send_keys(keypress,pause=0.01)

def FocusTheDesiredWnd():
    searchApp = pywinauto.application.Application()
    try:
        searchApp.connect(title_re=r'.*xT microscope Control.*', found_index = 0)
        
        restoreApp = searchApp.top_window()
        restoreApp.minimize()
        restoreApp.restore()
        restoreApp.set_focus()
        return restoreApp
    except:
        return 0

def main(argv):
    USER_INP = 3.75 #15 seconds, based on 1us dwell, 41s for 6us, 4int

    hFoundWnd = FocusTheDesiredWnd()

    f = open("AcqStat.txt",'r')
    statLine = f.readline()
    f.close()

    timeout = 60 # seconds to attempt window focusing before a timeout command is sent

    timeout_start = 0
    timeout_cond = 0
    
    while (statLine != "-1"):
        f = open("AcqStat.txt",'r')
        statLine = f.readline()
        f.close()

        if (statLine == "0"):
            hFoundWnd = FocusTheDesiredWnd()
            if(hFoundWnd != 0):
                timeout_cond = 0

                # Pump-Probe
                PressKey('{VK_F6}')

                time.sleep(USER_INP)

                PressKey('^s')

                f = open("AcqStat.txt",'w')
                f.write("1")
                f.close()
            else:
                if (timeout_cond == 0):
                    timeout_cond = 1
                    timeout_start = time.time()
                    print('Timer has begun on timeout.')

                if (time.time() - timeout_start > timeout):
                    print('Failed to find microscope window.')
                    f = open("AcqStat.txt",'w')
                    f.write("-1")
                    f.close()
                    statLine = "-1"

        time.sleep(0.5)

if __name__ == '__main__':
    main(sys.argv)