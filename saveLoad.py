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

from bge import logic
path = logic.expandPath("//profiles/")


def setProfile():
    ## Store user selected profile
    cont = logic.getCurrentController()
    own = cont.owner
    file = open(path+'activeProfile.txt','w')
    profile = str(own['profile'])
    file.write(str(profile))


def getProfile():
    ## Read user selected profile
    file = open(path+'activeProfile.txt','r')
    line = file.readline().replace('\n','').split(',')
    return str(line[0])


### Puzzle Data ######################
def savePuzzle():
    cont = logic.getCurrentController()
    own = cont.owner
    
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
    
    fileName = own['fileName']
    
    ## Update path for the current profile
    profilePath = path + getProfile()
    
    file = open(profilePath+fileName+'.txt','r')
    
    line = file.readline().replace('\n','').split(',')
    
    own['p1Stage'] = int(line[0])
    own['p2Stage'] = int(line[1])
    own['p3Stage'] = int(line[2])
    own['p4Stage'] = int(line[3])
    own['p5Stage'] = int(line[4])

########################################



### Inventory Data ######################
def saveInventory():
    cont = logic.getCurrentController()
    own = cont.owner
    
    ## Update path for the current profile
    profilePath = path + getProfile()
    
    ## Make different files per level
    fileName = own['fileName']
    
    ## Set variables for easier human reading
    red = str(own['red']) + ','
    orange = str(own['orange']) + ','
    yellow = str(own['yellow']) + ','
    green = str(own['green']) + ','
    blue = str(own['blue']) + ','
    violet = str(own['violet']) + ','
    white = str(own['white']) + ','
    
    ## Open (or create) the file for writing
    file = open(profilePath+fileName+".txt", 'w')
    
    ## Write data, no line breaks are written   
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
    
    fileName = own['fileName']
    
    ## Update path for the current profile
    profilePath = path + getProfile()
    
    file = open(profilePath+fileName+'.txt','r')
    
    line = file.readline().replace('\n','').split(',')
    
    own['red'] = int(line[0])
    own['orange'] = int(line[1])
    own['yellow'] = int(line[2])
    own['green'] = int(line[3])
    own['blue'] = int(line[4])
    own['violet'] = int(line[5])
    own['white'] = int(line[6])

########################################



### Loadout Data ######################
'''
    It will be a while before I am at point where I can 
    write this section.
'''
########################################


    