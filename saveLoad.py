'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

---------------------
Save / Load Game Data
---------------------

Save game data in comma seperated values text files
so it can be shared between different blend files.

Yup, data is saved in plain text so if you want to
cheat, have at it! :)
'''

import bge
from bge import logic
path = logic.expandPath("//profiles/")


# Data related keyboard input
# Called from the bare object (player)
def dataKeys():
    cont = logic.getCurrentController()
    own = cont.owner
    sensor = own.sensors["KeyInput"]

    for key,status in sensor.events:
        # Take only one screenshot per key press
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if key == bge.events.F9KEY:
                own.actuators["Screenshot"].startSound()
                screenshot()
            elif key == bge.events.F10KEY:
                own.actuators["Confirm"].startSound()
                savePuzzle()
                saveInventory()

# Store user selected profile
def setProfile():
    cont = logic.getCurrentController()
    own = cont.owner
    file = open(path+'activeProfile.txt','w')
    profile = str(own['profile'])
    file.write(str(profile))


# Read user selected profile
def getProfile():
    file = open(path+'activeProfile.txt','r')
    line = file.readline().replace('\n','').split(',')
    return str(line[0])


### Puzzle Data ######################
# Stored in the PuzzleStats object when game is running
def savePuzzle():
    # Explicitly get the object, so python can call this function
    logic.scene = logic.getCurrentScene()
    own = logic.scene.objects["PuzzleStats"]


    ## Update path for the current profile
    profilePath = path + getProfile()

    ## Make different files per level
    fileName = own['fileName']

    ## Set variables for easier human reading
    p1Stage = str(own['p1Stage']) + ','
    p2Stage = str(own['p2Stage']) + ','
    p3Stage = str(own['p3Stage']) + ','
    p4Stage = str(own['p4Stage']) + ','
    p5Stage = str(own['p5Stage']) + ','

    ## Open (or create) the file for writing
    file = open(profilePath+fileName+".txt", 'w')

    ## Write data, no line breaks are written
    file.write(str(p1Stage))
    file.write(str(p2Stage))
    file.write(str(p3Stage))
    file.write(str(p4Stage))
    file.write(str(p5Stage))


def loadPuzzle():
    cont = logic.getCurrentController()
    own = cont.owner

    ## Update path for the current profile
    fileName = own['fileName']
    profilePath = path + getProfile()

    try:
        file = open(profilePath+fileName+'.txt','r')

        line = file.readline().replace('\n','').split(',')

        own['p1Stage'] = int(line[0])
        own['p2Stage'] = int(line[1])
        own['p3Stage'] = int(line[2])
        own['p4Stage'] = int(line[3])
        own['p5Stage'] = int(line[4])
    except:
        # No puzzle data file for this profile so make one
        savePuzzle()

########################################



### Inventory Data ######################
# Stored in InventoryStats object when game is running
def saveInventory():
    logic.scene = logic.getCurrentScene()
    own = logic.scene.objects["InventoryStats"]

    # Update path for the current profile
    fileName = own['fileName']
    profilePath = path + getProfile()

    # Set variables for easier human reading
    red = str(own['red']) + ','
    orange = str(own['orange']) + ','
    yellow = str(own['yellow']) + ','
    green = str(own['green']) + ','
    blue = str(own['blue']) + ','
    violet = str(own['violet']) + ','
    white = str(own['white']) + ','

    # Open (or create) the file for writing
    file = open(profilePath+fileName+".txt", 'w')

    # Write data, no line breaks are written
    file.write(str(red))
    file.write(str(orange))
    file.write(str(yellow))
    file.write(str(green))
    file.write(str(blue))
    file.write(str(violet))
    file.write(str(white))


def loadInventory():
    cont = logic.getCurrentController()
    own = cont.owner

    # Update path for the current profile
    fileName = own['fileName']
    profilePath = path + getProfile()

    try:
        file = open(profilePath+fileName+'.txt','r')

        line = file.readline().replace('\n','').split(',')

        own['red'] = int(line[0])
        own['orange'] = int(line[1])
        own['yellow'] = int(line[2])
        own['green'] = int(line[3])
        own['blue'] = int(line[4])
        own['violet'] = int(line[5])
        own['white'] = int(line[6])
    except:
        # No inventory for this profile so make one then use it
        saveInventory()

########################################



### Misc I/O ######################

# Take a screenshot
def screenshot():
    # Use an index file to number screenshots
    indexPath = logic.expandPath("//Screenshots/")
    indexFile = "index.txt"
    noteToPlayer = "\nDo not delete this file. It prevents over-writing your old screenshots with new ones."

    try:
        # index file exists, so use it
        file = open(indexPath+indexFile,'r')
        line = file.readline()
        number = int(line[0])

        # append number to screenshot name and save the screenshot
        render = bge.render
        screenshot = "//" + "Screenshots\\" + "screenshot-" + str(number)
        render.makeScreenshot(screenshot)

        # increment the index number and save it
        number += 1
        file = open(indexPath+indexFile,'w')
        file.write(str(number))
        file.write(noteToPlayer)

    except:
        # no index file, so create one
        file = open(indexPath+indexFile,'w')
        file.write(str(1))
        file.write(noteToPlayer)

        # append number to screenshot name and save the screenshot
        render = bge.render
        screenshot = "//" + "Screenshots\\" + "screenshot-0"
        render.makeScreenshot(screenshot)


########################################


# Save settings
def saveSettings():
    cont = logic.getCurrentController()
    own = cont.owner
    fileName = "settings.txt"
    
    # Prevent crash by not allowing resolution to be greater than the screen can use.
    scene = logic.getCurrentScene()
    settings = scene.objects["Controller"]
    if own["height"] > settings["desktopHeight"]:
        return
    
    file = open(path+fileName,'w')
    # Resolution
    file.write(str(own["width"]) + ',')
    file.write(str(own["height"]) + ',')
    
# Load settings
def loadSettings():
    cont = logic.getCurrentController()
    own = cont.owner
    fileName = "settings.txt"
    
    file = open(path+fileName,'r')
    line = file.readline().replace('\n','').split(',')
    
    # Resoultion
    own["width"] = int(line[0])
    own["height"] = int(line[1])
