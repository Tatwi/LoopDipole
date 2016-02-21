'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

---------------------
Player Abilities
---------------------

Functions for player abilities

'''

## First, we import all the python modules
from bge import constraints
from bge import logic
from bge import events
from bge import render as r
import math


# Prevent laser bolts from shooting up into the air when driving
def levelLasers():
    em6 = logic.scene.objects["Emitter6"]
    em7 = logic.scene.objects["Emitter7"]
    logic.car = logic.scene.objects["bare"]
    ray = logic.car.sensors["groundRay"]

    # Always level out in case of issues
    player = logic.car.worldOrientation
    em6.worldOrientation = (player[0], player[1], [0.0, 0.0, 1.0])
    em7.worldOrientation = (player[0], player[1], [0.0, 0.0, 1.0])

    # Adjust to match angle of surface player is currently on
    if ray.positive:
        em6.alignAxisToVect(ray.hitNormal, 2, 1)
        em7.alignAxisToVect(ray.hitNormal, 2, 1)





# Inertial Reversal: Instantly go in the opposite direction without losing momentum.
# Implimented with Logic Bricks


# Collection Vortex (unfinished)
# Enlage Collector
def largeCollector():
    cont = logic.getCurrentController()
    owner = cont.owner

    owner.localScale.x = 2
    owner.localScale.z = 5
    owner.localPosition.z = 1
    owner["colTimer"] = 0

# Reset Collector
def normalCollector():
    cont = logic.getCurrentController()
    owner = cont.owner

    owner.localScale.x = 1
    owner.localScale.z = 1
    owner.localPosition.z = owner["homePos"]

