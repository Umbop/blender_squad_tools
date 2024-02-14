import bpy
import time
import math
from mathutils import Euler, Quaternion, Vector, Matrix
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator
from dataclasses import dataclass

from bpy_extras.io_utils import ExportHelper, ImportHelper

#used only in character animation import script (import_squad_character_animation)
@dataclass
class ImportAnimBone:
    new_bone: str
    original_bone: str
    translation_offset: Vector = (0.0,0.0,0.0)
    y_rot_offset: float = 0
    rotation_mode: str = "rotation_quaternion"
    #rotate_offset: Vector = (0.0,0.0,0.0)

'''


███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████ 
██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██      
█████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████ 
██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██ 
██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████ 
                                                                          
                                                                        
'''

def getattachedsquadrig():
    ob = bpy.context.object
    
    for constraint in ob.constraints:
            #make sure were getting the constraints we made before even if the user changed them slightly
            if constraint.type == "COPY_TRANSFORMS":
                if constraint.subtarget == "SUP_Weapon1_ATTACH" or constraint.name == "SQRig_attach":
                    return constraint.target
    return None

def is_squadrig_active():
    try:
        if(bpy.context.active_object.get("squadrigtype") == 'character_control_rig'):
            return True
    except (AttributeError, KeyError, TypeError):
        return False

#might be redundant
def create_export_pose():

    #creates a pose thats literally just the rest pose
    #the reason for doing so is because blender likes to bake the first frame of whatever its exporting right into the bindpose of what its exporting, completely destroying the animations
    #so for example it would bake the first frame of the basepose into the bind pose, causing all the other animations to break because theyre no longer playing on a properly A-posed character
    #this fixes it by making the rest pose the first action, so when it bakes the bone transforms in it just bakes in the rest pose, so kind of like a buffer action
    
    ob = bpy.context.object
    
    ob.animation_data.action = None
    
    for pose_bone in ob.pose.bones:
        #reset bone transforms
        pose_bone.location = (0,0,0)
        pose_bone.rotation_euler = Euler((0, 0, 0), 'XYZ')
        pose_bone.rotation_quaternion = (1, 0, 0, 0)
        pose_bone.scale = (1,1,1)
        #keyframe the reset transforms
        pose_bone.keyframe_insert(data_path='rotation_euler',frame=-1)
        pose_bone.keyframe_insert(data_path='rotation_quaternion',frame=-1)
        pose_bone.keyframe_insert(data_path='location',frame=-1)
        pose_bone.keyframe_insert(data_path='scale',frame=-1)
        #disable the constraints
        for constraint in pose_bone.constraints:
            constraint.mute = True
            constraint.keyframe_insert("mute")
    #set the name
    ob.animation_data.action.name = "temp_EXPORTPOSE"

    return ob.animation_data.action

'''
██ ███    ███ ██████   ██████  ██████  ████████      █████  ███    ██ ██ ███    ███  █████  ████████ ██  ██████  ███    ██ 
██ ████  ████ ██   ██ ██    ██ ██   ██    ██        ██   ██ ████   ██ ██ ████  ████ ██   ██    ██    ██ ██    ██ ████   ██ 
██ ██ ████ ██ ██████  ██    ██ ██████     ██        ███████ ██ ██  ██ ██ ██ ████ ██ ███████    ██    ██ ██    ██ ██ ██  ██ 
██ ██  ██  ██ ██      ██    ██ ██   ██    ██        ██   ██ ██  ██ ██ ██ ██  ██  ██ ██   ██    ██    ██ ██    ██ ██  ██ ██ 
██ ██      ██ ██       ██████  ██   ██    ██        ██   ██ ██   ████ ██ ██      ██ ██   ██    ██    ██  ██████  ██   ████ 
'''                                                                                                                        
                                                                                                                           



