'''
Loop Dipole and the Chaoties

Created by R. Bassett Jr.
www.tpot.ca

General Public Licence v3

---------------------
Sybox Camera

Based on a tutorial by ThaTimst3r
https://www.youtube.com/watch?v=TRpfJxnhFZ4
---------------------

Have the skybox camera move the same as the currently active camera.

'''
import bge

def update():
    cont = bge.logic.getCurrentController()
    scenelist = bge.logic.getSceneList()
    own = cont.owner

    # If the target scene blank, find it.
    if own['target'] == '':
        for i in scenelist:
            if 'Level1' in str(i):
                own['target'] = i
    else:
        cam = own['target'].active_camera
        own.worldOrientation = cam.worldOrientation
