#########################################################################################
# Python Bottle Web Application
# Used for interfacing with Pianobar Pandora-Client on a Raspberry Pi.
# Written by Joe Stanley
# (c) Stanley Solutions
#########################################################################################

import os
from bottle import route, run, template, get, post, Bottle
from bottle import request, error, static_file

# Define Webpage Parameters
IP = 'localhost'
PORT = '80'
HTMLdir = "C:/Users/Joe Stanley/Desktop/pandoraweb/Web Interfaced Control"
IMGdir = "C:/Users/Joe Stanley/Desktop/pandoraweb/Web Interfaced Control/Images"

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

# Define OS Interaction Function
def cmd( command ):
	# Send command to OS
	x = 1

# Define Pianobar Control Function:
def pianobar( command ):
	# Generate Command String
	command = "something" + command + "more"
	# Send command to OS
	cmd( command )

# Define Generic GET-Based Homepage-Load:
@Webapp.route('/index')
@Webapp.route('/')
def index():
	return( home("test") )

# Define Generic GET-Based Settings-Load:
@Webapp.route('/settings')
@Webapp.route('/setting')
def settingspage():
	return( settings( "test" ) )

# Define Control-Based Function
@Webapp.post('/index')
@Webapp.post('/')
def home_control():
    playpause   = request.forms.get('playpause')
    skip        = request.forms.get('skip')
    print("I made it")
    print(playpause, skip)
    return(home("test"))

@Webapp.post('/settings')
@Webapp.post('/setting')
def setting_control():
	return(settings("test"))

@Webapp.error(404)
def error404(error):
    return("Sorry, that link or page seems to be unavailable.")

# Run the Server
Webapp.run(host=IP, port=PORT, reloader=True)
