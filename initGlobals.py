'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

------------------------
Global Variable Declaration
------------------------

Loaded from the BaseStats object in Level1 scene once when the game loads.

'''

import GameLogic as G

def init():
    # Scripts.py -> CarInit() updates this every frame.
    # uiScripts.py -> readMySpeed() reads it every 2 frames, called from speedo object in HUD scene.
    G.mySpeed = 0.0

    # Tracking Turbo state (for logic and sharing with UI)
    G.turboActive = False
    G.turboCooldown = False
    G.turboDurTimerUI = "Joe"
    G.turboCoolTimerUI = "Suzy"

    # Tracking Glide state (for UI only)
    G.glideCooldownTimer = 0.0
    G.glideCooldown = 0
    G.activeShape = 1

