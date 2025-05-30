; Task: Custom launcher for VALORANT
; Description: This script acts as a dedicated game launcher for VALORANT to handle pre-launch and post-launch actions. Recommended for systems using Stardock Groupy or Rainmeter skins, as VALORANT may not start without disabling them first. 

; Permissions: None
; Dependencies: Stardock Groupy and Rainmeter installed

; Usage: Press `F12` to kill Riot Client Services after game exit.

; --------------------------------------------------

; System metadata for executable
;@Ahk2Exe-SetVersion 1.0.0
;@Ahk2Exe-SetName Riot Launcher
;@Ahk2Exe-SetDescription Riot Launcher
;@Ahk2Exe-SetOrigFilename RiotLauncher.exe

; Initialization
#Requires AutoHotkey v2.0
#SingleInstance Force

; Check for Admin privileges
if not A_IsAdmin {
    if A_IsCompiled {
        Run '*RunAs "' A_ScriptFullPath '" /restart'
    }
    else {
        Run '*RunAs "' A_AhkPath '" /restart "' A_ScriptFullPath '"'
    }
}

; Hotkey for Panic button
F3::Send "!{Tab}"

; Hotkey for closing Riot Client Services
F12::ProcessClose "RiotClientServices.exe"

; Disable Groupy
Run 'net stop "Groupy"', , "Hide"
Run '"C:\Program Files (x86)\Stardock\Groupy\GroupyCtrl.exe" unload'

; Disable Rainmeter
ProcessClose "rainmeter.exe"

; Start VALORANT
Run 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\VALORANT.lnk'

; Wait for game shutdown
ProcessWaitClose "RiotClientServices.exe"

; Restart explorer
ProcessClose("Explorer.exe")

; Enable Rainmeter
Run 'C:\Program Files\Rainmeter\Rainmeter.exe'

; Enable Groupy
Run 'net start "Groupy"', , "Hide"

; Exit the launcher
ExitApp
