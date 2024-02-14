import bpy

def FixActionRig5Beta():
    action = bpy.context.active_object.animation_data.action
    a_groups = action.groups

    correct_bones = ['Bip01_DEF_Clavicle_L',
                    'Bip01_Neck',
                    'Bip01_Head',
                    'Bip01_DEF_Clavicle_R',
                    'Bip01_DEF_Finger0_R',
                    'Bip01_DEF_Finger01_R',
                    'Bip01_DEF_Finger02_R',
                    'Bip01_DEF_Finger1_R',
                    'Bip01_DEF_Finger11_R',
                    'Bip01_DEF_Finger12_R',
                    'Bip01_DEF_Finger2_R',
                    'Bip01_DEF_Finger21_R',
                    'Bip01_DEF_Finger22_R',
                    'Bip01_DEF_Finger3_R',
                    'Bip01_DEF_Finger31_R',
                    'Bip01_DEF_Finger32_R',
                    'Bip01_DEF_Finger4_R',
                    'Bip01_DEF_Finger41_R',
                    'Bip01_DEF_Finger42_R',
                    'Bip01_DEF_Clavicle_L',
                    'Bip01_DEF_Finger0_L',
                    'Bip01_DEF_Finger01_L',
                    'Bip01_DEF_Finger02_L',
                    'Bip01_DEF_Finger1_L',
                    'Bip01_DEF_Finger11_L',
                    'Bip01_DEF_Finger12_L',
                    'Bip01_DEF_Finger2_L',
                    'Bip01_DEF_Finger21_L',
                    'Bip01_DEF_Finger22_L',
                    'Bip01_DEF_Finger3_L',
                    'Bip01_DEF_Finger31_L',
                    'Bip01_DEF_Finger32_L',
                    'Bip01_DEF_Finger4_L',
                    'Bip01_DEF_Finger41_L',
                    'Bip01_DEF_Finger42_L',]

    for bone in correct_bones:
        for curve in a_groups[bone].channels:
            curve.data_path = curve.data_path.replace('Bip01_','CON_')
            curve.data_path = curve.data_path.replace('_DEF','')

def FixActionRig3v2():
    ob = bpy.context.active_object
    action = ob.animation_data.action
    a_groups = action.groups

    for curve in a_groups["C_WeaponController"].channels:
            curve.data_path = curve.data_path.replace('C_WeaponController','CON_WeaponController')
    
    euler_bones = ["C_WeaponController"]
    for bone in euler_bones: #keyframe in keyframes:
        #bone.keyframe#keyframe euler on all euler bones
        for curve in a_groups[bone].channels:
            for point in curve.keyframe_points:
                bpy.data.scenes['Scene'].frame_set(point.frame)
                ob.keyframe_insert('pose.bones["CON_WeaponController"].rotation_euler', point.frame)



class SquadRig_PT_Dev_Panel(bpy.types.Panel):
    bl_idname = "WM_PT_squadrig_dev_panel"
    bl_label = "SQRig Dev Panel"
    bl_category = 'Squad Rig'

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"


    def draw(self,context):
        layout = self.layout
        ob = context.object

        layout.label(text = "Dev panel for dev(s)")

        col_flow = layout.column_flow(columns=0, align=False)
        col_flow.operator('squadrig.make_b1', text = "Convert to B1 Rig")
        col_flow.operator('squadrig.fix_action', text = "Fix Action")

        col_flow = layout.column_flow(columns=0, align=False)
        col_flow.operator('squadrig.create_ranging_object', text = "Add Ranging Object")
        

