# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Blender Squad Tools",
    "author" : "Umbop",
    "description" : "Tools to assist with mod development for OWI core.",
    "blender" : (2, 90, 0),
    "version" : (1, 2, 0),
    "location" : "View3D > Add > Armature and in the properties tab",
    "warning" : "",
    "wiki_url": "https://bit.ly/3uWu5DV",
    "tracker_url": "https://github.com/Umbop/blender_squad_tools/issues",
    "category" : "Animation"
}

import bpy

def update_action(self, value):
    if len(bpy.data.actions) !=0:
        ob = bpy.context.object
        
        #create anim data if there is none (stops an error)
        if ob.animation_data is None:
            ob.keyframe_insert(data_path='location',frame=0)
            bpy.data.actions.remove(ob.animation_data.action)
        
        #get selected action
        selected_action = bpy.data.actions[self["action_list_index"]]
        #apply selected action to armature
        ob.animation_data.action = selected_action
        
        #ob is character rig
        if selected_action.SquadLinkedAction in bpy.data.actions:
            #try:
            if(ob.get("squadrigtype") == 'character_control_rig'):
                weaponobject = getweapon()
                if weaponobject != None:
                    weaponobject.animation_data.action = bpy.data.actions[selected_action.SquadLinkedAction]
            
            #ob is weapon rig
            if getattachedsquadrig() is not None :
                characterrig = getattachedsquadrig()
                characterrig.animation_data.action = bpy.data.actions[selected_action.SquadLinkedAction]




#export props each object gets 
class SquadRigExportProperties(bpy.types.PropertyGroup):
    action_list_index : bpy.props.IntProperty(update=update_action)
    nla_track_index : bpy.props.IntProperty()
    export_name : bpy.props.StringProperty()

from . add_rig_ops import Squadrig_OT_Add_Control_Rig
from . add_rig_ops import Squadrig_OT_Add_Weapon_Rig

from . port_ops import Squadrig_OT_Export_Character_Animation
from . port_ops import Squadrig_OT_Import_Animation
from . port_ops import Squadrig_OT_Export_Animation
from . port_ops import Squadrig_OT_Import_Model
from . port_ops import Squadrig_OT_Import_Character_Animation
from . port_ops import Squadrig_OT_Export_Model

from . action_ops import SquadRig_OT_MarkForExport
from . action_ops import SquadRig_OT_UnmarkForExport
from . action_ops import SquadRig_OT_CreateAction
from . action_ops import SquadRig_OT_DeleteAction
from . action_ops import SquadRig_OT_DuplicateAction
from . action_ops import SquadRig_MT_NewActionMenu
from . action_ops import SquadRig_OT_LinkAction
from . action_ops import SquadRig_OT_AddFakeUser
from . action_ops import SquadRig_MT_LinkActionMenu


from . object_ops import SquadRig_OT_AttachToSquadRig
from . object_ops import SquadRig_OT_MakeCharacterSkin
from . object_ops import SquadRig_OT_RemoveCharacterSkin
from . object_ops import SquadRig_OT_DetachFromSquadRig
from . object_ops import SquadRig_OT_MakeChildOf
from . object_ops import SquadRig_OT_ChangeCharacterMesh
from . object_ops import SquadRig_MT_CharacterMeshSelector
from . object_ops import SquadRig_OT_DetachCharacterSkin
from . object_ops import SquadRig_OT_CreateRangingObject

from . pose_ops import SquadRig_OT_ApplyPose

from . lists import ACTION_UL_list
from . lists import NLA_UL_list

from . lists import CONTROLS_ACTION_UL_list
from . ui import SquadRig_PT_ToolsPanel
from . ui import SquadRig_PT_SquadRigControlsPanel
from . ui import SquadRig_PT_ExportPanel

from . dev_ops import SquadRig_PT_Dev_Panel
from . dev_ops import SquadRig_OT_ConvertToB1Droid
from . dev_ops import SquadRig_OT_FixAction
      

def getweapon():
    characterrig = bpy.context.object
    
    for object in bpy.data.objects:
        try:
            if(object.get("squadrigattachedtoid") == characterrig.get("squadrigid")):
                return object
        except (AttributeError, KeyError, TypeError):
            continue
    return None
        
def getattachedsquadrig():
    ob = bpy.context.object
    
    for constraint in ob.constraints:
            #make sure were getting the constraints we made before even if the user changed them slightly
            if constraint.type == "COPY_TRANSFORMS":
                if constraint.subtarget == "SUP_Weapon1_ATTACH" or constraint.name == "SQRig_attach":
                    return constraint.target
    return None

def control_rig_menu_func(self, context):
    self.layout.operator(Squadrig_OT_Add_Control_Rig.bl_idname,icon='MOD_ARMATURE')
def weapon_rig_menu_func(self, context):
    self.layout.operator(Squadrig_OT_Add_Weapon_Rig.bl_idname,icon='MODIFIER')

