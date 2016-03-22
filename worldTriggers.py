'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

---------------------
World Triggers
---------------------

Functionality for objects in the world that do things when the player interacts with them.
This does not include: Corner Triggers, Chaoties (Enemies), or Fountains (Puzzles).

'''

from bge import constraints
from bge import logic
from bge import events
from bge import render as r
import math
from random import randint
import GameLogic as G
# Allow use of functions in the script.py file
import scripts


# Toss the player a good distance, based on their current speed.
# Called by collision with player at bottom the ski jump on the orange level.
# Logic Brick creates SkiJumpEnd object and parents to player.
# While jumping, the turbo and gliding are disabled.
def skiJumpStart():
    logic.car["skiJumping"] = True
    logic.car["limitMaxVelocity"] = False
    logic.car.linVelocityMax = 5001
    logic.car.linearVelocity[1] += 50
    logic.car.linearVelocity[2] += 33


# Called by SkiJumpEnd object when it hits something (namely the ground).
def skiJumpEnd():
    logic.car.linVelocityMax = logic.car["myLinVelocityMax"]
    logic.car["limitMaxVelocity"] = True
    logic.car["skiJumping"] = False


# Possibly send player to one of 3 locations
def teleporterTV():
    rng = randint(1,100)
    if rng < 33:
        logic.car.actuators["Explosion"].startSound()
    else:
        if rng > 85:
            # Purple level, left eye, going East
            scripts.teleport(240.0, 840.0, 226.0, 1)
        elif rng > 60:
            # Blue level, going South
            scripts.teleport(-942.0, 1436.0, 201.0, 2)
        elif rng > 32:
            # Yellow level, right foot, going West
            scripts.teleport(-356.13, -1071.5, 101.0, 3)


# Single desitination portal. Called by Portal objects on collision with player.
# Destination stored in the object.
def portal():
    cont = logic.getCurrentController()
    scripts.teleport(cont.owner["x"], cont.owner["y"], cont.owner["z"], cont.owner["heading"])


# Define objects for use in this script
def main():
    logic.scene = logic.getCurrentScene()
    logic.car = logic.scene.objects["bare"]

# Run the main function
main()
