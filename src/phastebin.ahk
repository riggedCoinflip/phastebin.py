#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


;pastebin: use this if you prefer to use pastebin. Comment out the hastebin block
^+c::
Run, phastebin.py --copy pastebin
return

/*
;hastebin: use this if you prefer to use hastebin. Comment out the pastebin block
^+c::
Run, phastebin.py --copy hastebin
return
*/

^+v::
Run, phastebin.py --paste
return