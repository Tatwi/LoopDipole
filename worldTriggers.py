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


# Define objects for use in this script
def main():
    logic.scene = logic.getCurrentScene()
    logic.car = logic.scene.objects["bare"]

# Run the main function
main()