#gets called when you import
def import_squad_character_animation(self, context, filepath, delete_root_motion, delete_imported_armature):
    start_time = time.time()

    selected_ob = bpy.context.object
    
    pre_import_actions = []
    for action in bpy.data.actions:
        pre_import_actions.append(action)

    bpy.ops.import_scene.fbx(
    filepath = filepath,
    primary_bone_axis = 'X',
    secondary_bone_axis= 'Z'
    )

    new_actions = []
    for action in bpy.data.actions:
        if action not in pre_import_actions:
            #action is new
            new_actions.append(action)
            action.name = action.name.split("|",15)[len(action.name.split("|",15))-1]

    #if no new actions just exit function, theres nothing here for us :p
    if len(new_actions) == 0:
        self.report({'WARNING'}, "No animations in imported file.")
        return {'FINISHED'}
    elif len(new_actions) == 1:
        #if theres just one animation then name the action after the FBX file it was imported from
        new_actions[0].name = filepath.split("\\",15)[len(filepath.split("\\",15))-1][:-4]


    #get imported objects
    for object in bpy.context.selected_objects:
        #if object isnt an armature delete it
        if object.type != "ARMATURE":
            bpy.data.objects.remove(object, do_unlink=True)
            continue

        bones = object.pose.bones
        editbones =  object.data.edit_bones
        if "Bip01" in bones: #check if squad rig
            
            #prep the rig by adding the control bones
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            
            new_bone = editbones.new("CON_HandController_R")
            new_bone.head = (-46.7316, -8.5214, 98.2337)
            new_bone.tail = (-51.3532, -14.6657, 85.3538)
            new_bone.roll =-4.6889262199401855
            new_bone = editbones.new("CON_Finger0_R")
            new_bone.head = (-45.6527, -12.2053, 96.4872)
            new_bone.tail = (-44.6247, -13.8024, 94.3921)
            new_bone.roll =-1.226935625076294
            new_bone.parent = editbones["CON_HandController_R"]
            new_bone = editbones.new("CON_Finger01_R")
            new_bone.head = (-44.6247, -13.8024, 94.3921)
            new_bone.tail = (-44.0841, -14.7588, 91.4930)
            new_bone.roll =-0.8334141969680786
            new_bone.parent = editbones["CON_Finger0_R"]
            new_bone = editbones.new("CON_Finger02_R")
            new_bone.head = (-44.0841, -14.7588, 91.4930)
            new_bone.tail = (-43.4745, -15.9946, 89.1897)
            new_bone.roll =-0.9325141310691833
            new_bone.parent = editbones["CON_Finger01_R"]
            new_bone = editbones.new("CON_Finger1_R")
            new_bone.head = (-48.8526, -14.3876, 90.8003)
            new_bone.tail = (-49.3074, -15.5071, 87.9141)
            new_bone.roll =1.3348966836929321
            new_bone.parent = editbones["CON_HandController_R"]
            new_bone = editbones.new("CON_Finger11_R")
            new_bone.head = (-49.3074, -15.5071, 87.9141)
            new_bone.tail = (-48.7637, -15.9411, 85.6390)
            new_bone.roll =0.8363486528396606
            new_bone.parent = editbones["CON_Finger1_R"]
            new_bone = editbones.new("CON_Finger12_R")
            new_bone.head = (-48.7637, -15.9411, 85.6390)
            new_bone.tail = (-48.0640, -16.2008, 83.6762)
            new_bone.roll =0.7118951082229614
            new_bone.parent = editbones["CON_Finger11_R"]
            new_bone = editbones.new("CON_Finger2_R")
            new_bone.head = (-49.8975, -12.3649, 90.0702)
            new_bone.tail = (-50.1028, -13.4848, 86.4433)
            new_bone.roll =1.4863234758377075
            new_bone.parent = editbones["CON_HandController_R"]
            new_bone = editbones.new("CON_Finger21_R")
            new_bone.head = (-50.1028, -13.4848, 86.4433)
            new_bone.tail = (-49.7508, -14.2419, 83.7196)
            new_bone.roll =1.2492517232894897
            new_bone.parent = editbones["CON_Finger2_R"]
            new_bone = editbones.new("CON_Finger22_R")
            new_bone.head = (-49.7508, -14.2419, 83.7196)
            new_bone.tail = (-49.1490, -14.7023, 81.8483)
            new_bone.roll =1.0213693380355835
            new_bone.parent = editbones["CON_Finger21_R"]
            new_bone = editbones.new("CON_Finger3_R")
            new_bone.head = (-50.2956, -10.1475, 89.8140)
            new_bone.tail = (-50.1982, -11.1315, 86.5927)
            new_bone.roll =1.3880060911178589
            new_bone.parent = editbones["CON_HandController_R"]
            new_bone = editbones.new("CON_Finger31_R")
            new_bone.head = (-50.1982, -11.1315, 86.5927)
            new_bone.tail = (-49.2957, -11.6782, 84.3880)
            new_bone.roll =0.9361737966537476
            new_bone.parent = editbones["CON_Finger3_R"]
            new_bone = editbones.new("CON_Finger32_R")
            new_bone.head = (-49.2957, -11.6782, 84.3880)
            new_bone.tail = (-48.4419, -12.1134, 82.5669)
            new_bone.roll =0.8755220174789429
            new_bone.parent = editbones["CON_Finger31_R"]
            new_bone = editbones.new("CON_Finger4_R")
            new_bone.head = (-49.8851, -8.0214, 89.7819)
            new_bone.tail = (-49.5905, -8.8439, 87.0075)
            new_bone.roll =1.4554485082626343
            new_bone.parent = editbones["CON_HandController_R"]
            new_bone = editbones.new("CON_Finger41_R")
            new_bone.head = (-49.5905, -8.8439, 87.0075)
            new_bone.tail = (-48.9489, -9.2573, 85.6747)
            new_bone.roll =1.0340300798416138
            new_bone.parent = editbones["CON_Finger4_R"]
            new_bone = editbones.new("CON_Finger42_R")
            new_bone.head = (-48.9489, -9.2573, 85.6747)
            new_bone.tail = (-48.1950, -9.6886, 84.2952)
            new_bone.roll =0.9687179327011108
            new_bone.parent = editbones["CON_Finger41_R"]
            new_bone = editbones.new("CON_HandController_L")
            new_bone.head = (46.7316, -8.5214, 98.2337)
            new_bone.tail = (51.3532, -14.6657, 85.3538)
            new_bone.roll =4.6889262199401855
            new_bone = editbones.new("CON_Finger0_L")
            new_bone.head = (45.6527, -12.2051, 96.4872)
            new_bone.tail = (44.6248, -13.8022, 94.3922)
            new_bone.roll =1.2269269227981567
            new_bone.parent = editbones["CON_HandController_L"]
            new_bone = editbones.new("CON_Finger01_L")
            new_bone.head = (44.6248, -13.8022, 94.3922)
            new_bone.tail = (44.0842, -14.7586, 91.4930)
            new_bone.roll =0.8334070444107056
            new_bone.parent = editbones["CON_Finger0_L"]
            new_bone = editbones.new("CON_Finger02_L")
            new_bone.head = (44.0842, -14.7586, 91.4930)
            new_bone.tail = (43.4746, -15.9944, 89.1898)
            new_bone.roll =0.93250572681427
            new_bone.parent = editbones["CON_Finger01_L"]
            new_bone = editbones.new("CON_Finger1_L")
            new_bone.head = (48.8527, -14.3874, 90.8004)
            new_bone.tail = (49.3075, -15.5069, 87.9142)
            new_bone.roll =-1.3349049091339111
            new_bone.parent = editbones["CON_HandController_L"]
            new_bone = editbones.new("CON_Finger11_L")
            new_bone.head = (49.3075, -15.5069, 87.9142)
            new_bone.tail = (48.7638, -15.9409, 85.6391)
            new_bone.roll =-0.8363556265830994
            new_bone.parent = editbones["CON_Finger1_L"]
            new_bone = editbones.new("CON_Finger12_L")
            new_bone.head = (48.7638, -15.9409, 85.6391)
            new_bone.tail = (48.0641, -16.2006, 83.6762)
            new_bone.roll =-0.7119016051292419
            new_bone.parent = editbones["CON_Finger11_L"]
            new_bone = editbones.new("CON_Finger2_L")
            new_bone.head = (49.8975, -12.3646, 90.0702)
            new_bone.tail = (50.1029, -13.4845, 86.4433)
            new_bone.roll =-1.4863309860229492
            new_bone.parent = editbones["CON_HandController_L"]
            new_bone = editbones.new("CON_Finger21_L")
            new_bone.head = (50.1029, -13.4845, 86.4433)
            new_bone.tail = (49.7509, -14.2416, 83.7196)
            new_bone.roll =-1.2492588758468628
            new_bone.parent = editbones["CON_Finger2_L"]
            new_bone = editbones.new("CON_Finger22_L")
            new_bone.head = (49.7509, -14.2416, 83.7196)
            new_bone.tail = (49.1491, -14.7021, 81.8484)
            new_bone.roll =-1.0213758945465088
            new_bone.parent = editbones["CON_Finger21_L"]
            new_bone = editbones.new("CON_Finger3_L")
            new_bone.head = (50.2956, -10.1473, 89.8141)
            new_bone.tail = (50.1983, -11.1312, 86.5928)
            new_bone.roll =-1.3880137205123901
            new_bone.parent = editbones["CON_HandController_L"]
            new_bone = editbones.new("CON_Finger31_L")
            new_bone.head = (50.1983, -11.1312, 86.5928)
            new_bone.tail = (49.2957, -11.6780, 84.3881)
            new_bone.roll =-0.936180055141449
            new_bone.parent = editbones["CON_Finger3_L"]
            new_bone = editbones.new("CON_Finger32_L")
            new_bone.head = (49.2957, -11.6780, 84.3881)
            new_bone.tail = (48.4420, -12.1132, 82.5670)
            new_bone.roll =-0.8755280375480652
            new_bone.parent = editbones["CON_Finger31_L"]
            new_bone = editbones.new("CON_Finger4_L")
            new_bone.head = (49.8852, -8.0211, 89.7820)
            new_bone.tail = (49.5905, -8.8437, 87.0075)
            new_bone.roll =-1.4554561376571655
            new_bone.parent = editbones["CON_HandController_L"]
            new_bone = editbones.new("CON_Finger41_L")
            new_bone.head = (49.5905, -8.8437, 87.0075)
            new_bone.tail = (48.9490, -9.2571, 85.6747)
            new_bone.roll =-1.0340368747711182
            new_bone.parent = editbones["CON_Finger4_L"]
            new_bone = editbones.new("CON_Finger42_L")
            new_bone.head = (48.9490, -9.2571, 85.6747)
            new_bone.tail = (48.1951, -9.6884, 84.2953)
            new_bone.roll =-0.9687245488166809
            new_bone.parent = editbones["CON_Finger41_L"]
            new_bone = editbones.new("CON_FootController_R")
            new_bone.head = (-16.0214, 4.7825, 10.1650)
            new_bone.tail = (-16.0991, 4.4359, -9.8319)
            new_bone.roll =3.596271514892578
            new_bone = editbones.new("CON_FootController_L")
            new_bone.head = (16.0214, 4.7825, 10.1650)
            new_bone.tail = (16.0991, 4.4359, -9.8319)
            new_bone.roll =-9.879457473754883


            new_bone = editbones.new("CON_Toe_L")
            new_bone.head = (21.9982, -7.5605, 0.4333)
            new_bone.tail = (25.6493, -15.1032, 0.2398)
            
            new_bone.parent = editbones["CON_FootController_L"]
            new_bone.roll = editbones["Bip01_L_Toe0"].roll
            new_bone = editbones.new("CON_Toe_R")
            new_bone.head = (-21.9982, -7.6598, 0.4333)
            new_bone.tail = (-25.6493, -15.2031, 0.3847)
            new_bone.parent = editbones["CON_FootController_R"]
            new_bone.roll = editbones["Bip01_R_Toe0"].roll

            new_bone = editbones.new("CON_HandPole_R")
            new_bone.head = (-37.1059, 22.7652, 106.1376)
            new_bone.tail = (-41.1467, 45.0740, 91.3062)
            new_bone.roll =-5.747838020324707
            new_bone = editbones.new("CON_HandPole_L")
            new_bone.head = (37.1059, 22.7652, 106.1376)
            new_bone.tail = (41.1467, 45.0740, 91.3062)
            new_bone.roll =-0.5353477001190186
            new_bone = editbones.new("CON_FootPole_L")
            new_bone.head = (27.2263, -47.4057, 45.2025)
            new_bone.tail = (38.4660, -85.2847, 41.6700)
            new_bone.roll =0.7004109621047974
            new_bone = editbones.new("CON_FootPole_R")
            new_bone.head = (-27.2263, -47.4057, 45.2025)
            new_bone.tail = (-38.4660, -85.2847, 41.6700)
            new_bone.roll =-0.700411319732666
            new_bone = editbones.new("CON_SpineRoot")
            new_bone.head = (0.0000, 0.0000, 89.2365)
            new_bone.tail = (-0.2144, 0.5688, 108.5324)
            new_bone.roll =-0.005491495132446289
            new_bone = editbones.new("CON_PelvisController")
            new_bone.head = (0.0000, 0.0000, 89.2365)
            new_bone.tail = (-0.1650, 0.4375, 104.0796)
            new_bone.roll =-0.005491495132446289
            new_bone.parent = editbones["CON_SpineRoot"]
            new_bone = editbones.new("CON_SpineController")
            new_bone.head = (-0.0000, 2.8327, 131.7525)
            new_bone.tail = (-0.0000, 4.2921, 146.6814)
            new_bone.roll =-1.1920928955078125e-06
            new_bone.parent = editbones["CON_SpineRoot"]
            new_bone = editbones.new("CON_Neck")
            new_bone.head = (-0.0000, 3.2140, 151.7249)
            new_bone.tail = (-0.0000, 0.7551, 158.2003)
            new_bone.roll =3.5762786865234375e-07
            new_bone.parent = editbones["CON_SpineController"]
            new_bone = editbones.new("CON_Head")
            new_bone.head = (-0.0000, 0.7551, 158.2003)
            new_bone.tail = (-0.0000, -1.3043, 171.6651)
            new_bone.roll =-3.5762786865234375e-07
            new_bone.parent = editbones["CON_Neck"]
            new_bone = editbones.new("CON_Clavicle_R")
            new_bone.head = (-7.2822, 4.0076, 145.5279)
            new_bone.tail = (-21.0371, 4.0074, 142.3915)
            new_bone.roll =1.447348713874817
            new_bone.parent = editbones["CON_SpineController"]
            new_bone = editbones.new("CON_Clavicle_L")
            new_bone.head = (7.2822, 4.0077, 145.5280)
            new_bone.tail = (21.0371, 4.0075, 142.3915)
            new_bone.roll =-1.4473508596420288
            new_bone.parent = editbones["CON_SpineController"]
            new_bone = editbones.new("CON_WeaponController")
            new_bone.head = (-0.0000, 2.8327, 131.7526)
            new_bone.tail = (-0.0000, -47.1673, 131.7526)
            new_bone.roll =0.0
            new_bone = editbones.new("CON_WeaponHandController_R")
            new_bone.head = (-10.0000, 2.8327, 131.7526)
            new_bone.tail = (-10.0000, -22.1673, 131.7526)
            new_bone.roll =-1.5707956552505493
            new_bone.parent = editbones["CON_WeaponController"]
            new_bone = editbones.new("CON_WeaponHandController_L")
            new_bone.head = (10.0000, 2.8327, 131.7526)
            new_bone.tail = (10.0000, -22.1673, 131.7526)
            new_bone.roll =-4.712389945983887
            new_bone.parent = editbones["CON_WeaponController"]
            new_bone = editbones.new("CON_Camera")
            new_bone.head = (4.5669, 6.4197, 135.6715)
            new_bone.tail = (4.5669, -1.9427, 135.6715)
            new_bone.roll =0.0
            
            #align and bake control bones
            bpy.ops.object.mode_set(mode='POSE', toggle=False)
            #current_action = object.animation_data.action
            #change rotation modes for pose mode
            object.pose.bones["CON_WeaponController"].rotation_mode = "XYZ"
            object.pose.bones["CON_Camera"].rotation_mode = "XYZ"

            align_bones = [
                ImportAnimBone("CON_HandController_R", "Bip01_R_Hand"),
                ImportAnimBone("CON_HandController_R", "Bip01_R_Hand"),
                ImportAnimBone("CON_HandController_L", "Bip01_L_Hand"),
                ImportAnimBone("CON_HandPole_L", "Bip01_L_Forearm", (0, -20, 20)),
                ImportAnimBone("CON_HandPole_R", "Bip01_R_Forearm", (0, -20, 20)),
                ImportAnimBone("CON_FootPole_L", "Bip01_L_Calf", (0, -20, 20)),
                ImportAnimBone("CON_FootPole_R", "Bip01_R_Calf", (0, -20, 20)),
                ImportAnimBone("CON_FootController_R", "Bip01_R_Foot"),
                ImportAnimBone("CON_FootController_L", "Bip01_L_Foot",(0,0,0)),
                ImportAnimBone("CON_WeaponController","Bip01_Weapon1",(0,0,0),90,"rotation_euler"),
                ImportAnimBone("CON_SpineRoot", "Bip01_Pelvis"),
                ImportAnimBone("CON_Camera", "Bip01_CameraBone",(0,0,0),90,"rotation_euler"),
                ]

            align_bones_1 = [
                ImportAnimBone("CON_WeaponHandController_R","Bip01_R_Hand"),
                ImportAnimBone("CON_WeaponHandController_L","Bip01_L_Hand",(0,0,0)),
                ImportAnimBone("CON_SpineController","Bip01_Spine2"),
                ImportAnimBone('CON_Finger0_R','Bip01_R_Finger0'),
                ImportAnimBone('CON_Finger1_R','Bip01_R_Finger1'),
                ImportAnimBone('CON_Finger2_R','Bip01_R_Finger2'),
                ImportAnimBone('CON_Finger3_R','Bip01_R_Finger3'),
                ImportAnimBone('CON_Finger4_R','Bip01_R_Finger4'),
                ImportAnimBone('CON_Finger0_L','Bip01_L_Finger0'),
                ImportAnimBone('CON_Finger1_L','Bip01_L_Finger1'),
                ImportAnimBone('CON_Finger2_L','Bip01_L_Finger2'),
                ImportAnimBone('CON_Finger3_L','Bip01_L_Finger3'),
                ImportAnimBone('CON_Finger4_L','Bip01_L_Finger4'),
                ImportAnimBone("CON_Toe_L", "Bip01_L_Toe0"),
                ImportAnimBone("CON_Toe_R", "Bip01_R_Toe0"),
                ]

            align_bones_2 = [
                ImportAnimBone("CON_Neck","Bip01_Neck"),
                ImportAnimBone("CON_Clavicle_R", "Bip01_R_Clavicle"),
                ImportAnimBone("CON_Clavicle_L", "Bip01_L_Clavicle"),
                ImportAnimBone('CON_Finger01_R','Bip01_R_Finger01'),
                ImportAnimBone('CON_Finger11_R','Bip01_R_Finger11'),
                ImportAnimBone('CON_Finger21_R','Bip01_R_Finger21'),
                ImportAnimBone('CON_Finger31_R','Bip01_R_Finger31'),
                ImportAnimBone('CON_Finger41_R','Bip01_R_Finger41'),
                ImportAnimBone('CON_Finger01_L','Bip01_L_Finger01'),
                ImportAnimBone('CON_Finger11_L','Bip01_L_Finger11'),
                ImportAnimBone('CON_Finger21_L','Bip01_L_Finger21'),
                ImportAnimBone('CON_Finger31_L','Bip01_L_Finger31'),
                ImportAnimBone('CON_Finger41_L','Bip01_L_Finger41'),
                ]
            align_bones_3 = [
                ImportAnimBone("CON_Head","Bip01_Head"),
                ImportAnimBone('CON_Finger02_R','Bip01_R_Finger02'),
                ImportAnimBone('CON_Finger12_R','Bip01_R_Finger12'),
                ImportAnimBone('CON_Finger22_R','Bip01_R_Finger22'),
                ImportAnimBone('CON_Finger32_R','Bip01_R_Finger32'),
                ImportAnimBone('CON_Finger42_R','Bip01_R_Finger42'),
                ImportAnimBone('CON_Finger02_L','Bip01_L_Finger02'),
                ImportAnimBone('CON_Finger12_L','Bip01_L_Finger12'),
                ImportAnimBone('CON_Finger22_L','Bip01_L_Finger22'),
                ImportAnimBone('CON_Finger32_L','Bip01_L_Finger32'),
                ImportAnimBone('CON_Finger42_L','Bip01_L_Finger42'),
                ]

            align_iterations = [align_bones, align_bones_1, align_bones_2, align_bones_3]

            for action in new_actions:
                
                if delete_root_motion == True:
                    #find group with "Root" in name as its the action group with the object keyframes in it
                    #and delete specifically the location, rotation and scale keyframes
                    fcurves = action.fcurves
                    for group in action.groups:
                        if "Root" in group.name:
                            for c in fcurves:
                                if c.data_path == "location" or c.data_path == "rotation_euler" or c.data_path == "scale":
                                    fcurves.remove(c)

                object.animation_data.action = action

                for frame in range(int(action.frame_range[0]),(round(action.frame_range[1]+1))):
                    #set frame
                    bpy.context.scene.frame_set(frame)
                    #align all bones
                    for align_iteration in align_iterations:

                        for bone in align_iteration:
                            og_bone = bones[bone.original_bone]
                            new_bone = bones[bone.new_bone]

                            mat_trans = Matrix.Translation(bone.translation_offset)
                            mat_rot = Matrix.Rotation(math.radians(bone.y_rot_offset), 4, 'Y')

                            new_bone.matrix = og_bone.matrix @ mat_trans @ mat_rot
                            

                            new_bone.keyframe_insert("location",  frame=frame, group = bone.original_bone)
                            new_bone.keyframe_insert(bone.rotation_mode,  frame=frame, group = bone.original_bone)
                            #new_bone.keyframe_insert("rotation_euler",  frame=frame, group = bone.original_bone)
                            new_bone.keyframe_insert("scale",  frame=frame, group = bone.original_bone)
                        
                        bpy.context.view_layer.update()

        
        #delete imported armature
        if delete_imported_armature:
            bpy.data.objects.remove(object, do_unlink=True)
            
    #reselect original object
    selected_ob.select_set(True)
    

    bpy.context.view_layer.objects.active = selected_ob
    
    end_time = time.time()
    #print("imported in: " + str(end_time - start_time) + " seconds")
    self.report({'INFO'}, "Imported in:" + str(end_time - start_time) + " seconds.")

    return {'FINISHED'}

