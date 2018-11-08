from tkinter import *
from tkinter import messagebox # Used for tkinter popups
from tkinter import filedialog # Used for file dialog operations
import paramiko as p # Used for SSH
import time # Used for delays
import unicodedata # Used to filter non-printable characters out of strings
import os
import ctypes
WorkDir = os.getcwd() # Gather current working directory

# Control Character Removal Tool ##################################
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
###################################################################

# File Names ######################################################
selffile = "\PyPianobarContr_v2.pyw"
remParams = "\RemoteParams.txt"
Plog = "\Plog.txt"

###################################################################

# SSH Parameters ##################################################
# Load from file
with open(WorkDir + remParams) as fp:
    for i, line in enumerate(fp):
        line = remove_control_characters(line)
        if i == 7: # 8th line - IP
            server    = str(line)
        elif i == 8: # 9th line - username
            username  = str(line)
        elif i == 9: # 10th line - password
            password  = str(line)
        elif i == 10: # 11th line - Remote Log directory
            remoteLog = str(line)
        elif i > 10:
            break

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
def open_local_file( fname ):
    # Open a local file for editing by user
    file = WorkDir + fname
    os.startfile(file)

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

def write(textstr,color=False):
    text.insert(END, textstr + "\n")
    if (color != False):
        ind = text.index(END)
        start = float(ind) - 2
        strlen = len(textstr)
        stop = start + strlen/10
        text.tag_add("color", str(start), str(stop))
        text.tag_config("color", foreground = color)

def mainTask():
    command = ">" + remoteLog
    try:
        sftp.get( remoteLog, WorkDir+Plog )
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( command )
    except:
        write("FTP ERROR!!!","red")
    with open(WorkDir+Plog) as f:
        for line in f:
            line = remove_control_characters( line )
            if (line.find("2KTIME") == -1):
                line = line[3:]
                write(line,"cyan")
    
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
text = Text(termframe, bg="black",fg="green2",width=100,wrap=WORD)
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
    write("SSH Connection Failed!","red")
    gui.update()
    resp = messagebox.askquestion("Pianobar Control", "An error occurred "+
                                  "while trying to make SSH connection.\n"+
                                  "Check network and try again.\n\n"+
                                  "Would you like to edit your server config. "+
                                  "file to attempt fixing the issue?")
    if resp == 'yes':
        open_local_file( remParams )
        resp = messagebox.askquestion("Pianobar Control", "Would you like to " +
                                      "attempt restarting with the updated " +
                                      "configuration file?")
        if resp == 'yes':
            messagebox.showinfo("Pianobar Control","Sorry, that's not available now.")
    gui.destroy()
    sys.exit()
###################################################################

# Iteratively perform the main task and update the Tkinter Window
gui.after(10, mainTask)
gui.mainloop()
