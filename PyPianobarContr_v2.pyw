from tkinter import *
from tkinter import messagebox # Used for tkinter popups
from tkinter import filedialog # Used for file dialog operations
import paramiko as p # Used for SSH
import time # Used for delays
import os
import ctypes
WorkDir = os.getcwd() # Gather current working directory

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

# GUI Initialization ##############################################
gui = Tk()
gui.title("  Pianobar Pandora Client Control")
spclStr = StringVar()
myappid = 'Stanley Solutions.Python Pandora Control.GUI.2'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
###################################################################

# Functions #######################################################
def on_closing():
    sftp.close() # Close SSH FTP connection on quit
    ssh.close() # Close SSH Connection on quit
    gui.destroy() # Destroy gui window and quit program
    
def sendCMD(cmd):
    # Create string necessary to send information to fifo
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

def startPandora():
    # Use "nohup" to prevent closing when this script closes
    command = "nohup pianobar > pianobar.out 2>&1"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( command )

def saveLogasName():
    gui.filename = filedialog.asksaveasfilename(initialdir = WorkDir,
            title = "Save Pandora Log File as",
            filetypes = (("text file","*.txt"),("all files","*.*")))
    print(gui.filename)

def mainTask():
##    print("hi there")
##    print(sftp.getcwd())
##    sftp.chdir("/home/pi")
##    print(sftp.getcwd())
##    print(sftp.listdir())
##    print(sftp.lstat("pianobar.out"))
##    sftp.get( WorkDir+"\Plog.txt", "pianobar.out" )
    
    gui.after(5000, mainTask) # Reschedule main task
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
spclbtn = Button(contframe, text="Send Command to Pianobar:", padx=6, bg="white",
                 activebackground="white", command = spclCommand).pack(side=LEFT)
# Menu
menubar = Menu( gui )
filemenu = Menu(menubar,tearoff = 0)
filemenu.add_command(label = "Save Pandora Log As", command = saveLogasName)
menubar.add_cascade(label = "File", menu = filemenu)
conmenu = Menu(menubar, tearoff = 0)
conmenu.add_command(label = "Start Pianobar", command = startPandora)
conmenu.add_command(label = "Quit Pianobar", command = quitPandora)
menubar.add_cascade(label = "Pandora", menu = conmenu)
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
    gui.protocol("WM_DELETE_WINDOW", on_closing)
    gui.config( menu = menubar )
    gui.update()
    # Try starting control SSH
    ssh = p.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(p.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    # Try starting SSH File Transfer System
    sftp = ssh.open_sftp()
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

# Iteratively perform the main task and update the Tkinter Window
gui.after(10, mainTask)
gui.mainloop()