def import_squad_animation(self, context, filepath, delete_root_motion, bone_primary_axis, bone_secondary_axis, delete_imported_armature):
    start_time = time.time()

    selected_ob = bpy.context.object
    
    pre_import_actions = []
    for action in bpy.data.actions:
        pre_import_actions.append(action)

    bpy.ops.import_scene.fbx(
    filepath = filepath,
    primary_bone_axis = bone_primary_axis,
    secondary_bone_axis= bone_secondary_axis
    )

    new_actions = []
    for action in bpy.data.actions:
        if action not in pre_import_actions:
            #action is new
            new_actions.append(action)
            action.name = action.name.split("|",15)[len(action.name.split("|",15))-1]

    #if no new actions just exit function, theres nothing here for us :p
    if len(new_actions) == 0:
        self.report({'WARNING'}, "No animations in imported file.")
        return {'FINISHED'}
    elif len(new_actions) == 1:
        #if theres just one animation then name the action after the FBX file it was imported from
        new_actions[0].name = filepath.split("\\",15)[len(filepath.split("\\",15))-1][:-4]

    #get imported objects
    if delete_imported_armature:
        for object in bpy.context.selected_objects:
            bpy.data.objects.remove(object, do_unlink=True)

    end_time = time.time()
    #print("imported in: " + str(end_time - start_time) + " seconds")
    self.report({'INFO'}, "Imported in:" + str(end_time - start_time) + " seconds.")

    return {'FINISHED'}


