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

