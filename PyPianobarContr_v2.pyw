from tkinter import *
from tkinter import messagebox
import paramiko as p
import time
import os
import ctypes
WorkDir = os.getcwd()

# SSH Parameters ##################################################
server   = "192.168.1.10"
username = "pi"
password = "Lionel2truck"
# Pianobar Control Character Strings
nxt      = "n"
plps     = " "
vup      = "))))"
vdn      = "((((("
thmup    = "+"
thmdn    = "-"
qut      = "q"
tsong    = "t"
###################################################################

# Functions #######################################################
def sendCMD(cmd):
    command = "echo '"+cmd+"' >> /home/pi/.config/pianobar/ctl"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( command )

def playpause():
    sendCMD(plps)

def skip():
    sendCMD(nxt)

def volup():
    sendCMD(vup)

def voldn():
    sendCMD(vdn)

def like():
    sendCMD(thmup)

def ulike():
    sendCMD(thmdn)

def tired():
    sendCMD(tsong)

def quitPandora():
    sendCMD(qut)

def spclCommand():
    cmdStr = spclStr.get()
    sendCMD(cmdStr)

# GUI Initialization ##############################################
gui = Tk()
gui.title("  Pianobar Pandora Client Control")
spclStr = StringVar()
myappid = 'Stanley Solutions.Python Pandora Control.GUI.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
###################################################################

# Gather Images ###################################################
ptextimg = PhotoImage(file=WorkDir+"/Images/PANDORA.png")
Plogoimg = PhotoImage(file=WorkDir+"/Images/PandoraP.png")
playimg  = PhotoImage(file=WorkDir+"/Images/PlayPause.png")
skipimg  = PhotoImage(file=WorkDir+"/Images/Skip.png")
thdnimg  = PhotoImage(file=WorkDir+"/Images/ThumbDwn.png")
thupimg  = PhotoImage(file=WorkDir+"/Images/ThumbUp.png")
volupimg = PhotoImage(file=WorkDir+"/Images/VolUp.png")
voldnimg = PhotoImage(file=WorkDir+"/Images/VolDwn.png")
###################################################################

# GUI Setup #######################################################
# Frames
masterframe = Frame(gui,bg="white")
masterframe.pack()
headframe = Frame(masterframe,bg="white")
headframe.pack( side = TOP )
Pframe = Frame(headframe,bg="white")
Pframe.pack(side=LEFT)
contframe = Frame(headframe,bg="white")
contframe.pack(side=RIGHT)
sp1frame = Frame(headframe,bg="white",width=10)
sp1frame.pack(side=LEFT)
updnframe = Frame(headframe,bg="white")
updnframe.pack(side=LEFT)
sp2frame = Frame(headframe,bg="white",width=10)
sp2frame.pack(side=LEFT)
termframe = Frame(masterframe)
termframe.pack( side = BOTTOM )
# Images and Icons
gui.iconbitmap(WorkDir + "/Images/PandoraP.ico")
pandoraP = Label(Pframe, image=Plogoimg).pack()
# Buttons
playbtn = Button(contframe, image=playimg, width=300, bg="white",
                 activebackground="white", command = playpause).pack(side=TOP)
nextbtn = Button(contframe, image=skipimg, width=300, bg="white",
                 activebackground="white", command = skip).pack(side=TOP)
volupbtn = Button(updnframe, image=volupimg, width=75, bg="white",
                 activebackground="white", command = volup).pack(side=TOP)
volupbtn = Button(updnframe, image=voldnimg, width=75, bg="white",
                 activebackground="white", command = voldn).pack(side=BOTTOM)
thmupbtn = Button(updnframe, image=thupimg, width=75, bg="white",
                  activebackground="white", command=like).pack(side=LEFT)
thmdnbtn = Button(updnframe, image=thdnimg, width=75, bg="white",
                  activebackground="white", command=ulike).pack(side=RIGHT)
tierdbtn = Button(updnframe, text="Tired", padx=20, pady=10, bg="white",
                  activebackground="white", command=tired).pack()
quitbtn = Button(contframe, text="Close Pianobar Pandora Client", bg="white", padx=20,
                 activebackground="white", command = quitPandora).pack(side=BOTTOM)
spclbtn = Button(contframe, text="Send Command to Pianobar:", padx=6, bg="white",
                 activebackground="white", command = spclCommand).pack(side=LEFT)
# Terminal/Printout Display
text = Text(termframe, bg="black",fg="green2",width=100)
text.pack()
# Special Command Entry
spclEntry = Entry(contframe, textvariable=spclStr, bg="white", bd=5).pack(side=LEFT)
####################################################################

# SSH Initialization ##############################################
try:
    # Print status information for user
    text.insert(END, "Attempting SSH Connection to Pianobar Server...\n")
    gui.update()
    # Try starting control SSH
    ssh = p.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(p.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    # Print status information for user
    text.insert(END, "SSH Connection Established Successfully!\n")
except TimeoutError:
    # If failure, indicate to user
    text.insert(END, "SSH Connection Failed!")
    gui.update()
    messagebox.showinfo("Pianobar Control", "An error occurred "+
                        "while trying to make SSH connection.\n"+
                        "Check network and try again.")
    gui.destroy()
    sys.exit()
###################################################################

gui.mainloop()
