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



## Block Barrage: Throw some blocks ahead.
def blockBarrage():
    cont = logic.getCurrentController()
    obj = cont.owner
    
    # Get all the emitter actuators
    em1 = logic.scene.objects["Emitter1"]
    em1Acu = em1.actuators["Shoot"]
    em2 = logic.scene.objects["Emitter2"]
    em2Acu = em2.actuators["Shoot"]
    em3 = logic.scene.objects["Emitter3"]
    em3Acu = em3.actuators["Shoot"]
    em4 = logic.scene.objects["Emitter4"]
    em4Acu = em4.actuators["Shoot"]
    em5 = logic.scene.objects["Emitter5"]
    em5Acu = em5.actuators["Shoot"]
    
    # Shoot one block per emitter, X times
    for x in range(0, obj["barrage"]):
        em1Acu.instantAddObject()
        em2Acu.instantAddObject()
        em3Acu.instantAddObject()
        em4Acu.instantAddObject()
        em5Acu.instantAddObject()


## Inertial Reversal: Instantly go in the opposite direction without losing momentum.
# Implimented with Logic Bricks