'''
███████ ██   ██ ██████   ██████  ██████  ████████      █████  ███    ██ ██ ███    ███  █████  ████████ ██  ██████  ███    ██ 
██       ██ ██  ██   ██ ██    ██ ██   ██    ██        ██   ██ ████   ██ ██ ████  ████ ██   ██    ██    ██ ██    ██ ████   ██ 
█████     ███   ██████  ██    ██ ██████     ██        ███████ ██ ██  ██ ██ ██ ████ ██ ███████    ██    ██ ██    ██ ██ ██  ██ 
██       ██ ██  ██      ██    ██ ██   ██    ██        ██   ██ ██  ██ ██ ██ ██  ██  ██ ██   ██    ██    ██ ██    ██ ██  ██ ██ 
███████ ██   ██ ██       ██████  ██   ██    ██        ██   ██ ██   ████ ██ ██      ██ ██   ██    ██    ██  ██████  ██   ████ 
                                                                                                                                                                                                                                                    
'''

def export_squad_character_animation(self, context, filepath, visual_bake_actions, force_center_object, match_linked_length, force_lock_foot_root, simplify_factor):
    start_time = time.time()
    
    #get object
    ob = context.object
    bones = ob.pose.bones

    #select only squad rig
    for object in bpy.context.selected_objects:
            object.select_set(False)
    ob.select_set(True)
    
    object_named_root = None
    ob_old_name = ob.name
    for object in bpy.data.objects:
        if object.name == "Root":
            object.name = "Root_temp_new_name"
            object_named_root = object
    ob.name = "Root"

    if force_center_object:
        loc_constraint = ob.constraints.new('LIMIT_LOCATION')
        loc_constraint.name = "EXPORT_CONSTRAINT_LOCATION"
        loc_constraint.use_min_x = True
        loc_constraint.use_min_y = True
        loc_constraint.use_min_z = True
        loc_constraint.use_max_x = True
        loc_constraint.use_max_y = True
        loc_constraint.use_max_z = True
        loc_constraint.use_transform_limit = True

        rot_constraint = ob.constraints.new('LIMIT_ROTATION')
        rot_constraint.name = "EXPORT_CONSTRAINT_ROTATION"

        rot_constraint.min_z = 1.57079632679
        rot_constraint.max_z = 1.57079632679

        rot_constraint.use_limit_x = True
        rot_constraint.use_limit_y = True
        rot_constraint.use_limit_z = True
        rot_constraint.use_transform_limit = True

        sca_constraint = ob.constraints.new('LIMIT_SCALE')
        sca_constraint.name = "EXPORT_CONSTRAINT_SCALE"

        sca_constraint.min_x = 0.01
        sca_constraint.min_y = 0.01
        sca_constraint.min_z = 0.01
        sca_constraint.max_x = 0.01
        sca_constraint.max_y = 0.01
        sca_constraint.max_z = 0.01
        sca_constraint.use_min_x = True
        sca_constraint.use_min_y = True
        sca_constraint.use_min_z = True
        sca_constraint.use_max_x = True
        sca_constraint.use_max_y = True
        sca_constraint.use_max_z = True
        sca_constraint.use_transform_limit = True

    #keep track of pre export values so we can apply them again post export
    old_frame_current = bpy.context.scene.frame_current
   
    #reset the head scalar so the head is normal sized
    old_head_scale = ob.pose.bones["CON_Head"].constraints["Limit Scale"].influence
    ob.pose.bones["CON_Head"].constraints["Limit Scale"].influence = 0
    #remember the current action so we can change back to it
    old_action = ob.animation_data.action
    
    

    #iterate through NLA strips and convert each one to the squad nameing convention
    #also key all constraints
    for nlatrack in ob.animation_data.nla_tracks:
        if "BST_ExportTrack" in nlatrack.name:
            nlatrack.mute = False #make sure we're only exporting tracks marked for export
        ob.animation_data.action = nlatrack.strips[0].action #set track action as active so we can mess with it below
        
        bpy.context.scene.frame_set(int(nlatrack.strips[0].action.frame_range[0]))

        ob.rotation_euler = Euler((0, 0, 1.570796326794896619231), 'XYZ')#make rig face X+
        #ob.keyframe_insert("rotation_euler")
        ob.location = (0,0,0)
        #ob.keyframe_insert("location")
        ob.scale = (0.01,0.01,0.01)
        #ob.keyframe_insert("scale")
            
        nlatrack.strips[0].frame_start = nlatrack.strips[0].action.frame_range[0]
        nlatrack.strips[0].frame_end = nlatrack.strips[0].action.frame_range[1]
        #renaming the bones renames the fcurves
        for bone in bpy.context.object.pose.bones:
            #make sure all constraints are keyed
            for constraint in bone.constraints:
                constraint.mute = False
                constraint.keyframe_insert("mute")
    
    #lock footroot
    if force_lock_foot_root:
        foot_root_constraint = ob.pose.bones["IK_Feet_Root"].constraints.new("LIMIT_ROTATION")
        foot_root_constraint.name = "EXPORT_CONSTRAINT_ROTATION"
        foot_root_constraint.min_z = -1.57079632679
        foot_root_constraint.max_z = -1.57079632679

        foot_root_constraint.min_y = -1.57079632679
        foot_root_constraint.max_y = -1.57079632679

        foot_root_constraint.use_limit_x = True
        foot_root_constraint.use_limit_y = True
        foot_root_constraint.use_limit_z = True
        foot_root_constraint.use_transform_limit = True
        
    #setup export pose
    export_pose = create_export_pose()
    
    #make sure the constaint stays on
    if force_lock_foot_root:
        foot_root_constraint.mute = False
        foot_root_constraint.keyframe_insert("mute")
    
    #do the export
    bpy.ops.export_scene.fbx(
    filepath=filepath,
    use_selection = True,
    add_leaf_bones=False,
    use_armature_deform_only = True,
    bake_anim_use_all_actions=False,
    primary_bone_axis = 'X',
    secondary_bone_axis= 'Z',
    bake_anim_simplify_factor=simplify_factor
    )
    #revert all temporary changes made at the start

    for nlatrack in ob.animation_data.nla_tracks:
        nlatrack.mute = True
        ob.animation_data.action = nlatrack.strips[0].action

    #remove exportpose
    bpy.data.actions.remove(export_pose)
        
    ob.animation_data.action = old_action
    ob.pose.bones["CON_Head"].constraints["Limit Scale"].influence = old_head_scale
    ob.pose.bones["CON_Head"].constraints["Limit Scale"].mute = False
    bpy.context.scene.frame_set(old_frame_current)

    if object_named_root is not None:
        object_named_root.name = "Root"
    ob.name = ob_old_name
    
    #remove constraint
    if force_lock_foot_root:
        ob.pose.bones["IK_Feet_Root"].constraints.remove(foot_root_constraint)

    if force_center_object:
        ob.constraints.remove(loc_constraint)
        ob.constraints.remove(rot_constraint)
        ob.constraints.remove(sca_constraint)

    end_time = time.time()
    self.report({'INFO'}, "Exported in: " + str(end_time - start_time) + " seconds.")

    return {'FINISHED'}

