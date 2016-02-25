'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public License v3

---------------------
Fundamental player movement, stat changing, and related player input
---------------------

The player is based on the "car" from the vehicle physics demo, which has a whack of C++ dedicated
to simulating vehicle physics. I've modified and added to it to the point where there's almost
nothing left of the demo, but I'll leave the credits in here anyhow, because the demo's guidance
was part of what made this project possible (to do in the Blender Game Engine).

'''

#################################
#  Vehicle Physics Demo
#
#  This file is part of the book:
#  "Game Development with Blender"
#  by Dalai Felinto and Mike Pan
#
#  Published by "CENGAGE Learning" in 2013
#
#  You are free to use-it, modify it and redistribute
#  as long as you keep the original credits when pertinent.
#
#  File tested with Blender 2.66
#
#  Copyright - February 2013
#  This work is licensed under the Creative Commons
#  Attribution-Share Alike 3.0 Unported License
#################################

# First, we import all the python modules
from bge import constraints
from bge import logic
from bge import events
from bge import render as r
import math
import GameLogic as G

########
# BEGIN bare object (player) movement and handling
########

# Set/Change the wheel stats, which handle driving physics on the gound.
def setWheelStats():
    # Apply handling stats to the (invisible) wheels
    vehicle = constraints.getVehicleConstraint(logic.car["cid"])
    # Grab base stats from "BaseStats" object
    bstat = logic.scene.objects["BaseStats"]
    # set vehicle roll tendency
    vehicle.setRollInfluence(bstat["influence"],0)
    vehicle.setRollInfluence(bstat["influence"],1)
    vehicle.setRollInfluence(bstat["influence"],2)
    vehicle.setRollInfluence(bstat["influence"],3)
    # set vehicle suspension hardness
    vehicle.setSuspensionStiffness(bstat["stiffness"],0)
    vehicle.setSuspensionStiffness(bstat["stiffness"],1)
    vehicle.setSuspensionStiffness(bstat["stiffness"],2)
    vehicle.setSuspensionStiffness(bstat["stiffness"],3)
    # set vehicle suspension dampness
    vehicle.setSuspensionDamping(bstat["damping"],0)
    vehicle.setSuspensionDamping(bstat["damping"],1)
    vehicle.setSuspensionDamping(bstat["damping"],2)
    vehicle.setSuspensionDamping(bstat["damping"],3)
    # set vehicle suspension compression ratio
    vehicle.setSuspensionCompression(bstat["compression"],0)
    vehicle.setSuspensionCompression(bstat["compression"],1)
    vehicle.setSuspensionCompression(bstat["compression"],2)
    vehicle.setSuspensionCompression(bstat["compression"],3)
    # set vehicle tire friction
    vehicle.setTyreFriction(bstat["friction"],0)
    vehicle.setTyreFriction(bstat["friction"],1)
    vehicle.setTyreFriction(bstat["friction"],2)
    vehicle.setTyreFriction(bstat["friction"],3)


# Put the physics for the player together, using the car logic
# Called from the object named "bare" once at the start of the game
def carInit():
    # setup aliases for Blender API access
    cont = logic.getCurrentController()
    logic.scene = logic.getCurrentScene()
    logic.car  = cont.owner

    # Grab base stats from "BaseStats" object
    bstat = logic.scene.objects["BaseStats"]

    # Constants
    wheelRadius = bstat["wheelRadius"]
    wheelBaseWide = bstat["wheelBaseWide"]
    wheelFrontOffset = bstat["wheelFrontOffset"]
    wheelBackOffset = bstat["wheelBackOffset"]
    AttachHeightLocal = bstat["AttachHeightLocal"]
    suspensionLength = bstat["suspensionLength"]

    # setup general vehicle characteristics
    wheelAttachDirLocal = [0,0,-1]
    wheelAxleLocal = [-1,0,0]

    # setup vehicle physics
    vehicle = constraints.createConstraint(logic.car.getPhysicsId(), 0, constraints.VEHICLE_CONSTRAINT)
    logic.car["cid"] = vehicle.getConstraintId()
    vehicle = constraints.getVehicleConstraint(logic.car["cid"])

    # Initialize variable to store speed so we can get the delta between frames
    logic.car["dS"] = 0.0

    # Attach the wheels to the bare object
    # (0)---(1)
    #    [|]
    # (2)---(3)
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

    # set the default values for anything that can be changed later
    resetStats()
    setWheelStats()


# Check if we are on the ground using -Y ray cast from bare object
def groundCheck():
    ray = logic.car.sensors["groundRay"]
    if ray.positive:
        logic.car["onGround"] = True
        # Show ray when testing
        #from bge import render as r
        #r.drawLine(logic.car.worldPosition, ray.hitPosition, [1,0,0])
    else:
        logic.car["onGround"] = False


# Check if we are on a ribbon (road) using -Y ray cast from bare object
# Change movement speed based on shape
def ribbonCheck():
    ray = logic.car.sensors["ribbonRay"]

    if logic.car["onGround"] == True:
        if ray.positive:
            logic.car["onRibbon"] = True

            # Show ray when testing
            #from bge import render as r
            #r.drawLine(logic.car.worldPosition, ray.hitPosition, [1,0,0])
        else:
            logic.car["onRibbon"] = False


# Main player "game loop"
# Called from bare object (player) every frame
def carHandler():
    # Apply max/top speed constraint (any time we aren't changing it)
    if logic.car["limitMaxVelocity"] == True:
        logic.car.linVelocityMax = logic.car["myLinVelocityMax"]

    vehicle = constraints.getVehicleConstraint(logic.car["cid"])

    # calculate speed by using the back wheel rotation and delta of value stored in the previous frame
    S = vehicle.getWheelRotation(2)+vehicle.getWheelRotation(3)
    logic.car["speed"] = (S - logic.car["dS"])*10.0

    # calculate world velocity, which is also valid while in the air. Raw value used for speedometer UI.
    Xspeed, Yspeed, Zspeed = logic.car.getLinearVelocity(True)
    linSum = Xspeed + Yspeed
    G.mySpeed = linSum

    # apply engine force
    vehicle.applyEngineForce(logic.car["force"]*10,0)
    vehicle.applyEngineForce(logic.car["force"]*10,1)
    vehicle.applyEngineForce(logic.car["force"]*10,2)
    vehicle.applyEngineForce(logic.car["force"]*10,3)

    # calculate steering with varying sensitivity
    if math.fabs(logic.car["speed"])<15.0: s = 2.0
    elif math.fabs(logic.car["speed"])<28.0: s=1.5
    elif math.fabs(logic.car["speed"])<40.0: s=1.0
    else: s=0.5

    # steer front wheels
    vehicle.setSteeringValue(logic.car["steer"]*s,0)
    vehicle.setSteeringValue(logic.car["steer"]*s,1)

    # slowly ease off gas and center steering
    logic.car["steer"] *= 0.6
    logic.car["force"] *= 0.9

    # align to Z axis to prevent flipping
    bstat = logic.scene.objects["BaseStats"]
    logic.car.alignAxisToVect([0.0,0.0,1.0], 2, bstat["Stability"])

    # store old values
    logic.car["dS"] = S
    logic.car["dlinSum"] = linSum

    # Checks and status updates
    groundCheck()
    ribbonCheck()
    turboStatus()
    glideStatus()


# Move the player
# Note that in the air the player automatically increases to max speed when holding spacebar
def movePlayer(direction):
    # Ribbon Speed
    adjustSpeed = 1.0

    if logic.car["onGround"] == True:
        if logic.car["onRibbon"] == False:
            # Plain Ground Speed
            adjustSpeed = 2 - logic.car["speedMult"]

    if direction == 1:
        # Forward
        logic.car["force"]  = logic.car["accelNormal"] * adjustSpeed
    elif direction == 0 and logic.car["speed"] < 10.0:
        # Reverse
        logic.car["force"]  = logic.car["accelNormal"] / 2 * adjustSpeed * -1


# Apply keyboard steering
def steerPlayer(direction):
    if direction == 1:
        # Left
        logic.car["steer"] += logic.car["steerAmount"]
    elif direction == 0:
        # Right
        logic.car["steer"] -= logic.car["steerAmount"]


# Apply brakes
def applyBrakes():
    if logic.car["speed"] > 2.0:
         # Braking when going forward
        logic.car["force"]  = logic.car["brakeForce"]
    if logic.car["speed"] < 0:
        # Braking when going backward
        logic.car["force"]  = -10


# Handle Turbo key press
def pressedTurbo():
    if G.turboCooldown == True:
        return

    if G.turboActive == True:
        applyTurbo()
    else:
        G.turboActive = True
        logic.car["turboDurTimer"] = 0
        applyTurbo()


# Apply Turbo motion
def applyTurbo():
    if logic.car["onGround"] == True:
        logic.car.linVelocityMax += 4
        logic.car["force"]  = logic.car["accelTurbo"]
    else:
        logic.car.linVelocityMax += 1
        logic.car.linearVelocity[1] += abs(logic.car["accelTurbo"]) / 40


# Set Turbo status
def turboStatus():
    # Prevent slowing down while doing a skijump
    if logic.car["skiJumping"] == True:
        return

    if G.turboActive == True:
        # Turbo is ON, so start timer and stop limiting max speed
        logic.car["turboCoolTimer"] = 0
        logic.car["limitMaxVelocity"] = False
        if logic.car["turboDurTimer"] > logic.car["turboDur"]:
            # Time is up, so turn off Turbo and start cooldown timer
            G.turboActive = False
            logic.car["turboCoolTimer"] = 0
            G.turboCooldown = True
    elif G.turboCooldown == True:
        logic.car["turboDurTimer"] = 0
        if logic.car["turboCoolTimer"] > logic.car["turboCooldown"]:
            G.turboCooldown = False
    else:
         logic.car["turboCoolTimer"] = 0
         logic.car["turboDurTimer"] = 0

    # Slow down after using turbo
    if G.turboActive == False:
        if logic.car.linVelocityMax > logic.car["myLinVelocityMax"]:
            # Gently reset top speed
            logic.car.linVelocityMax -= 2
        elif logic.car.linVelocityMax <= logic.car["myLinVelocityMax"]:
            # Back at normal top speed, so hard limit it again
            logic.car["limitMaxVelocity"] = True

    # Send timer data to global variables for UI
    G.turboDurTimerUI = str(int(logic.car["turboDur"] - logic.car["turboDurTimer"]))
    G.turboCoolTimerUI = str(int(logic.car["turboCooldown"] - logic.car["turboCoolTimer"]))


# Gliding/flying for aircraft shapes
# Glide timer is kept at 0 while the player is holding spacebar down and is in the air
def airGlide():
    # Prevent gliding while doing a skijump (avoid exploiting super high top speed)
    if logic.car["skiJumping"] == True:
        return

    if logic.car["onGround"] == True and logic.car["glideTimer"] > logic.car["glideCooldown"]:
        logic.car["glideTimer"] = 0
        # Apply upward and forward impulse
        for x in range(0, 30):
            logic.car.linearVelocity[1] += logic.car["glideJumpY"]
            logic.car.linearVelocity[2] += logic.car["glideJumpZ"] * (logic.car["speed"] / 200 + 1)
    elif logic.car["onGround"] == False:
        # Maintain Glide
        logic.car.linearVelocity[1] += logic.car["glideBonusY"] * 2
        logic.car.linearVelocity[2] += logic.car["glideBonusZ"] * 2
        # Allow gliding as long as you like, but start cooldown upon landing
        logic.car["glideTimer"] = 0


def glideStatus():
    # Send timer data to global variable for UI
    G.glideCooldownTimer = logic.car["glideTimer"]
    G.glideCooldown = logic.car["glideCooldown"]
    G.activeShape = logic.car["activeShape"]
    G.cornerAssist = logic.car["cornerAssist"]


### BEGIN Gliding (Corner Assist) for Shapes 4 and 5

# The three car shapes can't fly, instead they can turn on corner assist mode
# which automatically sucks them around 90 and 180 degree turns.

# Toggle ON/OFF state (once in 1 second)
def groundGlide():
    logic.scene = logic.getCurrentScene()
    timer = logic.scene.objects["Controller"]
    if timer["timer"] > 1:
        timer["timer"] = 0
        if logic.car["cornerAssist"] == False:
            logic.car["cornerAssist"] = True
            cornerTriggerVisibility(True)
        elif logic.car["cornerAssist"] == True:
            logic.car["cornerAssist"] = False
            cornerTriggerVisibility(False)

def cornerTriggerVisibility(state):
    for o in logic.scene.objects:
        if 'CornerTrigger' in o:
            o.setVisible(state)

# Move the navigation mesh and trigger group into position
def moveNavMesh(meshName, startTrigger):
    if logic.car["activeShape"] > 4:
        if logic.car["onRibbon"] == True and logic.car["cornerAssist"] == True:
            cont = logic.getCurrentController()
            logic.scene = logic.getCurrentScene()
            timer = logic.scene.objects["Controller"]

            # timer gets set to 0 when approaching a corner assist trigger from the wrong direction
            # (when player collides with a CornerTriggerWrongDirection object), thereby preventing this
            # function from spawning an unwanted nav mesh/trigger that would send the player back the way they came.
            if timer["timer"] > 0.5:
                trigger = logic.scene.objects[startTrigger]
                trigger["ready"] = True
                navMesh = logic.scene.objects[meshName]
                navMesh.worldPosition = cont.owner.worldPosition
                navMesh.worldOrientation = cont.owner.worldOrientation

# Called by the RailNav___Start objects on collision with player
# Script logic brick does not appear to allow using argruements when calling a function, so I have a function
# for each logic brick that simply calls the fuction I want to use with the correct arguements...
def moveNavMesh180R():
    moveNavMesh("RailNav180Right", "180GoRightStart")

def moveNavMesh180L():
    moveNavMesh("RailNav180Left", "180GoLeftStart")

def moveNavMesh90R():
    moveNavMesh("RailNav90Right", "90GoRightStart")

def moveNavMesh90L():
    moveNavMesh("RailNav90Left", "90GoLeftStart")

# Turn off the pathing effect
# Called by RailNav___End objects on collision with player
def goOff():
    logic.scene = logic.getCurrentScene()
    right90 = logic.scene.objects["90GoRightStart"]
    left90 = logic.scene.objects["90GoLeftStart"]
    right180 = logic.scene.objects["180GoRightStart"]
    left180 = logic.scene.objects["180GoLeftStart"]

    right90["go"] = False
    left90["go"] = False
    right180["go"] = False
    left180["go"] = False

# Move the navigation mesh and trigger group back under the world
# Called by the RailNav___Mover objects on collision with the player
def moveNavMeshHome():
    cont = logic.getCurrentController()
    myParent = cont.owner["myParent"]
    navMesh = logic.scene.objects[myParent]

    logic.scene = logic.getCurrentScene()
    right90 = logic.scene.objects["90GoRightStart"]
    left90 = logic.scene.objects["90GoLeftStart"]
    right180 = logic.scene.objects["180GoRightStart"]
    left180 = logic.scene.objects["180GoLeftStart"]

    #Turn off pathing trigger to avoid hitting the player with it while moving it (super important!)
    right90["ready"] = False
    left90["ready"] = False
    right180["ready"] = False
    left180["ready"] = False

    navMesh.worldPosition = (0, 0, -200)
### END Gliding (Corner Assist) for Shapes 4 and 5


# Flip player over and lift them to unstick
def rescuePlayer():
    pos = logic.car.worldPosition
    if logic.car["rescue"] > 5:
        # re-orient car (5 second cooldown)
        logic.car.position = (pos[0], pos[1], pos[2]+3.0)
        # Reset chase cam in case it gets stuck
        chaseCam = logic.scene.objects["cam0"]
        chaseCam.position = logic.car.position
        logic.car["rescue"] = -10
    if logic.car["rescue"] < 0:
        # right the player
        logic.car.alignAxisToVect([0.0,0.0,1.0], 2, 1.0)
        logic.car.setLinearVelocity([0.0,0.0,0.0],1)
        logic.car.setAngularVelocity([0.0,0.0,0.0],1)
        logic.car["rescue"] = 0


# Send player back home after "death"
# Called by chaos level on collision with player or CTL + R key press by the player
def resetPlayer():
    rescuePlayer()
    changeShape(1)
    logic.car.position = (0, 0, 6.0)
    chaseCam = logic.scene.objects["cam0"]
    chaseCam.position = logic.car.position


########
# BEGIN Changing shapes / setting stats and abilities
########

# Set all player shapes invisible
def makeInvisible():
    logic.scene.objects["Loop 1_proxy"].setVisible(False)
    logic.scene.objects["Loop 2_proxy"].setVisible(False)
    logic.scene.objects["Loop 3_proxy"].setVisible(False)
    logic.scene.objects["Loop 4_proxy"].setVisible(False)
    logic.scene.objects["Loop 5_proxy"].setVisible(False)
    logic.scene.objects["Loop 6_proxy"].setVisible(False)
    logic.scene.objects["Loop 7_proxy"].setVisible(False)

# Set current shape visible again (when switching from first person camera, etc.)
def makeVisible():
    showMe = logic.car["activeShape"]
    if showMe == 1:
        logic.scene.objects["Loop 1_proxy"].setVisible(True)
    elif showMe == 2:
        logic.scene.objects["Loop 2_proxy"].setVisible(True)
    elif showMe == 3:
        logic.scene.objects["Loop 3_proxy"].setVisible(True)
    elif showMe == 4:
        logic.scene.objects["Loop 4_proxy"].setVisible(True)
    elif showMe == 5:
        logic.scene.objects["Loop 5_proxy"].setVisible(True)
    elif showMe == 6:
        logic.scene.objects["Loop 6_proxy"].setVisible(True)
    elif showMe == 7:
        logic.scene.objects["Loop 7_proxy"].setVisible(True)


#  Set default shape values (Green glider shape)
def resetStats():
    # Max/Top Speed
    logic.car["myLinVelocityMax"] = 54
    # Ribbon speed bonus (*speedMult) and off ribbon hinderance (*2-speedMult)
    logic.car["speedMult"]  = 1.25

    # Default Shape
    logic.car["activeShape"] = 1
    logic.car["accelNormal"] = -12.0
    logic.car["accelTurbo"] = -16.0
    logic.car["turboDur"] = 7.0
    logic.car["turboCooldown"] = 10.0
    logic.car["brakeForce"] = 10.0
    logic.car["steerAmount"] = 0.08
    logic.car["glideCooldown"] = 30
    logic.car["glideDur"] = 5
    logic.car["glideBonusY"] = 0.2
    logic.car["glideBonusZ"] = 0.38
    # Lift impulse or "jump"
    logic.car["glideJumpY"] = 0.1
    logic.car["glideJumpZ"] = 0.43

    # Base Stats
    bstat = logic.scene.objects["BaseStats"]
    bstat["influence"] = 0.01
    bstat["stiffness"] = 20.0
    bstat["damping"] = 2.0
    bstat["compression"] = 4.0
    bstat["friction"] = 10.0
    bstat["Stability"] = 0.1

    # Abilities
    abilities = logic.scene.objects["Abilities"]
    abilities["abilityLMB"] = 1
    abilities["abilityRMB"] = 1


# Change Shapes
# Any stat not listed in an if block is set to the default value
# I figured this make it easier to see the differences
def changeShape(choice):
    makeInvisible()
    resetStats()
    cornerTriggerVisibility(False)
    logic.car["cornerAssist"] = False

    # Grab Base Stats to modify them
    bstat = logic.scene.objects["BaseStats"]
    # Grab abilities
    abilities = logic.scene.objects["Abilities"]
    # Grab current camera
    camera = logic.scene.objects["Controller"]

    if choice == 1:
        # Glider
        # Uses the default stats (Nimble, easy to handle, short range gliding.)
        logic.scene.objects["Loop 1_proxy"].setVisible(True)
    elif choice == 2:
        # Bomber
        # Higher top speed, slow turning, stable, strong, max speed anywhere.
        abilities["abilityLMB"] = 1
        abilities["abilityRMB"] = 1
        logic.scene.objects["Loop 2_proxy"].setVisible(True)
        logic.car["activeShape"] = 2
        logic.car["myLinVelocityMax"] = 120
        logic.car["speedMult"]  = 1.0
        logic.car["glideBonusY"] = 0.5
        logic.car["glideBonusZ"] = 0.42
        logic.car["glideCooldown"] = 20
        logic.car["glideDur"] = 22.0
        logic.car["glideJumpY"] = 0.6
        logic.car["glideJumpZ"] = 0.4
        logic.car["accelNormal"] = -12
        logic.car["accelTurbo"] = -18
        logic.car["turboDur"] = 16
        logic.car["turboCooldown"] = 20.0
        logic.car["brakeForce"] = 3.0
        logic.car["steerAmount"] = 0.015
        # Wheel/Handling Stats
        bstat["stiffness"] = 30.0
        bstat["damping"] = 4.0
        bstat["Stability"] = 0.1
        setWheelStats()
    elif choice == 3:
        # Air Racer
        # Fastest, highest top speed, unstable, longest glide
        abilities["abilityLMB"] = 2
        abilities["abilityRMB"] = 1
        logic.scene.objects["Loop 3_proxy"].setVisible(True)
        logic.car["activeShape"] = 3
        logic.car["myLinVelocityMax"] = 200
        logic.car["speedMult"]  = 1.5
        logic.car["accelNormal"] = -18
        logic.car["accelTurbo"] = -25
        logic.car["turboDur"] = 8.0
        logic.car["turboCooldown"] = 8.0
        logic.car["brakeForce"] = 3
        logic.car["glideBonusY"] = 1
        logic.car["glideBonusZ"] = 0.41
        logic.car["glideCooldown"] = 4
        logic.car["glideDur"] = 18
        logic.car["glideJumpY"] = 0.5
        logic.car["glideJumpZ"] = 0.4
        logic.car["steerAmount"] = 0.125
        # Wheel/Handling Stats
        bstat["influence"] = 0.07
        bstat["stiffness"] = 40.0
        bstat["damping"] = 4.0
        bstat["Stability"] = 0.03
        setWheelStats()
    elif choice == 4:
        # Strategic Fighter Jet
        # Stable yet nimble, long glide
        abilities["abilityLMB"] = 1
        abilities["abilityRMB"] = 1
        logic.scene.objects["Loop 4_proxy"].setVisible(True)
        logic.car["activeShape"] = 4
        logic.car["myLinVelocityMax"] = 150
        logic.car["speedMult"]  = 1.5
        logic.car["accelNormal"] = -12
        logic.car["turboDur"] = 16.0
        logic.car["turboCooldown"] = 18.0
        logic.car["glideBonusY"] = 0.8
        logic.car["glideBonusZ"] = 0.43
        logic.car["glideCooldown"] = 15
        logic.car["glideDur"] = 12
        logic.car["steerAmount"] = 0.045
        # Wheel/Handling Stats
        bstat["stiffness"] = 30
        bstat["damping"] = 4.0
        bstat["Stability"] = 0.066
        #setWheelStats()
    elif choice == 5:
        # Scifimobile
        # Trades Glide for ability to stick to ribbons, fastest, weak, reduced agro.
        abilities["abilityLMB"] = 3
        abilities["abilityRMB"] = 1
        logic.scene.objects["Loop 5_proxy"].setVisible(True)
        logic.car["activeShape"] = 5
        logic.car["myLinVelocityMax"] = 110
        logic.car["speedMult"]  = 1.66
        logic.car["accelNormal"] = -22
        logic.car["accelTurbo"] = -30
        logic.car["turboDur"] = 5
        logic.car["turboCooldown"] = 20.0
        logic.car["glideCooldown"] = 2.0
        logic.car["brakeForce"] = 2
        logic.car["steerAmount"] = 0.06
        # Wheel/Handling Stats
        bstat["stiffness"] = 40.0
        bstat["Stability"] = 0.14
        setWheelStats()
    elif choice == 6:
        # Muscle Car
        # Trades Glide for ability to stick to ribbons, strong.
        abilities["abilityLMB"] = 1
        abilities["abilityRMB"] = 1
        logic.scene.objects["Loop 6_proxy"].setVisible(True)
        logic.car["activeShape"] = 6
        logic.car["myLinVelocityMax"] = 75
        logic.car["speedMult"]  = 1.66
        logic.car["accelNormal"] = -16
        logic.car["accelTurbo"] = -20
        logic.car["turboDur"] = 12
        logic.car["turboCooldown"] = 10.0
        logic.car["glideCooldown"] = 2.0
        logic.car["brakeForce"] = 8
        logic.car["steerAmount"] = 0.06
        # Wheel/Handling Stats
        bstat["stiffness"] = 30
        bstat["Stability"] = 0.12
        setWheelStats()
    elif choice == 7:
        # Kid Car
        # Trades Glide for ability to stick to ribbons, free, easy to drive.
        logic.scene.objects["Loop 7_proxy"].setVisible(True)
        logic.car["activeShape"] = 7
        logic.car["myLinVelocityMax"] = 46
        logic.car["speedMult"]  = 1.0
        logic.car["accelNormal"] = -8
        logic.car["accelTurbo"] = -14
        logic.car["turboDur"] = 6
        logic.car["turboCooldown"] = 6.0
        logic.car["glideCooldown"] = 2.0
        logic.car["brakeForce"] = 9
        logic.car["steerAmount"] = 0.035
        # Wheel/Handling Stats
        bstat["stiffness"] = 30
        bstat["Stability"] = 0.12
        setWheelStats()

    if camera["activeCamera"] == 3:
        # First person camera is ON so don't show shape.
        makeInvisible()


########
# Player Input
########

# Keyboard - called from bare object
def keyHandler():
    cont = logic.getCurrentController()
    sensor = cont.sensors["KeyInput"].events
    for key in sensor:
        # Forward
        if key[0] == events.WKEY or key[0] == events.UPARROWKEY:
            movePlayer(1)
        # Turbo
        if key[0] == events.LEFTSHIFTKEY or key[0] == events.RIGHTSHIFTKEY:
             pressedTurbo()
        # Reverse
        elif key[0] == events.SKEY or key[0] == events.DOWNARROWKEY:
            movePlayer(0)
        # Right
        elif key[0] == events.DKEY or key[0] == events.RIGHTARROWKEY:
            steerPlayer(0)
        # Left
        elif key[0] == events.AKEY or key[0] == events.LEFTARROWKEY:
            steerPlayer(1)
        # Rescue/Unstick Player
        elif key[0] == events.RKEY:
                rescuePlayer()
        # Reset Player
        elif key[0] == events.F12KEY:
                resetPlayer()
        # Brake
        elif key[0] == events.LEFTCTRLKEY or key[0] == events.RIGHTCTRLKEY:
            applyBrakes()
        # Gliding
        elif key[0] == events.SPACEKEY or key[0] == events.PAD0:
            if logic.car["activeShape"] <= 4:
                airGlide()
            elif logic.car["activeShape"] >= 5:
                groundGlide()
        # This section is for testing only. Will be replaced by UI.
        elif key[0] == events.PAD1:
            changeShape(1)
        elif key[0] == events.PAD2:
            changeShape(2)
        elif key[0] == events.PAD3:
            changeShape(3)
        elif key[0] == events.PAD4:
            changeShape(4)
        elif key[0] == events.PAD5:
            changeShape(5)
        elif key[0] == events.PAD6:
            changeShape(6)
        elif key[0] == events.PAD7:
            changeShape(7)


# Mouse Steering - called from bare object
def mouseMove():
    cont = logic.getCurrentController()
    logic.car = cont.owner
    mouse = cont.sensors["Mouse"]

    # Set mouse sensitivity
    sensitivity = 0.07

    h = r.getWindowHeight()//2
    w = r.getWindowWidth()//2
    x = (h - mouse.position[0])*sensitivity
    y = (w - mouse.position[1])*sensitivity

    #  reset mouse for next frame and keep mouse in the game window
    r.setMousePosition(h, w)

    rot = logic.car.localOrientation.to_euler()

    #  Bank / Lean when gliding, but not for car shapes
    if logic.car["onGround"] == False and logic.car["activeShape"] <= 4:
        yaw = math.degrees(rot[2]) + x / 6
        rot[2] = math.radians(yaw)

        roll = math.degrees(rot[1]) + x * -1
        rot[1] = math.radians(roll)

        pitch = math.degrees(rot[0]) + y / 4
        rot[0] = math.radians(pitch)

        #  Apply rotation
        logic.car.localOrientation = rot.to_matrix()

    # Mouse "dead zone" 0.45 to help moving straight
    #  Right
    if x < -0.45:
        #  Turn Wheels
        logic.car["steer"] -= logic.car["steerAmount"] / 2
        if logic.car["onGround"] == False:
            #  Vector thrust to move (and stay in the air)
            logic.car.linearVelocity[0] += logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 3
    #  Left
    if x > 0.45:
        #  Turn Wheels
        logic.car["steer"] += logic.car["steerAmount"] / 2
        if logic.car["onGround"] == False:
            #  Vector thrust to move (and stay in the air)
            logic.car.linearVelocity[0] -= logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 3


    #  reset mouse for next frame and keep mouse in the game window
    r.setMousePosition(h, w)
