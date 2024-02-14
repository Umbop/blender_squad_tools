import bpy
import bmesh

import random
import string

import os

def AddRig(RigObjectName):
    #append rig
    blendfile = os.path.dirname(os.path.abspath(__file__)) + "/BST_Resources.blend"
    section   = "\\Object\\"
    object    = RigObjectName

    filepath  = blendfile + section + object
    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(
        filepath=filepath, 
        filename=filename,
        directory=directory)
    
    #unlink boneshapes from view layer
    view_layer = bpy.context.view_layer
    view_layer_objects = view_layer.active_layer_collection.collection.objects
    for object in bpy.data.objects:
        if object.get('squad_rig_bone_shape') == 1 and object in view_layer_objects.values(): #check for custom properties 'squad_rig_bone_shape'
            view_layer_objects.unlink(object)

    #make new rig active and place it by 3d curor
    for object in bpy.context.selected_objects:
        view_layer.objects.active = object
        object.location = bpy.context.scene.cursor.location

class Squadrig_OT_Add_Control_Rig(bpy.types.Operator):
    bl_idname = "squadrig.add_control_rig"
    bl_label = "Squad Control Rig"
    bl_description = "Adds a Squad control rig to scene."

    def execute(self,context):
        
        AddRig("SQRig_FP_Camera")

        return {'FINISHED'}

class Squadrig_OT_Add_Weapon_Rig(bpy.types.Operator):
    bl_idname = "squadrig.add_weapon_rig"
    bl_label = "Squad Weapon Rig"
    bl_description = "Adds a Squad weapon rig to scene."

    def execute(self,context):

        AddRig("WeaponRoot")

        return {'FINISHED'}
