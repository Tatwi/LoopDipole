'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

---------------------
Player Movement
---------------------

The player is based on the "car" from the vehicle physics demo, which has a whack of C++ dedicated
to simulating vehicle physics. I've modified it to handle how I would like and I have added extra
functionality, such as jumping, gliding, turbo speed, and mouse controls.

'''

# #############################
# Vehicle Physics Demo
# #############################
# This file is part of the book:
# "Game Development with Blender"
# by Dalai Felinto and Mike Pan
#
# Published by "CENGAGE Learning" in 2013
#
# You are free to use-it, modify it and redistribute
# as long as you keep the original credits when pertinent.
#
# File tested with Blender 2.66
#
# Copyright - February 2013
# This work is licensed under the Creative Commons
# Attribution-Share Alike 3.0 Unported License
# #############################

## First, we import all the python modules
from bge import constraints
from bge import logic
from bge import events
from bge import render as r
import math


## Set/Change the wheel stats in their own function
## because there are a load of them!
def setWheelStats():
    ## Apply handling stats to the (invisible) wheels
    vehicle = constraints.getVehicleConstraint(logic.car["cid"])
    ## Grab base stats from "BaseStats" object
    bstat = logic.scene.objects["BaseStats"]
    ## set vehicle roll tendency ##
    vehicle.setRollInfluence(bstat["influence"],0)
    vehicle.setRollInfluence(bstat["influence"],1)
    vehicle.setRollInfluence(bstat["influence"],2)
    vehicle.setRollInfluence(bstat["influence"],3)
    ## set vehicle suspension hardness ##
    vehicle.setSuspensionStiffness(bstat["stiffness"],0)
    vehicle.setSuspensionStiffness(bstat["stiffness"],1)
    vehicle.setSuspensionStiffness(bstat["stiffness"],2)
    vehicle.setSuspensionStiffness(bstat["stiffness"],3)
    ## set vehicle suspension dampness ##
    vehicle.setSuspensionDamping(bstat["damping"],0)
    vehicle.setSuspensionDamping(bstat["damping"],1)
    vehicle.setSuspensionDamping(bstat["damping"],2)
    vehicle.setSuspensionDamping(bstat["damping"],3)
    ## set vehicle suspension compression ratio ##
    vehicle.setSuspensionCompression(bstat["compression"],0)
    vehicle.setSuspensionCompression(bstat["compression"],1)
    vehicle.setSuspensionCompression(bstat["compression"],2)
    vehicle.setSuspensionCompression(bstat["compression"],3)
    ## set vehicle tire friction ##
    vehicle.setTyreFriction(bstat["friction"],0)
    vehicle.setTyreFriction(bstat["friction"],1)
    vehicle.setTyreFriction(bstat["friction"],2)
    vehicle.setTyreFriction(bstat["friction"],3)


# Reset stats when changing shapes
def resetStats():
    ## Max/Top Speed
    logic.car.linVelocityMax = 40

    ## Default Shape
    logic.car["activeShape"] = 1

    logic.car["accelNormal"] = -12.0
    logic.car["accelTurbo"] = -16.0
    logic.car["turboDur"] = 5.0
    logic.car["brakeForce"] = 15.0
    logic.car["steerAmount"] = 0.08

    logic.car["glideCooldown"] = 10
    logic.car["glideDur"] = 5
    logic.car["glideBonusY"] = 0.2
    logic.car["glideBonusZ"] = 0.2
    ## Lift impulse or "jump"
    logic.car["glideJumpY"] = 0.1
    logic.car["glideJumpZ"] = 0.43

    ## Base Stats
    bstat = logic.scene.objects["BaseStats"]
    bstat["influence"] = 0.01
    bstat["stiffness"] = 20.0
    bstat["damping"] = 2.0
    bstat["compression"] = 4.0
    bstat["friction"] = 10.0
    bstat["Stability"] = 0.1


## This is called from the object named "bare"
## is run once at the start of the game
def carInit():
    ## setup aliases for Blender API access ##
    cont = logic.getCurrentController()
    logic.scene = logic.getCurrentScene()
    logic.car  = cont.owner

    ## Grab base stats from "BaseStats" object
    bstat = logic.scene.objects["BaseStats"]

    ## Constants
    wheelRadius = bstat["wheelRadius"]
    wheelBaseWide = bstat["wheelBaseWide"]
    wheelFrontOffset = bstat["wheelFrontOffset"]
    wheelBackOffset = bstat["wheelBackOffset"]
    AttachHeightLocal = bstat["AttachHeightLocal"]
    suspensionLength = bstat["suspensionLength"]

    ## setup general vehicle characteristics ##
    wheelAttachDirLocal = [0,0,-1]
    wheelAxleLocal = [-1,0,0]

    ## setup vehicle physics ##
    vehicle = constraints.createConstraint(logic.car.getPhysicsId(), 0, constraints.VEHICLE_CONSTRAINT)
    logic.car["cid"] = vehicle.getConstraintId()
    vehicle = constraints.getVehicleConstraint(logic.car["cid"])

    ## initialize temporary variables ##
    logic.car["dS"] = 0.0

    ## attached wheel based on actuator name ##
    wheel0 = logic.scene.objects["Wheel0"]
    wheelAttachPosLocal = [wheelBaseWide ,wheelFrontOffset, AttachHeightLocal]
    vehicle.addWheel(wheel0,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,1)

    wheel1 = logic.scene.objects["Wheel1"]
    wheelAttachPosLocal = [-wheelBaseWide ,wheelFrontOffset, AttachHeightLocal]
    vehicle.addWheel(wheel1,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,1)

    wheel2 = logic.scene.objects["Wheel2"]
    wheelAttachPosLocal = [wheelBaseWide ,wheelBackOffset, AttachHeightLocal]
    vehicle.addWheel(wheel2,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,0)

    wheel3 = logic.scene.objects["Wheel3"]
    wheelAttachPosLocal = [-wheelBaseWide ,wheelBackOffset, AttachHeightLocal]
    vehicle.addWheel(wheel3,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,0)

    ## set the default values for anything that can be changed later
    resetStats()
    setWheelStats()


## called from main car object
def carHandler():
    vehicle = constraints.getVehicleConstraint(logic.car["cid"])

    ## calculate speed by using the back wheel rotation speed ##
    S = vehicle.getWheelRotation(2)+vehicle.getWheelRotation(3)
    logic.car["speed"] = (S - logic.car["dS"])*10.0

    ## apply engine force ##
    vehicle.applyEngineForce(logic.car["force"],0)
    vehicle.applyEngineForce(logic.car["force"],1)
    vehicle.applyEngineForce(logic.car["force"],2)
    vehicle.applyEngineForce(logic.car["force"],3)

    ## calculate steering with varying sensitivity ##
    if math.fabs(logic.car["speed"])<15.0: s = 2.0
    elif math.fabs(logic.car["speed"])<28.0: s=1.5
    elif math.fabs(logic.car["speed"])<40.0: s=1.0
    else: s=0.5

    ## steer front wheels
    vehicle.setSteeringValue(logic.car["steer"]*s,0)
    vehicle.setSteeringValue(logic.car["steer"]*s,1)

    ## slowly ease off gas and center steering ##
    logic.car["steer"] *= 0.6
    logic.car["force"] *= 0.9

    ## align car to Z axis to prevent flipping ##
    bstat = logic.scene.objects["BaseStats"]
    logic.car.alignAxisToVect([0.0,0.0,1.0], 2, bstat["Stability"])

    ## store old values ##
    logic.car["dS"] = S

    ## Cast a Ray to tell if we're still on the ground
    ray = logic.car.sensors["groundRay"]
    if ray.positive:
        logic.car["onGround"] = True
        ## Show ray when testing
        #r.drawLine(logic.car.worldPosition, ray.hitPosition, [1,0,0])
    else:
        logic.car["onGround"] = False


## Set all player shapes invisible
def makeInvisible():
    logic.scene.objects["Loop 1_proxy"].setVisible(False)
    logic.scene.objects["Loop 2_proxy"].setVisible(False)
    logic.scene.objects["Loop 3_proxy"].setVisible(False)
    logic.scene.objects["Loop 4_proxy"].setVisible(False)


## Change Shapes
## Any stat not listed in an if block is set to the default value
## I figured this make it easier to see the differences
def changeShape(choice):
    makeInvisible()
    resetStats()

    ## Grab Base Stats to modify them
    bstat = logic.scene.objects["BaseStats"]

    if choice == 1:
        ## Basic
        ## Uses the default stats (Nimble, yet slow and easy to handle)
        logic.scene.objects["Loop 1_proxy"].setVisible(True)
    elif choice == 2:
        ## Bomber
        ## Higher top speed, slow turning, stable, does not take damage
        logic.scene.objects["Loop 2_proxy"].setVisible(True)
        logic.car["activeShape"] = 2
        logic.car.linVelocityMax = 90
        logic.car["glideBonusY"] = 0.5
        logic.car["glideBonusZ"] = 0.47
        logic.car["glideCooldown"] = 28
        logic.car["glideDur"] = 22
        logic.car["glideJumpY"] = 0.6
        logic.car["glideJumpZ"] = 0.4
        logic.car["accelNormal"] = -12
        logic.car["accelTurbo"] = -15
        logic.car["turboDur"] = 16
        logic.car["brakeForce"] = 3.0
        logic.car["steerAmount"] = 0.015
        ## Wheel/Handling Stats
        bstat["stiffness"] = 30.0
        bstat["damping"] = 20.0
        bstat["Stability"] = 0.1
        setWheelStats()
    elif choice == 3:
        ## Racer - Wild
        ## Fastest, highest top speed, unstable, longest glide
        logic.scene.objects["Loop 3_proxy"].setVisible(True)
        logic.car["activeShape"] = 3
        logic.car.linVelocityMax = 400
        logic.car["accelNormal"] = -18
        logic.car["accelTurbo"] = -25
        logic.car["turboDur"] = 12
        logic.car["brakeForce"] = 3
        logic.car["glideBonusY"] = 1
        logic.car["glideBonusZ"] = 0.43
        logic.car["glideCooldown"] = 24
        logic.car["glideDur"] = 18
        logic.car["glideJumpY"] = 0.5
        logic.car["glideJumpZ"] = 0.6
        logic.car["steerAmount"] = 0.125
        ## Wheel/Handling Stats
        bstat["influence"] = 0.07
        bstat["stiffness"] = 40.0
        bstat["damping"] = 20.0
        bstat["Stability"] = 0.03
        setWheelStats()
    elif choice == 4:
        ## Racer - Tame
        ## Fast, stable yet nimble, long glide
        logic.scene.objects["Loop 4_proxy"].setVisible(True)
        logic.car["activeShape"] = 4
        logic.car.linVelocityMax = 70
        logic.car["accelNormal"] = -12
        logic.car["turboDur"] = 16
        logic.car["glideBonusY"] = 0.6
        logic.car["glideBonusZ"] = 0.46
        logic.car["glideCooldown"] = 14
        logic.car["glideDur"] = 12
        logic.car["steerAmount"] = 0.05
        ## Wheel/Handling Stats
        bstat["Stability"] = 0.1
        setWheelStats()
    elif choice == 5:
        ## Tank
        ## Trades Glide for a turret, strong, slow turning
        logic.scene.objects["Loop 1_proxy"].setVisible(True)
        logic.car["activeShape"] = 5
    elif choice == 6:
        ## Mech
        ## Trades Glide for turret and Turbo for jump, slow, strong, deadly
        logic.scene.objects["Loop 1_proxy"].setVisible(True)
        logic.car["activeShape"] = 6
        logic.car["mechJumpY"]  = 10.0
        logic.car["mechJumpZ"]  = 20.0


## Reset max speed after using turbo
def resetTopSpeed():
    if logic.car["activeShape"] == 1:
        logic.car.linVelocityMax = 40
    elif logic.car["activeShape"] == 2:
        logic.car.linVelocityMax = 90
    elif logic.car["activeShape"] == 3:
        logic.car.linVelocityMax = 400
    elif logic.car["activeShape"] == 4:
        logic.car.linVelocityMax = 70
    elif logic.car["activeShape"] == 5:
        logic.car.linVelocityMax = 60
    elif logic.car["activeShape"] == 6:
        logic.car.linVelocityMax = 60


## Turbo
def turbo():
    if logic.car["onGround"] == True:
        ## Foward bonus when driving
        if logic.car["turbo"] == False and logic.car["turboTimer"] > logic.car["turboCooldown"]:
            logic.car["turbo"] = True
            logic.car["turboTimer"] = 0
        if logic.car["turbo"] == True and logic.car["turboTimer"] < logic.car["turboDur"]:
            logic.car.linVelocityMax += 5
            logic.car["force"]  = logic.car["accelTurbo"]
        else:
            logic.car["turbo"] = False
            resetTopSpeed()
    else:
        ## Forward bonus when gliding
        ## Note that topspeed is N/A, because the wheels aren't rolling!
        if logic.car["turbo"] == False and logic.car["turboTimer"] > logic.car["turboCooldown"]:
            logic.car["turbo"] = True
            logic.car["turboTimer"] = 0
        if logic.car["turbo"] == True and logic.car["turboTimer"] < logic.car["turboDur"]:
            logic.car.linearVelocity[1] += abs(logic.car["accelTurbo"]) / 10
        else:
            logic.car["turbo"] = False
            resetTopSpeed()


## Glide
def glide():
    if logic.car["onGround"] == True and logic.car["glideTimer"] > logic.car["glideCooldown"]:
        logic.car["glideTimer"] = 0
        ## Apply upward and forward impulse
        for x in range(0, 30):
            logic.car.linearVelocity[1] += logic.car["glideJumpY"]
            logic.car.linearVelocity[2] += logic.car["glideJumpZ"] * (logic.car["speed"] / 200 + 1)
    elif logic.car["onGround"] == False:
        ## Maintain Glide
        logic.car.linearVelocity[1] += logic.car["glideBonusY"]
        logic.car.linearVelocity[2] += logic.car["glideBonusZ"]
        ## Allow gliding as long as you like, but start cooldown upon landing
        logic.car["glideTimer"] = 0

## Unlimited Jump for the Mech shape
def mechJump():
    if logic.car["onGround"]:
        logic.car.linearVelocity[1] += logic.car["mechJumpY"]
        logic.car.linearVelocity[2] += logic.car["mechJumpZ"]


## Flip player over or reset to start position
def resetPlayer():
    pos = logic.car.worldPosition
    if logic.car["rescue"] > 5:
        # re-orient car (5 second cooldown)
        logic.car.position = (pos[0], pos[1], pos[2]+3.0)
        logic.car["rescue"] = -10
    if pos[2] < -3.0:
        # return to start position if below lowest level
        logic.car.position = (0, 0, 8.0)
        logic.car["rescue"] = -10
    if logic.car["rescue"] < 0:
        # right the player
        logic.car.alignAxisToVect([0.0,0.0,1.0], 2, 1.0)
        logic.car.setLinearVelocity([0.0,0.0,0.0],1)
        logic.car.setAngularVelocity([0.0,0.0,0.0],1)
        logic.car["rescue"] = 0


## called from main car object
def keyHandler():
    cont = logic.getCurrentController()
    keys = cont.sensors["key"].events
    for key in keys:
        ## Forward
        if key[0] == events.WKEY:
            logic.car["force"]  = logic.car["accelNormal"]
        ## Turbo
        if key[0] == events.LEFTSHIFTKEY:
             if logic.car["activeShape"] <= 5:
                turbo()
             else:
                # Do Mech Jump
                mechJump()
        ## Reverse
        elif key[0] == events.SKEY:
            if logic.car["speed"] < 10.0:
                logic.car["force"]  = logic.car["accelNormal"] / 2 * -1
        ## Right
        elif key[0] == events.DKEY:
            logic.car["steer"] -= logic.car["steerAmount"]
        ## Left
        elif key[0] == events.AKEY:
            logic.car["steer"] += logic.car["steerAmount"]
        ## Reset Player
        elif key[0] == events.RKEY:
                resetPlayer()
        ## Brake
        elif key[0] == events.LEFTCTRLKEY:
            if logic.car["speed"] > 2.0:
                 ## Braking when going forward
                logic.car["force"]  = logic.car["brakeForce"]
            if logic.car["speed"] < 0:
                ## Braking when going backward
                logic.car["force"]  = -10
        ## Gliding / Turrets
        elif key[0] == events.SPACEKEY:
            if logic.car["activeShape"] <= 4:
                glide()
            elif logic.car["activeShape"] == 5:
                ## Allow Tank Turret Movement (NYI)
                blah = 1
            elif logic.car["activeShape"] == 6:
                ## Allow Mech Turret Movement (NYI)
                blah = 1
        elif key[0] == events.PAD1:
            changeShape(1)
        elif key[0] == events.PAD2:
            changeShape(2)
        elif key[0] == events.PAD3:
            changeShape(3)
        elif key[0] == events.PAD4:
            changeShape(4)
        elif key[0] == events.PAD5:
            ## Model not in yet
            changeShape(5)
        elif key[0] == events.PAD6:
            ## Model not in yet
            changeShape(6)


## Mouse Steering
def mouseMove():
    cont = logic.getCurrentController()
    logic.car = cont.owner
    mouse = cont.sensors["Mouse"]

    ## Set mouse sensitivity
    sensitivity = 0.07

    h = r.getWindowHeight()//2
    w = r.getWindowWidth()//2
    x = (h - mouse.position[0])*sensitivity
    y = (w - mouse.position[1])*sensitivity

    # reset mouse for next frame and keep mouse in the game window
    r.setMousePosition(h, w)

    rot = logic.car.localOrientation.to_euler()

    # Bank / Lean when gliding, but not for Tank and Mech
    if logic.car["onGround"] == False and logic.car["activeShape"] <= 4:
        yaw = math.degrees(rot[2]) + x / 6
        rot[2] = math.radians(yaw)

        roll = math.degrees(rot[1]) + x * -1
        rot[1] = math.radians(roll)

        pitch = math.degrees(rot[0]) + y / 4
        rot[0] = math.radians(pitch)

        # Apply rotation
        logic.car.localOrientation = rot.to_matrix()

    ## Mouse "dead zone" 0.45 to help moving straight
    # Right
    if x < -0.45:
        # Turn Wheels
        logic.car["steer"] -= logic.car["steerAmount"] / 2
        if logic.car["onGround"] == False:
            # Vector thrust to move (and stay in the air)
            logic.car.linearVelocity[0] += logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 4
    # Left
    if x > 0.45:
        # Turn Wheels
        logic.car["steer"] += logic.car["steerAmount"] / 2
        if logic.car["onGround"] == False:
            # Vector thrust to move (and stay in the air)
            logic.car.linearVelocity[0] -= logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 4


    # reset mouse for next frame and keep mouse in the game window
    r.setMousePosition(h, w)


