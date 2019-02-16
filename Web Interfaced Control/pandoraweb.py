#########################################################################################
# Python Bottle Web Application
# Used for interfacing with Pianobar Pandora-Client on a Raspberry Pi.
# Written by Joe Stanley
# (c) Stanley Solutions
#########################################################################################

import os

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname('/home/pi/pandoraweb/pandoraweb.py'))

from bottle import route, run, template, get, post, Bottle
from bottle import request, error, static_file, redirect

# Define Webpage Parameters
IP = '192.168.1.6'
PORT = '8080'
HTMLdir = "/home/pi/pandoraweb"
IMGdir = "/home/pi/pandoraweb/Images"

Webapp = Bottle()

# Define and route Static Files (Images):
@Webapp.route('/settings/<filename>')
@Webapp.route('/setting/<filename>')
@Webapp.route('/index/<filename>')
@Webapp.route('/<filename>')
def server_static(filename):
	return(static_file(filename, root=IMGdir))

# Define Pages:
def home(songinfo):
	return( template("index.tpl", {'songinfo':songinfo}, root=HTMLdir) )
def settings(songinfo):
	return( template("settings.tpl", {'songinfo':songinfo}, root=HTMLdir ) )

# Define Terminal Interaction Function
def cmd( command ):
	# Send command to Terminal
	os.system( command )

# Define Pianobar Control Function:
def pianobar( command ):
	# Generate Command String
	command = "echo '" + command + "' >> /home/pi/.config/pianobar/ctl"
	# Send command to Terminal
	cmd( command )

# Define Generic GET-Based Homepage-Load:
@Webapp.route('/index')
@Webapp.route('/')
def index():
	return( home("Not Currently Available") )

# Define Generic GET-Based Settings-Load:
@Webapp.route('/settings')
@Webapp.route('/setting')
def settingspage():
	return( settings( "Not Currently Available" ) )

# Define Control-Based Function
@Webapp.post('/index')
@Webapp.post('/')
def home_control():
	playpauseid   = request.forms.get('playpause')
	skipid        = request.forms.get('skip')
	settingid     = request.forms.get('settings')
	stationlistid = request.forms.get('stationlist')
	vdownid       = request.forms.get('vdown')
	vupid         = request.forms.get('vup')
	thumbdownid   = request.forms.get('thumb_down')
	thumbupid     = request.forms.get('thumb_up')
	tiredid       = request.forms.get('tired')
	
	# Send Pianobar command as necessary
	if(playpauseid!=None):		pianobar("p")
	elif(skipid!=None):			pianobar("n")
	elif(vdownid!=None):		pianobar("(((((")
	elif(vupid!=None):			pianobar(")))))")
	elif(thumbdownid!=None):	pianobar("-")
	elif(thumbupid!=None):		pianobar("+")
	elif(tiredid!=None):		pianobar("t")
	
	# Change page as necessary
	if(settingid!=None):
		redirect("/setting")
	elif(stationlistid!=None):
		redirect("/stations")
	else:
		return(home("Not Currently Available"))

@Webapp.post('/settings')
@Webapp.post('/setting')
def setting_control():
	returnid      = request.forms.get('return')
	playpauseid   = request.forms.get('playpause')
	start         = request.forms.get('start')
	stop          = request.forms.get('stop')
	# Start Pianobar when Needed
	if(start!=None):
		cmd( "nohup pianobar > pianobar.out 2>&1 &" )
	# Quit Pianobar when Needed
	if(stop!=None):
		pianobar( "q" )
	# When asked to play or pause, do so
	if(playpauseid!=None):
		return(settings("Not Currently Available"))
	else:
		redirect("/")

@Webapp.error(404)
def error404(error):
    return( template("404err.tpl", root=HTMLdir ) )

# Run the Server
Webapp.run(host=IP, port=PORT, reloader=True)