def export_weapon_animation(self, context, filepath, visual_bake_actions, force_center_object, match_linked_length, simplify_factor, bone_primary_axis, bone_secondary_axis, object_export_name):
    start_time = time.time()
    
    #get object
    ob = context.object
    bones = ob.pose.bones
    
    #select only squad rig
    for object in bpy.context.selected_objects:
            object.select_set(False)
    ob.select_set(True)

    #temp rename
    if object_export_name != "":
        object_named_root = None
        ob_old_name = ob.name
        for object in bpy.data.objects:
            if object.name == object_export_name:
                object.name = object.name + "_temp_rename_for_export"
                object_named_root = object
        ob.name = object_export_name

    
    
    
    old_frame_current = bpy.context.scene.frame_current #remember what frame we're on so we can set it back to that after the export
    bpy.context.scene.frame_set(0) #set frame to 0 so we dont accidentally make actions longer when we start keyframing
    
    old_action = ob.animation_data.action #remember the current action so we can change back to it
    
    baked_action_names = []
    if visual_bake_actions:#visual bake actions to their linked actions
        for nlatrack in ob.animation_data.nla_tracks:
            if nlatrack.strips[0].action.SquadLinkedAction in bpy.data.actions is not None:
                nlatrack.mute = False #unmute track
                action_to_bake = nlatrack.strips[0].action
                ob.animation_data.action = action_to_bake
                linked_action = bpy.data.actions[ob.animation_data.action.SquadLinkedAction]

                #start_frame = nlatrack.strips[0].action.frame_range[0]
                #end_frame = nlatrack.strips[0].action.frame_range[1]
                start_frame = int(linked_action.frame_range[0])
                end_frame = int(linked_action.frame_range[1])

                nlatrack.strips[0].action_frame_start = start_frame
                nlatrack.strips[0].action_frame_end = end_frame
                
                characterrig = getattachedsquadrig()
                characterrig.animation_data.action = linked_action
                
                action_name = ob.animation_data.action.name

                for bone in bones:
                    #make sure all constraints are turned on
                    for constraint in bone.constraints:
                        #todo: put an if statement here that finds out if there is already keyframed data for "mute", and doesnt keyframe it itself if there is
                        constraint.mute = False
                        constraint.keyframe_insert("mute")
                
                #bake it with the operator
                bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, only_selected=False, visual_keying=True, bake_types={'POSE'})
                #upon baking the baked action will be active ^
                baked_action = ob.animation_data.action
                baked_action.name = action_name + "_baked_for_export"
                baked_action_names.append(baked_action.name)
                
                
                nlatrack.strips[0].action = baked_action #replace the nlastrip unbaked action with the baked one so it gets exported instead
                
                for bone in bones:      
                    #make sure all constraints are *off* and keyed (stops child of constraints from going bananas with baked actions)
                    for constraint in bone.constraints:
                        constraint.mute = True
                        constraint.keyframe_insert("mute")
                nlatrack.mute = True #remute track so it doesnt interfere with next bake

    if force_center_object:#nuke root motion with constraints
        loc_constraint = ob.constraints.new('LIMIT_LOCATION')
        loc_constraint.name = "EXPORT_CONSTRAINT_LOCATION"
        loc_constraint.use_min_x = True
        loc_constraint.use_min_y = True
        loc_constraint.use_min_z = True
        loc_constraint.use_max_x = True
        loc_constraint.use_max_y = True
        loc_constraint.use_max_z = True
        loc_constraint.use_transform_limit = True

        rot_constraint = ob.constraints.new('LIMIT_ROTATION')
        rot_constraint.name = "EXPORT_CONSTRAINT_ROTATION"

        #rot_constraint.min_z = 1.57079632679
        #rot_constraint.max_z = 1.57079632679

        rot_constraint.use_limit_x = True
        rot_constraint.use_limit_y = True
        rot_constraint.use_limit_z = True
        rot_constraint.use_transform_limit = True

        sca_constraint = ob.constraints.new('LIMIT_SCALE')
        sca_constraint.name = "EXPORT_CONSTRAINT_SCALE"

        sca_constraint.min_x = 0.01
        sca_constraint.min_y = 0.01
        sca_constraint.min_z = 0.01
        sca_constraint.max_x = 0.01
        sca_constraint.max_y = 0.01
        sca_constraint.max_z = 0.01
        sca_constraint.use_min_x = True
        sca_constraint.use_min_y = True
        sca_constraint.use_min_z = True
        sca_constraint.use_max_x = True
        sca_constraint.use_max_y = True
        sca_constraint.use_max_z = True
        sca_constraint.use_transform_limit = True
    
    attach_constraint = None
    for constraint in ob.constraints:#detach weapon from squadrig
        #make sure were getting the constraints we made before even if the user changed them slightly
        if constraint.type == "COPY_TRANSFORMS":
            if constraint.subtarget == "SUP_Weapon1_ATTACH" or constraint.name == "SQRig_attach":
                attach_constraint = constraint
                attach_constraint.influence = 0
                attach_constraint.mute = True
    
    #iterate through NLA strips and unmute them so they get included in the export
    for nlatrack in ob.animation_data.nla_tracks:
        nlatrack.mute = False
        for bone in bones:
            #make sure all constraints are keyed
            nlatrack.strips[0].frame_start = nlatrack.strips[0].action.frame_range[0]
            nlatrack.strips[0].frame_end = nlatrack.strips[0].action.frame_range[1]
            #make sure constraints are keyframed so that the export pose doesnt mess with them
            for constraint in bone.constraints:
                constraint.keyframe_insert("mute")
        
        if match_linked_length and nlatrack.strips[0].action.SquadLinkedAction in bpy.data.actions is not None:
            linked_action = bpy.data.actions[nlatrack.strips[0].action.SquadLinkedAction]
            nlatrack.strips[0].frame_start = linked_action.frame_range[0]
            nlatrack.strips[0].frame_end =   linked_action.frame_range[1]
                
    
    #create an export action, see the function to see what it actually does
    create_export_pose()
    export_action = ob.animation_data.action
    
    #do the export
    bpy.ops.export_scene.fbx(
    filepath=filepath,
    use_selection = True,
    add_leaf_bones= False,
    use_armature_deform_only = True,
    bake_anim_use_all_actions=False,
    primary_bone_axis = bone_primary_axis,
    secondary_bone_axis= bone_secondary_axis,
    bake_anim_simplify_factor=simplify_factor
    )
    
    #iterate through all the tracks again and change them back
    for nlatrack in ob.animation_data.nla_tracks:
        nlatrack.mute = True
        for strip in nlatrack.strips:
            if strip.action.name in baked_action_names:#revert actions in the export list off of the baked ones and back to the normal ones
                strip.action = bpy.data.actions[strip.action.name.replace("_baked_for_export","")]
                
    #delete baked actions
    for action_name in baked_action_names:
        bpy.data.actions.remove(bpy.data.actions[action_name])

    #remove the temporary export action
    bpy.data.actions.remove(export_action)
    
    #revert all temporary changes made at the start
    if attach_constraint is not None:
        attach_constraint.influence = 1
        attach_constraint.mute = False
    bpy.context.scene.frame_set(old_frame_current)
    ob.animation_data.action = old_action


    if object_export_name is not None:
        if object_named_root is not None:
            object_named_root.name = object_export_name
        ob.name = ob_old_name

    if force_center_object:
        ob.constraints.remove(loc_constraint)
        ob.constraints.remove(rot_constraint)
        ob.constraints.remove(sca_constraint)
    
    end_time = time.time()
    self.report({'INFO'}, "Exported in: " + str(end_time - start_time) + " seconds.")
    return {'FINISHED'}
