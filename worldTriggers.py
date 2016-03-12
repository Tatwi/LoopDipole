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
        logic.car.setLinearVelocity([0.0,0.0,0.0],1)
        if rng > 85:
            # Purple level, left eye
            logic.car.position = (98.0, 870.0, 231.0)
        elif rng > 60:
            # Blue level
            logic.car.position = (-995, 961, 206.0)
        elif rng > 32:
            # Yellow level, right foot
            logic.car.position = (-980, -1077, 106.0)

        teleportSound = logic.scene.objects["Controller"].actuators["Load In"]
        teleportSound.startSound()


# Define objects for use in this script
def main():
    logic.scene = logic.getCurrentScene()
    logic.car = logic.scene.objects["bare"]

# Run the main function
main()
