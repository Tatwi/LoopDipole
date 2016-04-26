'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

------------------------
User Interface Scripts
------------------------

Functions for the general interface.

'''

import Rasterizer
import GameLogic as G
import bge
from bge import logic

def showMouse():
    Rasterizer.showMouse(1);

def hideMouse():
    Rasterizer.showMouse(0);

# Speedometer is based on bare object's linear velocity, but it was tuned to match the speed read by the rotation of the wheels.
# Tried to make the speed values feel as close to real life as I could. :)
# Rough math...
# Muscle Car Shape is roughly a coupe muscle car and they average around 180in = 4.572 meters
# 1 square of world lines approx = 2.5 Muscle Car lengths = 11.43m
# Traveled 5 squares in 11.5 seconds (at what showed as 6.2158).
# 5 squares x 11.43m = 57.15m
# 57.15m / 11.5 seconds = 4.97m/s = 17.89 kilometers/hour
# 17.89Km/h actual / 6.2158Km/h showing = of by a factor of 2.8781
# Already had increased by 1.4, so proper "fudge factor" should be 4.2781!
# Test... game said 18.9943 with a feelSpeed of 4.2781, so over estimate, but close.
# Adjustments found that feelSpeed "fudge factor" of 4.03 gives 17.89 Km/h and that's close enough for me!
def readMySpeed():
    cont = logic.getCurrentController()

    wheelSpeed = G.mySpeed / 1.5
    feelSpeed = wheelSpeed * 4.03
    mph = abs(int(feelSpeed))
    kph = abs(int(feelSpeed * 1.609344))
    if cont.owner["KPH"] == True:
        cont.owner["Text"] = kph
    else:
        cont.owner["Text"] = mph


# Display Turbo State (Ready, On, Charging)
def displayTurboStatus():
    cont = logic.getCurrentController()

    if G.turboCooldown == True:
        cont.owner["Text"] = "Turbo: Charging (" + G.turboCoolTimerUI + ")"
    elif G.turboActive == True:
        cont.owner["Text"] = "Turbo: Running (" + G.turboDurTimerUI + ")"
    else:
        cont.owner["Text"] = "Turbo: Ready"


# Show button when player presses turbo key
# Both are toggled off with logic bricks on key release
def turboButtonToggle():
    scene = logic.getCurrentScene()

    if G.turboCooldown == True:
        scene.objects["TurboButtonOn"].setVisible(False)
        scene.objects["TurboButtonOff"].setVisible(True)
    else:
        scene.objects["TurboButtonOff"].setVisible(False)
        scene.objects["TurboButtonOn"].setVisible(True)


# Display Glide State
# Air Gliding: cooldown starts after landing.
# Ribbon Gliding: Either on or off, no cooldown.
def displayGlideStatus():
    cont = logic.getCurrentController()

    countDif = G.glideCooldown - G.glideCooldownTimer
    timerStr = str(int(countDif))
    if G.activeShape < 5:
        # Air Gliding
        if countDif < 0:
            cont.owner["Text"] = "Glide: Ready"
        elif int(G.glideCooldownTimer) == 0:
            cont.owner["Text"] = "Gliding"
        elif countDif > 0:
            cont.owner["Text"] = "Glide: Charging (" + timerStr + ")"
    else:
        # Ribbon Gliding
        if G.cornerAssist == False:
            cont.owner["Text"] = "Glide: Off"
        elif G.cornerAssist == True:
            cont.owner["Text"] = "Glide: On"


###############
# Menu Screens
###############

# Find the max screen height
# start.blend is set to start at the desktop resolution by default, so each time it 
# loads it saves the desktop height, then changes to the resolution saved in settings.
def maxDesktopHeight():
    cont = logic.getCurrentController()
    rend = bge.render
    cont.owner["desktopHeight"] = rend.getWindowHeight()


# Displays the current resolution on the settings screen.
def displayResolution():
    cont = logic.getCurrentController()
    rend = bge.render
    width = rend.getWindowWidth()
    height = rend.getWindowHeight()
    cont.owner["Text"] = "(" + str(width) + "x" + str(height) + ")"


# Set Resolution
# Values saved in Button.SettingsApply object in start.blend file
def setResolution():
    cont = logic.getCurrentController()
    own = cont.owner
    rend = bge.render
    
    scene = logic.getCurrentScene()
    settings = scene.objects["Controller"]
    
    if own["height"] > settings["desktopHeight"]:
        # Prevent crash by not allowing resolution to be greater than the screen can use.
        rend.setWindowSize(800, 600)
        warning = scene.objects["WarningSpawn"]
        warning.actuators["Resolution"].instantAddObject()
        return
    else:
        rend.setWindowSize( own["width"], own["height"])
    
    
# Select Resolution
# Values saved in Button.SettingsApply object in start.blend file
# Called from settings menu when player clicks a resolution
def selectResolution():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()
    settings = scene.objects["Button.SettingsApply"]
    settings["width"] = own["width"]
    settings["height"] = own["height"]
    
    scene.objects["Button.Res1"].setVisible(False)
    scene.objects["Button.Res2"].setVisible(False)
    scene.objects["Button.Res3"].setVisible(False)
    scene.objects["Button.Res4"].setVisible(False)
    scene.objects["Button.Res5"].setVisible(False)
    scene.objects["Button.Res6"].setVisible(False)
    own.setVisible(True)


def profileOver():
    cont = logic.getCurrentController()
    own = cont.owner
    
    mouse = cont.sensors["Over"]
    status = mouse.status
    mouseTarget = mouse.hitObject
    
    if status == 1 or own["selected"] == True:
        # Mouse over or selected
        own.setVisible(True)
    elif status == 3:
        # Mouse out
        own.setVisible(False)
        own["selected"] = False
        
def profileClick():
    cont = logic.getCurrentController()
    own = cont.owner
    scene = logic.getCurrentScene()
    
    mouseOver = cont.sensors["Over"]
    statusOver = mouseOver.status
    mouseTarget = mouseOver.hitObject
    
    mouseClick = cont.sensors["Over"]
    statusClick = mouseClick.status
    
    # Set selected profile on click
    if statusClick == 2 and mouseTarget == own:
        playButton = scene.objects["Button.Play"]
        playButton["profile"] = own["profile"]
        own["selected"] = True
        
        # Deselect other profile
        if own["profile"] != 1:
            profile1 = scene.objects["Button.Profile1"]
            profile1["selected"] = False
            profile1.setVisible(False)
        if own["profile"] != 2:
            profile2 = scene.objects["Button.Profile2"]
            profile2["selected"] = False
            profile2.setVisible(False)
        if own["profile"] != 3:
            profile3 = scene.objects["Button.Profile3"]
            profile3["selected"] = False
            profile3.setVisible(False)
        if own["profile"] != 4:
            profile4 = scene.objects["Button.Profile4"]
            profile4["selected"] = False
            profile4.setVisible(False)
    

    