'''


██ ███    ███ ██████   ██████  ██████  ████████     ███    ███  ██████  ██████  ███████ ██      
██ ████  ████ ██   ██ ██    ██ ██   ██    ██        ████  ████ ██    ██ ██   ██ ██      ██      
██ ██ ████ ██ ██████  ██    ██ ██████     ██        ██ ████ ██ ██    ██ ██   ██ █████   ██      
██ ██  ██  ██ ██      ██    ██ ██   ██    ██        ██  ██  ██ ██    ██ ██   ██ ██      ██      
██ ██      ██ ██       ██████  ██   ██    ██        ██      ██  ██████  ██████  ███████ ███████ 
                                                                                                
                                                                                            
'''
def import_squad_model(self, context, filepath, delete_import_empty, bone_primary_axis, bone_secondary_axis, delete_lods, min_bone_length):
    start_time = time.time()

    bpy.ops.import_scene.fbx(
    filepath = filepath,
    primary_bone_axis = bone_primary_axis,
    secondary_bone_axis= bone_secondary_axis,
    ignore_leaf_bones = False
    )

    if delete_import_empty:
        #remove empty at top of object heirarchy
        for object in bpy.context.selected_objects:
            if object.parent == None:
                if object.type == "EMPTY":
                    for child in object.children:
                        child.scale = 0.01,0.01,0.01

                    bpy.data.objects.remove(object, do_unlink=True)

    if delete_lods:
        for object in bpy.context.selected_objects:
            if 'LOD' in object.name and 'LOD0' not in object.name:
                bpy.data.objects.remove(object, do_unlink=True)
            elif 'LodGroup' in object.name and object.type == "EMPTY":
                bpy.data.objects.remove(object, do_unlink=True)

    if min_bone_length > 0:
        for object in bpy.context.selected_objects:
            if object.type == "ARMATURE":
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                for bone in object.data.edit_bones:
                    bone.length = max(bone.length, min_bone_length)
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        

    end_time = time.time()
    self.report({'INFO'}, "Exported in: " + str(end_time - start_time) + " seconds.")

    return {'FINISHED'}


