#Learn from men with hair on their chest. CGMasters.net
#
# Modified by R. Bassett Jr. www.tpot.ca
#
# Attach this script to your character/vehicle, pointing to it with  an 
# Always Sensor (True) and a Mouse Sensor (Movement). Give the object a
# booleen property called startup and set it to True.
#
# For the camera, add a camera and use the logic bricks to have it follow
# your character. No parenting required, as the Camera actuator brick will
# allow you to select the character it needs to follow. Higher dampening 
# on the camera actuator makes the camera less wobbly. You can also choose 
# from a bunch of different camera presets on its properties page - these 
# control the distance from the character (Focal Length) and field of view.
#
# On the Physics settings for your character, select Physics Type: Character
# from the drop down list. It works really well for a sci-fi vehicle and a 
# huminoid character.


from bge import render as r
import math

cont = bge.logic.getCurrentController()
own = cont.owner
mouse = cont.sensors["Mouse"]

#set speed for camera movement
sensitivity = 0.07

h = r.getWindowHeight()//2
w = r.getWindowWidth()//2
x = (h - mouse.position[0])*sensitivity
y = (w - mouse.position[1])*sensitivity

if own["startup"]:
    r.setMousePosition(h, w)
    own ["startup"] = False
else:    
    rot = own.localOrientation.to_euler()
      
    yaw = math.degrees(rot[2]) + x
    roll = math.degrees(rot[1]) + x * -1
    
    # Limit Roll angle - leaning when turning
    # Too large of a number causes the character to bounce/jitter
    if roll > 12:
        roll = 12
    elif roll < -12:
        roll = -12
    
    # Change degrees back to radians and apply the values
    # Roll conditions to level out after turning
    if abs(roll) > 4:
        rot[1] = math.radians(roll)
    else:
        roll = roll - 0.2
        rot[1] = math.radians(roll)
    rot[2] = math.radians(yaw)
    own.localOrientation = rot.to_matrix()
    
    # Reset mouse for next frame
    r.setMousePosition(h, w)