class SquadRig_OT_ConvertToB1Droid(bpy.types.Operator):
    """Converts rig for use with B1 Battledroid"""
    bl_idname = "squadrig.make_b1"
    bl_label = "Convert to B1 Rig"
    
    attach_target_bone : bpy.props.StringProperty("")
    
    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        ob = bpy.context.active_object
        bones = ob.data.edit_bones
        p_bones = ob.pose.bones

        bpy.ops.object.mode_set(mode='EDIT', toggle=True)

        bones['Bip01_Neck'].roll = -5.496910375768493e-07
        bones['Bip01_Neck'].head = (4.6170171117410064e-05,4.821495532989502,147.8706512451172)
        bones['Bip01_Neck'].tail = (5.143109956406988e-05,16.543624877929688,172.81431579589844)
        bones['Bip01_Head'].roll = -1.0361434306105366e-06
        bones['Bip01_Head'].head = (5.143109956406988e-05,16.543624877929688,172.81431579589844)
        bones['Bip01_Head'].tail = (4.7386096412083134e-05,14.484253883361816,186.27919006347656)
        bones['Bip01_R_Clavicle'].roll = 1.570796251296997
        bones['Bip01_R_Clavicle'].head = (-7.282226085662842,4.927592754364014,141.67001342773438)
        bones['Bip01_R_Clavicle'].tail = (-21.037124633789062,4.927595138549805,141.67001342773438)
        bones['Bip01_R_Finger0'].roll = -2.608431816101074
        bones['Bip01_R_Finger0'].head = (-46.976444244384766,-11.584989547729492,95.33103942871094)
        bones['Bip01_R_Finger0'].tail = (-43.421730041503906,-12.223426818847656,89.5059585571289)
        bones['Bip01_R_Finger01'].roll = -2.6084322929382324
        bones['Bip01_R_Finger01'].head = (-43.42173767089844,-12.223423957824707,89.50597381591797)
        bones['Bip01_R_Finger01'].tail = (-40.497684478759766,-12.748590469360352,84.71435546875)
        bones['Bip01_R_Finger02'].roll = -2.6084389686584473
        bones['Bip01_R_Finger02'].head = (-40.4976921081543,-12.74859619140625,84.71434020996094)
        bones['Bip01_R_Finger02'].tail = (-39.019752502441406,-13.014089584350586,82.29248809814453)
        bones['Bip01_R_Finger1'].roll = 1.500143051147461
        bones['Bip01_R_Finger1'].head = (-49.0764045715332,-11.682355880737305,91.88839721679688)
        bones['Bip01_R_Finger1'].tail = (-51.09251403808594,-14.708795547485352,85.31305694580078)
        bones['Bip01_R_Finger11'].roll = 1.5001378059387207
        bones['Bip01_R_Finger11'].head = (-50.13013458251953,-16.560287475585938,85.88867950439453)
        bones['Bip01_R_Finger11'].tail = (-51.57019805908203,-18.72203254699707,81.1919937133789)
        bones['Bip01_R_Finger12'].roll = 1.5001392364501953
        bones['Bip01_R_Finger12'].head = (-52.087154388427734,-12.905182838439941,84.77643585205078)
        bones['Bip01_R_Finger12'].tail = (-53.527225494384766,-15.066960334777832,80.07974243164062)
        bones['Bip01_L_Clavicle'].roll = -1.5707950592041016
        bones['Bip01_L_Clavicle'].head = (7.282161712646484,4.927685260772705,141.7021484375)
        bones['Bip01_L_Clavicle'].tail = (21.037063598632812,4.927682876586914,141.7021484375)
        bones['Bip01_L_Finger0'].roll = 2.60842947369
        bones['Bip01_L_Finger0'].head = (46.976444244384766,-11.585043907165527,95.33106231689453)
        bones['Bip01_L_Finger0'].tail = (43.42173767089844,-12.223478317260742,89.50599670410156)
        bones['Bip01_L_Finger01'].roll = 2.60842947369
        bones['Bip01_L_Finger01'].head = (43.42172622680664,-12.223482131958008,89.5059814453125)
        bones['Bip01_L_Finger01'].tail = (40.4976806640625,-12.74864673614502,84.7143783569336)
        bones['Bip01_L_Finger1'].roll = -1.5001425743103027
        bones['Bip01_L_Finger1'].head = (49.0764045715332,-11.682361602783203,91.8884048461914)
        bones['Bip01_L_Finger1'].tail = (51.09251022338867,-14.708799362182617,85.31306457519531)
        bones['Bip01_L_Finger11'].roll = -1.5001417398452759
        bones['Bip01_L_Finger11'].head = (50.130126953125,-16.56029510498047,85.88868713378906)
        bones['Bip01_L_Finger11'].tail = (51.5702018737793,-18.72203826904297,81.19200897216797)
        bones['Bip01_L_Finger12'].roll = -1.5001416206359863
        bones['Bip01_L_Finger12'].head = (52.08715057373047,-12.905190467834473,84.77645111083984)
        bones['Bip01_L_Finger12'].tail = (53.5272216796875,-15.066961288452148,80.07976531982422)
        bones['Bip01_L_Toe0'].roll = -0.07942576706409454
        bones['Bip01_L_Toe0'].head = (19.19300079345703,-2.323594331741333,1.4517862796783447)
        bones['Bip01_L_Toe0'].tail = (22.844141006469727,-9.866620063781738,1.5966947078704834)
        bones['Bip01_R_Toe0'].roll = 0.0794249176979065
        bones['Bip01_R_Toe0'].head = (-19.19304656982422,-2.323648691177368,1.4517862796783447)
        bones['Bip01_R_Toe0'].tail = (-22.84416389465332,-9.866692543029785,1.5966912508010864)


        #controller bones

        bones['CON_Neck'].roll = -5.496910375768493e-07
        bones['CON_Neck'].head = (4.6170171117410064e-05,4.821495532989502,147.8706512451172)
        bones['CON_Neck'].tail = (5.143109956406988e-05,16.543624877929688,172.81431579589844)
        bones['CON_Head'].roll = -1.0361434306105366e-06
        bones['CON_Head'].head = (5.143109956406988e-05,16.543624877929688,172.81431579589844)
        bones['CON_Head'].tail = (4.7386096412083134e-05,14.484253883361816,186.27919006347656)

        bones['CON_Finger0_R'].roll = -2.608431816101074
        bones['CON_Finger0_R'].head = (-46.976444244384766,-11.584989547729492,95.33103942871094)
        bones['CON_Finger0_R'].tail = (-43.421730041503906,-12.223426818847656,89.5059585571289)
        bones['CON_Finger01_R'].roll = -2.6084322929382324
        bones['CON_Finger01_R'].head = (-43.42173767089844,-12.223423957824707,89.50597381591797)
        bones['CON_Finger01_R'].tail = (-40.497684478759766,-12.748590469360352,84.71435546875)

        bones['CON_Finger0_L'].roll = 2.60842947369
        bones['CON_Finger0_L'].head = (46.976444244384766,-11.585043907165527,95.33106231689453)
        bones['CON_Finger0_L'].tail = (43.42173767089844,-12.223478317260742,89.50599670410156)
        bones['CON_Finger01_L'].roll = 2.60842947369
        bones['CON_Finger01_L'].head = (43.42172622680664,-12.223482131958008,89.5059814453125)
        bones['CON_Finger01_L'].tail = (40.4976806640625,-12.74864673614502,84.7143783569336)

        bones['CON_Finger1_R'].roll = 1.500143051147461
        bones['CON_Finger1_R'].head = (-49.0764045715332,-11.682355880737305,91.88839721679688)
        bones['CON_Finger1_R'].tail = (-51.09251403808594,-14.708795547485352,85.31305694580078)
        bones['CON_Finger11_R'].roll = 1.5001378059387207
        bones['CON_Finger11_R'].head = (-50.13013458251953,-16.560287475585938,85.88867950439453)
        bones['CON_Finger11_R'].tail = (-51.57019805908203,-18.72203254699707,81.1919937133789)
        bones['CON_Finger12_R'].roll = 1.5001392364501953
        bones['CON_Finger12_R'].head = (-52.087154388427734,-12.905182838439941,84.77643585205078)
        bones['CON_Finger12_R'].tail = (-53.527225494384766,-15.066960334777832,80.07974243164062)

        bones['CON_Clavicle_L'].roll = -1.5707950592041016
        bones['CON_Clavicle_L'].head = (7.282161712646484,4.927685260772705,141.7021484375)
        bones['CON_Clavicle_L'].tail = (21.037063598632812,4.927682876586914,141.7021484375)
        bones['CON_Clavicle_R'].roll = 1.570796251296997
        bones['CON_Clavicle_R'].head = (-7.282226085662842,4.927592754364014,141.67001342773438)
        bones['CON_Clavicle_R'].tail = (-21.037124633789062,4.927595138549805,141.67001342773438)
        bones['CON_Finger1_L'].roll = -1.5001425743103027
        bones['CON_Finger1_L'].head = (49.0764045715332,-11.682361602783203,91.8884048461914)
        bones['CON_Finger1_L'].tail = (51.09251022338867,-14.708799362182617,85.31306457519531)
        bones['CON_Finger11_L'].roll = -1.5001417398452759
        bones['CON_Finger11_L'].head = (50.130126953125,-16.56029510498047,85.88868713378906)
        bones['CON_Finger11_L'].tail = (51.5702018737793,-18.72203826904297,81.19200897216797)
        bones['CON_Finger12_L'].roll = -1.5001416206359863
        bones['CON_Finger12_L'].head = (52.08715057373047,-12.905190467834473,84.77645111083984)
        bones['CON_Finger12_L'].tail = (53.5272216796875,-15.066961288452148,80.07976531982422)

        bones['CON_Finger12_L'].parent = bones['CON_Finger1_L']
        bones['CON_Finger12_R'].parent = bones['CON_Finger1_R']

        bpy.ops.object.mode_set(mode='OBJECT', toggle=True)

        #stuff
        p_bones['CON_Neck'].custom_shape_scale = 0.17

        finger_bones = [
        p_bones["CON_Finger11_R"],
        p_bones["CON_Finger12_R"],
        p_bones["CON_Finger1_R"],
        p_bones["CON_Finger01_R"],
        p_bones["CON_Finger11_L"],
        p_bones["CON_Finger12_L"],
        p_bones["CON_Finger1_L"],
        p_bones["CON_Finger01_L"]
        ]

        for bone in finger_bones:
            bone.rotation_mode = "XYZ"
            bone.lock_rotation = (False,True,True)
            
        p_bones["CON_Finger0_L"].rotation_mode = "XYZ"
        p_bones["CON_Finger0_R"].rotation_mode = "XYZ"

        p_bones["CON_Clavicle_R"].rotation_mode = "XYZ"
        p_bones["CON_Clavicle_L"].rotation_mode = "XYZ"
        p_bones["CON_Clavicle_R"].lock_rotation = (True,False,True)
        p_bones["CON_Clavicle_L"].lock_rotation = (True,False,True)

        hide_finger_bones = []
        hide_finger_bones.append(p_bones['CON_Finger02_R'])
        hide_finger_bones.append(p_bones['CON_Finger2_R'])
        hide_finger_bones.append(p_bones['CON_Finger21_R'])
        hide_finger_bones.append(p_bones['CON_Finger22_R'])
        hide_finger_bones.append(p_bones['CON_Finger3_R'])
        hide_finger_bones.append(p_bones['CON_Finger31_R'])
        hide_finger_bones.append(p_bones['CON_Finger32_R'])
        hide_finger_bones.append(p_bones['CON_Finger4_R'])
        hide_finger_bones.append(p_bones['CON_Finger41_R'])
        hide_finger_bones.append(p_bones['CON_Finger42_R'])
        hide_finger_bones.append(p_bones['CON_Finger02_L'])
        hide_finger_bones.append(p_bones['CON_Finger2_L'])
        hide_finger_bones.append(p_bones['CON_Finger21_L'])
        hide_finger_bones.append(p_bones['CON_Finger22_L'])
        hide_finger_bones.append(p_bones['CON_Finger3_L'])
        hide_finger_bones.append(p_bones['CON_Finger31_L'])
        hide_finger_bones.append(p_bones['CON_Finger32_L'])
        hide_finger_bones.append(p_bones['CON_Finger4_L'])
        hide_finger_bones.append(p_bones['CON_Finger41_L'])
        hide_finger_bones.append(p_bones['CON_Finger42_L'])

        for bone in hide_finger_bones:
            for layer in bone.bone.layers:
                layer = False
            bone.bone.layers[14] = True
            bone.bone.layers[0] = False

        return {'FINISHED'}

class SquadRig_OT_FixAction(bpy.types.Operator):
    """Fixes action STILL IN DEVELOPMENT"""
    bl_idname = "squadrig.fix_action"
    bl_label = "Fix action"
    
    @classmethod
    def poll(cls, context):
        return context.active_object
    
    def execute(self, context):
        action = bpy.context.active_object.animation_data.action
        a_groups = action.groups

        if a_groups['Bip01_DEF_Clavicle_L'] and a_groups['CC_CustomConstraints_itemAttach.R']:
            FixActionRig5Beta()
            print("Rig 5 beta found")
            self.report({'INFO'}, "Rig 5 (beta) found")
        elif a_groups['C_WeaponAttach.R'] and a_groups['CC_CustomConstraints_rightHandAttach']:
            print("Rig 3 v2 found")
            self.report({'INFO'}, "Rig 3 v2 found, can't do anything though")
            #FixActionRig3v2()
        else:
            self.report({'INFO'}, "No idea what rig this action belongs to.")


        return {'FINISHED'}
    