def export_squad_model(self, context, filepath, object_export_name, use_tangent_space, bone_primary_axis, bone_secondary_axis, force_center_object):
    start_time = time.time()

    #grab the object at the top of the heirarchy of selected objects
    root_ob = bpy.context.selected_objects[0]
    for i in range(0,100):
        if root_ob.parent == None:
            break
        if root_ob.parent in bpy.context.selected_objects:
            root_ob = root_ob.parent
    ob = root_ob
    #do the temporary naming
    if object_export_name != "":
        ob = root_ob
        object_named_root = None
        ob_old_name = ob.name
        for object in bpy.data.objects:
            if object.name == object_export_name:
                object.name = object_export_name + "_temp_new_name"
                object_named_root = object
        ob.name = object_export_name

    if force_center_object:#nuke root motion with constraints
        loc_constraint = ob.constraints.new('LIMIT_LOCATION')
        loc_constraint.name = "EXPORT_CONSTRAINT_LOCATION"
        loc_constraint.use_min_x = True
        loc_constraint.use_min_y = True
        loc_constraint.use_min_z = True
        loc_constraint.use_max_x = True
        loc_constraint.use_max_y = True
        loc_constraint.use_max_z = True
        loc_constraint.use_transform_limit = True

        rot_constraint = ob.constraints.new('LIMIT_ROTATION')
        rot_constraint.name = "EXPORT_CONSTRAINT_ROTATION"

        #rot_constraint.min_z = 1.57079632679
        #rot_constraint.max_z = 1.57079632679

        rot_constraint.use_limit_x = True
        rot_constraint.use_limit_y = True
        rot_constraint.use_limit_z = True
        rot_constraint.use_transform_limit = True

        sca_constraint = ob.constraints.new('LIMIT_SCALE')
        sca_constraint.name = "EXPORT_CONSTRAINT_SCALE"

        sca_constraint.min_x = 0.01
        sca_constraint.min_y = 0.01
        sca_constraint.min_z = 0.01
        sca_constraint.max_x = 0.01
        sca_constraint.max_y = 0.01
        sca_constraint.max_z = 0.01
        sca_constraint.use_min_x = True
        sca_constraint.use_min_y = True
        sca_constraint.use_min_z = True
        sca_constraint.use_max_x = True
        sca_constraint.use_max_y = True
        sca_constraint.use_max_z = True
        sca_constraint.use_transform_limit = True

    # do the export
    bpy.ops.export_scene.fbx(
    filepath=filepath,
    use_selection = True,
    object_types = {"ARMATURE", "MESH"},
    mesh_smooth_type = "EDGE",
    use_tspace = use_tangent_space,
    add_leaf_bones= False,
    use_armature_deform_only = True,
    bake_anim = False,
    bake_anim_use_all_actions=False,
    primary_bone_axis = bone_primary_axis,
    secondary_bone_axis= bone_secondary_axis,
    )

    #remove constraints that were made earlier
    if force_center_object:
        ob.constraints.remove(loc_constraint)
        ob.constraints.remove(rot_constraint)
        ob.constraints.remove(sca_constraint)

    #undo the temporary naming
    if object_export_name != "":
        ob.name = ob_old_name
        if object_named_root != None:
            object_named_root.name = object_export_name
        

    #print the operating time
    end_time = time.time()
    self.report({'INFO'}, "Exported in: " + str(end_time - start_time) + " seconds.")
    return {'FINISHED'}


'''
 ██████  ██████  ███████ ██████   █████  ████████  ██████  ██████  ███████ 
██    ██ ██   ██ ██      ██   ██ ██   ██    ██    ██    ██ ██   ██ ██      
██    ██ ██████  █████   ██████  ███████    ██    ██    ██ ██████  ███████ 
██    ██ ██      ██      ██   ██ ██   ██    ██    ██    ██ ██   ██      ██ 
 ██████  ██      ███████ ██   ██ ██   ██    ██     ██████  ██   ██ ███████ 
                                                                                                                
'''
class Squadrig_OT_Export_Character_Animation(Operator, ExportHelper):
    """Export Squad Character Animation"""
    bl_idname = "squadrig.export_squad_character_animation"
    bl_label = "Export Squad Character Animation"
    
    # ExportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    ) # type: ignore

    visual_bake_actions: BoolProperty(
        name="Pre-Bake Actions",
        description="Bake the actions before export so any constrained movement from the opposing rig baked. Currently only works on weapon animation exports.",
        default=False,
    ) # type: ignore

    force_center_object: BoolProperty(
        name="Force center object.",
        description="Forces the object to the center of the world, effectively removing any object root motion for the export. Leave on unless you're doing cinematics.",
        default=True,
    ) # type: ignore
    
    match_linked_length: BoolProperty(
        name="Match action length to linked.",
        description="Matches the length of each action to the linked actions so that they sync up correctly in-game. Currently only works on weapon animation exports.",
        default=True,
    ) # type: ignore
    force_lock_foot_root: BoolProperty(
        name="Lock Foot Root bone",
        description="Locks the foot root bone in place as an extra safety measure against the infamous third person spaghetti legs.",
        default=True,
    ) # type: ignore
    simplify_factor: FloatProperty(
        name="Simplify Factor",
        description="Factor to simplify the keyframes to.",
        default=0,
        max = 10,
        min = 0
    )

    @classmethod
    def poll(cls, context):
        if context.active_object != None:
            if context.active_object.animation_data != None:
                return len(context.active_object.animation_data.nla_tracks) != 0

    def execute(self, context):
        return export_squad_character_animation(self, context, self.filepath, self.visual_bake_actions,self.force_center_object, self.match_linked_length, self.force_lock_foot_root, self.simplify_factor)

