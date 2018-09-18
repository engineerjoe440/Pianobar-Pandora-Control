' Pianobar AutoStartup VBScript
' Written by Joe Stanley 12/4/2017

' This script automtically starts Pianboar given a specified directory.

Dim oShell
Set oShell = WScript.CreateObject ("WScript.Shell")

' Specified Pianobar directory
directory = """C:\Program Files\Pianobar\pianobar.exe"""

' Wait for Windows to load and settle down.
oShell.Popup "Waiting 5 seconds...", 5, "Pianobar Message"

' Open pianobar.exe
oShell.run(directory), 1, false

' Play Pandora Quickmix
WScript.Sleep 3000
oShell.SendKeys "q"
oShell.SendKeys "{ENTER}"

' Print notification message.
oShell.Popup "Started Pianobar Successfully.", 1, "Pianobar Message"