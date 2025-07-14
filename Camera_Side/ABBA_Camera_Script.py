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
    USER_INP = 7 #9 if 22 #7.75 # 6.75 #15 seconds, based on 1us dwell, 41s for 6us, 4int

    hFoundWnd = FocusTheDesiredWnd()

    f = open("AcqStat.txt",'r')
    statLine = f.readline()
    f.close()
    
    while (statLine != "-1"):
        f = open("AcqStat.txt",'r')
        statLine = f.readline()
        f.close()

        if (statLine == "2"):
            hFoundWnd = FocusTheDesiredWnd()
            f = open("AcqStat.txt",'w')
            f.write("1")
            f.close()

        if (statLine == "0"):
            # Pump-Probe
            PressKey('{VK_F6}')

            time.sleep(USER_INP)

            PressKey('^s')

            f = open("AcqStat.txt",'w')
            f.write("1")
            f.close()

        time.sleep(0.1)

if __name__ == '__main__':
    main(sys.argv)