def register():
    print("squad rig tools register")
    bpy.utils.register_class(SquadRigExportProperties)
    bpy.types.Object.SquadRigExportProperties = bpy.props.PointerProperty(type=SquadRigExportProperties)
    bpy.types.Action.SquadLinkedAction = bpy.props.StringProperty()

    bpy.utils.register_class(SquadRig_OT_ApplyPose)
    
    bpy.utils.register_class(Squadrig_OT_Add_Control_Rig)
    bpy.utils.register_class(Squadrig_OT_Add_Weapon_Rig)
    bpy.utils.register_class(Squadrig_OT_Export_Character_Animation)
    bpy.utils.register_class(Squadrig_OT_Import_Animation)
    bpy.utils.register_class(Squadrig_OT_Import_Character_Animation)
    bpy.utils.register_class(Squadrig_OT_Export_Animation)
    bpy.utils.register_class(Squadrig_OT_Import_Model)
    bpy.utils.register_class(Squadrig_OT_Export_Model)
    bpy.utils.register_class(SquadRig_OT_AddFakeUser)
    bpy.utils.register_class(SquadRig_OT_DuplicateAction)
    bpy.utils.register_class(SquadRig_MT_NewActionMenu)

    bpy.utils.register_class(SquadRig_OT_MarkForExport)
    bpy.utils.register_class(SquadRig_OT_UnmarkForExport)
    bpy.utils.register_class(SquadRig_OT_CreateAction)
    bpy.utils.register_class(SquadRig_OT_DeleteAction)
    bpy.utils.register_class(SquadRig_MT_CharacterMeshSelector)
    bpy.utils.register_class(SquadRig_OT_LinkAction)
    bpy.utils.register_class(SquadRig_MT_LinkActionMenu)

    
    bpy.utils.register_class(SquadRig_OT_AttachToSquadRig)
    bpy.utils.register_class(SquadRig_OT_MakeCharacterSkin)
    bpy.utils.register_class(SquadRig_OT_RemoveCharacterSkin)
    bpy.utils.register_class(SquadRig_OT_DetachFromSquadRig)
    bpy.utils.register_class(SquadRig_OT_MakeChildOf)
    bpy.utils.register_class(SquadRig_OT_ChangeCharacterMesh)
    bpy.utils.register_class(SquadRig_OT_DetachCharacterSkin)
    bpy.utils.register_class(SquadRig_OT_CreateRangingObject)

    bpy.utils.register_class(CONTROLS_ACTION_UL_list)
    bpy.utils.register_class(ACTION_UL_list)
    bpy.utils.register_class(NLA_UL_list)

    bpy.utils.register_class(SquadRig_PT_SquadRigControlsPanel)
    bpy.utils.register_class(SquadRig_PT_ToolsPanel)
    bpy.utils.register_class(SquadRig_PT_ExportPanel)

    bpy.types.VIEW3D_MT_armature_add.append(control_rig_menu_func)
    bpy.types.VIEW3D_MT_armature_add.append(weapon_rig_menu_func)

    bpy.utils.register_class(SquadRig_OT_ConvertToB1Droid)
    bpy.utils.register_class(SquadRig_OT_FixAction)
    bpy.utils.register_class(SquadRig_PT_Dev_Panel)



def unregister():
    print("squad rig tools unregister")
    bpy.utils.unregister_class(SquadRig_PT_Dev_Panel)
    bpy.utils.unregister_class(SquadRig_OT_FixAction)
    bpy.utils.unregister_class(SquadRig_OT_ConvertToB1Droid)

    bpy.types.VIEW3D_MT_armature_add.remove(control_rig_menu_func)
    bpy.types.VIEW3D_MT_armature_add.remove(weapon_rig_menu_func)

    bpy.utils.unregister_class(SquadRig_PT_ToolsPanel)
    bpy.utils.unregister_class(SquadRig_PT_ExportPanel)
    bpy.utils.unregister_class(SquadRig_PT_SquadRigControlsPanel)


    bpy.utils.unregister_class(CONTROLS_ACTION_UL_list)
    bpy.utils.unregister_class(NLA_UL_list)
    bpy.utils.unregister_class(ACTION_UL_list)

    bpy.utils.unregister_class(SquadRig_OT_LinkAction)
    bpy.utils.unregister_class(SquadRig_MT_LinkActionMenu)
    bpy.utils.unregister_class(SquadRig_MT_NewActionMenu)
    bpy.utils.unregister_class(SquadRig_OT_MarkForExport)
    bpy.utils.unregister_class(SquadRig_OT_UnmarkForExport)
    bpy.utils.unregister_class(SquadRig_OT_CreateAction)
    bpy.utils.unregister_class(SquadRig_OT_DeleteAction)
    bpy.utils.unregister_class(SquadRig_OT_DuplicateAction)
    bpy.utils.unregister_class(SquadRig_OT_AddFakeUser)
    bpy.utils.unregister_class(SquadRig_MT_CharacterMeshSelector)
    
    bpy.utils.unregister_class(Squadrig_OT_Import_Character_Animation)
    bpy.utils.unregister_class(Squadrig_OT_Export_Character_Animation)
    bpy.utils.unregister_class(Squadrig_OT_Import_Animation)
    bpy.utils.unregister_class(Squadrig_OT_Export_Animation)
    bpy.utils.unregister_class(Squadrig_OT_Import_Model)
    bpy.utils.unregister_class(Squadrig_OT_Export_Model)
    bpy.utils.unregister_class(Squadrig_OT_Add_Control_Rig)
    bpy.utils.unregister_class(Squadrig_OT_Add_Weapon_Rig)
    
    bpy.utils.unregister_class(SquadRig_OT_CreateRangingObject)
    bpy.utils.unregister_class(SquadRig_OT_AttachToSquadRig)
    bpy.utils.unregister_class(SquadRig_OT_MakeCharacterSkin)
    bpy.utils.unregister_class(SquadRig_OT_RemoveCharacterSkin)
    bpy.utils.unregister_class(SquadRig_OT_DetachCharacterSkin)
    bpy.utils.unregister_class(SquadRig_OT_DetachFromSquadRig)
    bpy.utils.unregister_class(SquadRig_OT_MakeChildOf)
    bpy.utils.unregister_class(SquadRig_OT_ChangeCharacterMesh)

    bpy.utils.unregister_class(SquadRig_OT_ApplyPose)

    
    bpy.utils.unregister_class(SquadRigExportProperties)