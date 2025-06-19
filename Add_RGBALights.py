# -----------------------------------
# Add_RGBA_Lights
#
# Description:
#   Select Arnold lights in the scene, add an RGBA AOV named after each light, 
#   and assign the light to that AOV group.
#
# Author: YCI-yves1122
# Copyright (c) 2023 YCI-yves1122
# License: MIT
# Repository: https://github.com/YCI-yves1122
# -----------------------------------

from maya import cmds
from mtoa.aovs import AOVInterface

#select lights and add RGBA_name of light and rename AOV lightgroup to name of node.

def add_RGBA_lights():
    
    aovs = AOVInterface()
    sl_node = cmds.ls(sl = True, type = "transform")
    
    if not sl_node:
        cmds.warning("no lights selected")
        return
    
    # lists acceptable light shapes
    for light in sl_node:
        shapes = cmds.listRelatives(light, shapes=True, type="aiAreaLight") or \
                 cmds.listRelatives(light, shapes=True, type="directionalLight") or \
                 cmds.listRelatives(light, shapes=True, type="aiSkyDomeLight") or \
                 cmds.listRelatives(light, shapes=True, type="aiPhotometricLight") or \
                 cmds.listRelatives(light, shapes=True, type="aiMeshLight") or []
        
        if not shapes:
            cmds.warning(f"{light} is not an Arnold light.")
            continue


        shape = shapes[0]

        if not cmds.objExists(f"{shape}.aiAov"):
            cmds.warning(f"{light} has no aiAov attribute.")
            continue

        # find the lightGroup shape
        light_group = cmds.getAttr(f"{shape}.aiAov")

        cmds.setAttr(f"{shape}.aiAov",f"{light}",type = "string")
        aov_name = f"RGBA_{light}"
        
        if not aovs.getAOVNode(aov_name):
            aovs.addAOV(aov_name)
        else:
            cmds.warning(f"{aov_name} already exists, skipping.")
        
        # sets data type to rgba
        aov_node = aovs.getAOVNode(aov_name)
        cmds.setAttr(f"{aov_node}.type", 6)
        
        

add_RGBA_lights()