class Squadrig_OT_Export_Animation(Operator, ExportHelper):
    """Export Squad Animation"""
    bl_idname = "squadrig.export_squad_animation"
    bl_label = "Export Squad Animation"
    
    # ExportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    animation_type: EnumProperty(
        name="",
        description="Exported animations are character or weapon animations.",
        items=(
            ('CHARACTER', "Character Animation", "Animation is for Squad character rig."),
            ('WEAPON', "Weapon Animation", "Animation is for a Squad item."),
        ),
        default='WEAPON',
    )
    object_export_name: StringProperty(
        name="Object export name",
        description="Name of object for export. Overrides name in scene.",
        default="WeaponRoot",
    )
    visual_bake_actions: BoolProperty(
        name="Pre-Bake Actions",
        description="Bake the actions before export so any constrained movement from the opposing rig baked. Currently only works on weapon animation exports.",
        default=False,
    )

    force_center_object: BoolProperty(
        name="Force center object.",
        description="Forces the object to the center of the world, effectively removing any object root motion for the export. Leave on unless you're doing cinematics.",
        default=True,
    )
    match_linked_length: BoolProperty(
        name="Match action length to linked.",
        description="Matches the length of each action to the linked actions so that they sync up correctly in-game. Currently only works on weapon animation exports.",
        default=True,
    )
    force_lock_foot_root: BoolProperty(
        name="Lock Foot Root bone",
        description="Locks the foot root bone in place as an extra safety measure against the infamous third person spaghetti legs.",
        default=True,
    )
    simplify_factor: FloatProperty(
        name="Simplify Factor",
        description="Factor to simplify the keyframes to.",
        default=0,
        max = 10,
        min = 0
    )
    

    bone_primary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    bone_secondary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]

    bone_primary_axis : bpy.props.EnumProperty(items=bone_primary_axis_items, name = "Primary Bone Axis", description="Forward facing axis for bones.", default = "X")

    bone_secondary_axis : bpy.props.EnumProperty(items=bone_secondary_axis_items, name = "Secondary Bone Axis", description="Right facing axis for bones", default = "-Y")

    @classmethod
    def poll(cls, context):
        if context.active_object != None:
            if context.active_object.animation_data != None:
                return len(context.active_object.animation_data.nla_tracks) != 0

    def execute(self, context):
        if(self.animation_type == "CHARACTER"):
            return export_squad_character_animation(self, context, self.filepath, self.visual_bake_actions,self.force_center_object, self.match_linked_length, self.force_lock_foot_root, self.simplify_factor)
        elif(self.animation_type == "WEAPON"):
            return export_weapon_animation(self, context, self.filepath, self.visual_bake_actions,self.force_center_object, self.match_linked_length, self.simplify_factor, self.bone_primary_axis, self.bone_secondary_axis, self.object_export_name)

class Squadrig_OT_Import_Animation(bpy.types.Operator, ImportHelper):
    """Import Squad Animation"""
    bl_idname = "squadrig.import_squad_animation"
    bl_label = "Import Squad Animation"
    
    # ImportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    is_character_animation: BoolProperty(
        name="Animation is character animation",
        description="Handle imported animation as character animation.",
        default=is_squadrig_active(),
    )
    delete_imported_armature: BoolProperty(
        name="Delete Imported Armature",
        description="Deletes the armature that gets imported with the animations.",
        default=True,
    )

    delete_root_motion: BoolProperty(
        name="Delete object keyframes.",
        description="Delete location,scale,rotation keyframes for object transform.",
        default=False,
    )

    
    bone_primary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    bone_secondary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    
    bone_primary_axis : bpy.props.EnumProperty(items=bone_primary_axis_items, name = "Primary Bone Axis", description="Forward facing axis for bones.", default = "X")

    bone_secondary_axis : bpy.props.EnumProperty(items=bone_secondary_axis_items, name = "Secondary Bone Axis", description="Right facing axis for bones", default = "-Y")

    def execute(self, context):
        if self.is_character_animation:
            return import_squad_character_animation(self, context, self.filepath, self.delete_root_motion, self.delete_imported_armature)
        else:
            return import_squad_animation(self, context, self.filepath, self.delete_root_motion, self.bone_primary_axis, self.bone_secondary_axis, self.delete_imported_armature)

class Squadrig_OT_Import_Character_Animation(bpy.types.Operator, ImportHelper):
    """Import Squad Animation"""
    bl_idname = "squadrig.import_squad_character_animation"
    bl_label = "Import Squad Character Animation"
    
    # ImportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    delete_imported_armature: BoolProperty(
        name="Delete Imported Armature",
        description="Deletes the armature that gets imported with the animations.",
        default=True,
    )

    delete_root_motion: BoolProperty(
        name="Delete object keyframes.",
        description="Delete location,scale,rotation keyframes for object transform.",
        default=False,
    )

    def execute(self, context):
        return import_squad_character_animation(self, context, self.filepath, self.delete_root_motion, self.delete_imported_armature)

class Squadrig_OT_Import_Model(bpy.types.Operator, ImportHelper):

    """Import Squad Model"""
    bl_idname = "squadrig.import_squad_model"
    bl_label = "Import Squad Model"
    
    # ImportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    delete_import_empty: BoolProperty(
        name="Delete import empty",
        description="Deletes that pesky little empty you get from importing from UE4. Only have this enabled when importing an FBX that was exported from UE4.",
        default=True,
    )

    delete_lods: BoolProperty(
        name="Delete LODs",
        description="Deletes all the extra Level of Detail (LOD) meshes that you get.",
        default=True,
    ) # type: ignore

    min_bone_length: FloatProperty(
        name="Minimum Bone Length",
        description="Minimum length for imported bones. Blender likes to make some bones REALLY small on import.",
        default=10.0,
    ) # type: ignore

    bone_primary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    bone_secondary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    
    bone_primary_axis : bpy.props.EnumProperty(items=bone_primary_axis_items, name = "Primary Bone Axis", description="Forward facing axis for bones.", default = "X")

    bone_secondary_axis : bpy.props.EnumProperty(items=bone_secondary_axis_items, name = "Secondary Bone Axis", description="Right facing axis for bones", default = "-Y")

    def execute(self, context):
        return import_squad_model(self, context, self.filepath, self.delete_import_empty, self.bone_primary_axis, self.bone_secondary_axis, self.delete_lods, self.min_bone_length)

class Squadrig_OT_Export_Model(Operator, ExportHelper):
    """Export Squad Model"""
    bl_idname = "squadrig.export_squad_model"
    bl_label = "Export Squad Model"
    
    # ExportHelper mixin class uses this
    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    object_export_name: StringProperty(
        name="Object export name",
        description="Name of object for export. Overrides name in scene.",
        default="",
    )

    force_center_object: BoolProperty(
        name="Force center object.",
        description="Forces the object to the center of the world, effectively removing any object root motion for the export. Leave on unless you're doing cinematics.",
        default=True,
    )

    use_tangent_space: BoolProperty(
        name="Tangent Space",
        description="Add binormal and tangent vectors, together with normal they form the (will only work correctly with tris/quads only meshes!).",
        default=True,
    )


    bone_primary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    bone_secondary_axis_items = [
    ("X", "X Axis", "", 1),
    ("Y", "Y Axis", "", 2),
    ("Z", "Z Axis", "", 3),
    ("-X", "-X Axis", "", 4),
    ("-Y", "-Y Axis", "", 5),
    ("-Z", "-Z Axis", "", 6),
    ]
    
    bone_primary_axis : bpy.props.EnumProperty(items=bone_primary_axis_items, name = "Primary Bone Axis", description="Forward facing axis for bones.", default = "X")

    bone_secondary_axis : bpy.props.EnumProperty(items=bone_secondary_axis_items, name = "Secondary Bone Axis", description="Right facing axis for bones", default = "-Y")

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object is not None

    def execute(self, context):
        return export_squad_model(self, context, self.filepath, self.object_export_name, self.use_tangent_space, self.bone_primary_axis, self.bone_secondary_axis, self.force_center_object)