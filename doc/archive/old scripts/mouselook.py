# Learn from men with hair on their chest. CGMasters.net
#
#http://www.cgmasters.net/free-tutorials/fps-mouselook-script-plus-real-text/
#
# Using the Mouselook Script
# 
# 
# The script is super simple to use, and includes camera angle limitations so the camera stops 
# rotating when you’re looking straight up or straight down. This angle range can be easily 
# changed too.
# 
# Now you can either reverse engineer that scene to understand it, import the objects into your 
# scene, or follow these instructions to learn how to implement it on your own. First, here’s 
# the actual script itself. If you’re implementing this into your own scene, simply paste the 
# following code into a new text document in Blender’s text editor, and name it something like 
# “mouselook.py”.
# 
# Running the Script in Your Game
# 
# In short all you have to do is run the script from a camera which is parented to your main
# character. Also give the camera a boolean property called “startup” set to True. That’s all. 
# The script rotates the camera but also rotates the object it’s parented to so that your main 
# character is facing the same direction the camera is. So when you open that example file 
# you’ll see the camera running the script from a mouse movement sensor and an always sensor
# (set to true pulse). This camera is parented to my main character(which is a cube) which 
# also has typical FPS movement controls. To be safe, make sure your main character’s Z axis 
# is pointed up. Check out the images below for the different settings for both the cube and 
# the camera and then let’s move on to text in the game engine.

from bge import render as r
import math

cont = bge.logic.getCurrentController()
own = cont.owner
mouse = cont.sensors["Mouse"]
parent = own.parent

#set speed for camera movement
sensitivity = 0.05

#set camera rotation limits
# Defaults for stright up and down
# high_limit = 180
# low_limit = 0
high_limit = 100
low_limit = 80

h = r.getWindowHeight()//2
w = r.getWindowWidth()//2
x = (h - mouse.position[0])*sensitivity
y = (w - mouse.position[1])*sensitivity

if own["startup"]:
    r.setMousePosition(h, w)
    own ["startup"] = False
else:
    rot = own.localOrientation.to_euler()
    pitch = abs(math.degrees(rot[0]))
    if high_limit > (pitch+y) > low_limit:
        pitch += y
    elif (pitch+y) < low_limit:
        pitch = low_limit
    elif (pitch+y) > high_limit:
        pitch = high_limit
    rot[0] = math.radians(pitch)
    own.localOrientation = rot.to_matrix()

    parentRot = parent.localOrientation.to_euler()
    yaw = math.degrees(parentRot[2]) + x
    parentRot[2] = math.radians(yaw)
    parent.localOrientation = parentRot.to_matrix()

    r.setMousePosition(h, w)
