if turbo = false and timer > cooldown
    turbo = true
    timer = 0
if turbo = true and timer < max duration
    apply the bonus speed
else
    turbo = false
    
    
    
                                         
            
            
            
            
                if logic.car["glideTimer"] < logic.car["glideCooldown"]:
                    logic.car["glideTimer"] = 0
                    for x in range(0, 30):
                        ## Apply upward and forward impulse
                        logic.car.linearVelocity[1] += logic.car["glideJumpY"]
                        logic.car.linearVelocity[2] += logic.car["glideJumpZ"] * (logic.car["speed"] / 200 + 1)
                else:
                    maintainGlide()
                    
                    
                    
                    
                    
                    
                    
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
    
    if logic.car["mouseControls"]:
        r.setMousePosition(h, w)
        logic.car["mouseControls"] = False
    elif logic.car["mouseSteering"]:
        ## Steer with the mouse when on the ground
        ## This is optional and off by default
        rot = logic.car.localOrientation.to_euler()
        # Yaw    
        yaw = math.degrees(rot[2]) + x
        rot[2] = math.radians(yaw)

        # Turn Wheels (use x > 0 or x < 0 for no mouse dead zone)
        if x < -1:
            # Right
            logic.car["steer"] -= 0.05
        if x > 1:
            # Left
            logic.car["steer"] += 0.05

        # Apply rotation
        logic.car.localOrientation = rot.to_matrix()

        # reset mouse for next frame and keep mouse in the game window
        r.setMousePosition(h, w)
    elif logic.car["gliding"] == True:
        rot = logic.car.localOrientation.to_euler()
        
        yaw = math.degrees(rot[2]) + x / 6
        rot[2] = math.radians(yaw)
        
        roll = math.degrees(rot[1]) + x * -1
        rot[1] = math.radians(roll)
        
        pitch = math.degrees(rot[0]) + y / 4
        rot[0] = math.radians(pitch)
        
        # Vector thrust based on shape stats
        if x < -0.25:
            # Right
            logic.car.linearVelocity[0] += logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 4
        if x > 0.25:
            # Left
            logic.car.linearVelocity[0] -= logic.car["glideJumpZ"]
            logic.car.linearVelocity[2] += logic.car["glideBonusZ"] / 4
        
        # Apply rotation
        logic.car.localOrientation = rot.to_matrix()

        # reset mouse for next frame and keep mouse in the game window
        r.setMousePosition(h, w)
    else: 
        r.setMousePosition(h, w)