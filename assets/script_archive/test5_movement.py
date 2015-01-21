# Character Abilities
# 
# R. Bassett Jr. www.tpot.ca
#############################


cont = bge.logic.getCurrentController()
own = cont.owner

# Actuators
move = cont.actuators["move"]

# Input
pressForward = cont.sensors["Forward"]
pressBackward = cont.sensors["Backward"]
pressStop = cont.sensors["Stop"]
pressTurbo = cont.sensors["Turbo"]

# Data
speed = move.dLoc[1]

# Move forward
if pressForward.positive:
    speed = 0.8
    # Turbo
    if pressTurbo.positive:
        speed = 1.4
    move.dLoc = [0.0, speed, 0.0]
    cont.activate(move)
# Slow down and reverse
elif pressBackward.positive:
    speed = speed - 0.1
    if speed < -0.3:
        speed = -0.3
    move.dLoc = [0.0, speed, 0.0]
    cont.activate(move)

# Stop
if pressStop.positive:
    speed = 0
    cont.deactivate(move)
    move.dLoc = [0.0, 0.0, 0.0]
        
        

