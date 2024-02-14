import bpy

def is_squadrig_active():
    try:
        if(bpy.context.active_object.get("squadrigtype") == 'character_control_rig'):
            return True
    except (AttributeError, KeyError, TypeError):
        return False

def is_weaponrig_active():
    try:
        ob = bpy.context.active_object
        for constraint in ob.constraints:
            #make sure were getting the constraints we made before even if the user changed them slightly
            if constraint.type == "COPY_TRANSFORMS":
                if constraint.subtarget == "SUP_Weapon1_ATTACH" or constraint.name == "SQRig_attach":
                    return True
        return False
    except (AttributeError, KeyError, TypeError):
        return False

def get_active_squadrig():
    try:
        if(bpy.context.active_object.get("squadrigtype") == 'character_control_rig'):
            return bpy.context.active_object
    except (AttributeError, KeyError, TypeError):
        return None

class SquadRig_PT_ExportPanel(bpy.types.Panel):
    """Panel for exporting and organizing actions."""
    bl_label = "Squad Rig Import/Export"
    bl_idname = "SCENE_PT_squadrig_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Squad Rig"
    
    def draw(self, context):
        layout = self.layout
        ob = context.object
        
        #export buttons
        if is_squadrig_active():
            col_flow = layout.column_flow(columns=2, align=True)
            col_flow.scale_y = 1.5
            col_flow.operator("squadrig.import_squad_model", text = "Import Model", icon = 'IMPORT')
            col_flow.operator("squadrig.import_squad_character_animation", text = "Import Character Animation", icon = 'IMPORT')
            col_flow.operator("squadrig.export_squad_model", text = "Export Model", icon = 'EXPORT')
            export_anim = col_flow.operator("squadrig.export_squad_character_animation", text = "Export Character Animation", icon = 'EXPORT')
            #export_anim.animation_type = "CHARACTER"
            #export_anim.object_export_name = "Root"
            #export_anim.visual_bake_actions = False
        elif is_weaponrig_active():
            col_flow = layout.column_flow(columns=2, align=True)
            col_flow.scale_y = 1.5
            col_flow.operator("squadrig.import_squad_model", text = "Import Model", icon = 'IMPORT')
            col_flow.operator("squadrig.import_squad_animation", text = "Import Animation", icon = 'IMPORT')
            col_flow.operator("squadrig.export_squad_model", text = "Export Model", icon = 'EXPORT')
            export_anim = col_flow.operator("squadrig.export_squad_animation", text = "Export Weapon Animation", icon = 'EXPORT')
            #export_anim.animation_type = "WEAPON"
            #export_anim.object_export_name = "WeaponRoot"
            #export_anim.visual_bake_actions = True
        else:
            col_flow = layout.column_flow(columns=2, align=True)
            col_flow.scale_y = 1.5
            col_flow.operator("squadrig.import_squad_model", text = "Import Model", icon = 'IMPORT')
            col_flow.operator("squadrig.import_squad_animation", text = "Import Animation", icon = 'IMPORT')
            col_flow.operator("squadrig.export_squad_model", text = "Export Model", icon = 'EXPORT')
            export_anim = col_flow.operator("squadrig.export_squad_animation", text = "Export Animation", icon = 'EXPORT')
            #export_anim.animation_type = "WEAPON"
            #export_anim.object_export_name = "WeaponRoot"
            #export_anim.visual_bake_actions = True
        

        if context.active_object is not None:
            #active action
            if ob.type != "ARMATURE":
                layout.label(text="Animating non-skeletons not recommended for SQUAD.", icon = "ERROR")
            
            if ob.animation_data is not None:
                layout.label(text="Active Action:")
                layout.prop(ob.animation_data, "action", text = "")
            #else:
            #    layout.label(text="No animation_data.")


            
            if ob.animation_data is not None:
                if ob.animation_data.action is not None:
                    layout.label(text="Linked Action:")
                    row = layout.row()
                    row.prop(ob.animation_data.action, "SquadLinkedAction", text = "", icon = "LINKED")
            
            
            #lists
            layout.label(text="Action List:")
            #col_flow = layout.grid_flow(columns=2, align=False)
            split = layout.split(factor=0.90)
            
            #action list
            col = split.column()
            col.template_list("ACTION_UL_list", "", bpy.data, "actions", ob.SquadRigExportProperties, "action_list_index")
            col = split.column(align = True)

            #action buttons
            if is_squadrig_active():#if squad rig
                col.operator("wm.call_menu", text = "", icon = 'ADD' ).name = "OBJECT_MT_new_action_menu"
            else:#if not squad rig
                col.operator("squadrig.create_action", text = "", icon = 'ADD')
            col.operator("squadrig.delete_action", text = "", icon = 'REMOVE')
            col.operator("squadrig.duplicate_action", text = "", icon = 'DUPLICATE')
            
            #export list
            layout.label(text="Export list:")
            layout.template_list("NLA_UL_list", "", ob.animation_data, "nla_tracks", ob.SquadRigExportProperties, "nla_track_index")

class SquadRig_PT_SquadRigControlsPanel(bpy.types.Panel):
    """Controls for Squad Rig."""
    bl_label = "Squad Rig Controls"
    bl_idname = "SCENE_PT_squadrig_controls"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Squad Rig'
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def draw(self, context):
        layout = self.layout
        ob = context.object
        scene = context.scene
        
        squadrig = get_active_squadrig()
        
        '''
        if ob.animation_data is not None:
            #layout.label(text="Active Action:")
            layout.prop(ob.animation_data, "action", text = "Active Action", emboss = False, icon = "NONE")
            if ob.animation_data.action is not None:
                row = layout.row()
                row.prop(ob.animation_data.action, "SquadLinkedAction", text = "Linked Action")
                row.operator("wm.call_menu", text = "", icon = 'ADD' ).name = "OBJECT_MT_link_action"
        #lists
        layout.label(text="Action List:")
        #col_flow = layout.grid_flow(columns=2, align=False)
        split = layout.split(factor=0.90)
        
        #action list
        col = split.column()
        col.template_list("CONTROLS_ACTION_UL_list", "", bpy.data, "actions", ob.SquadRigExportProperties, "action_list_index")
        

        #action buttons
        col = split.column(align = True)
        if squadrig is not None:
            col.operator("wm.call_menu", text = "", icon = 'ADD' ).name = "OBJECT_MT_new_action_menu"
        else:
            col.operator("squadrig.create_action", text = "", icon = 'ADD')
        col.operator("squadrig.delete_action", text = "", icon = 'REMOVE')
        col.operator("squadrig.duplicate_action", text = "", icon = 'DUPLICATE')
        '''
        if squadrig is not None: #squad rig is selected
            #hand attach stuff
            layout.label(text="Hand Attach:", icon = "VIEW_PAN")
            row = layout.row()
            row.prop(ob.pose.bones["Bip01_IK_L_Hand"].constraints["attach_weapon"], "influence", text='Left Hand Gun Attach', icon =  "EVENT_L")
            row = layout.row()
            row.prop(ob.pose.bones["Bip01_IK_R_Hand"].constraints["attach_weapon"], "influence", text='Right Hand Gun Attach', icon =  "EVENT_R")
            
            #head size slider (to stop the face clipping through the camera in first person)
            row = layout.row()
            row.prop(ob.pose.bones["CON_Head"].constraints["Limit Scale"], "influence", text = "Shrink head", icon =  "MONKEY")

            '''
            #Bone layer stuff
            layout.label(text="Bone Layers:", icon = "GROUP_BONE")
            row = layout.row()
            row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Third Person', icon = "ARMATURE_DATA")
            row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='First Person', icon = "OUTLINER_OB_CAMERA")
            row = layout.row()
            row.prop(context.active_object.data, 'layers', index=17, toggle=True, text='More Weapon Controls', icon =  "NONE")
            row.prop(context.active_object.data, 'layers', index=18, toggle=True, text='Fingers', icon =  "NONE")
            row = layout.row()
            split = row.split(factor = 0.494)
            split.prop(context.active_object.data, 'layers', index=23, toggle=True, text='Face', icon =  "NONE")
            row = layout.row()
            row.prop(context.active_object.data, 'layers', index=8, toggle=True, text='Weight Painting', icon =  "NONE")
            '''
            #character visibility layer stuff
            row = layout.row()
            row.label(text = "Character Skin:")
            #row = layout.row()

            #row = layout.row()
            #row.prop(bpy.data.objects["SQRIG_character_mesh"], "data", text = "", emboss = False)
            #op = row.operator("wm.call_menu")
            #op.name=CharacterMeshSelector.bl_idname
            row = layout.row()
            row.menu("OBJECT_MT_squad_character_mesh_selector_menu", text = "Deform Mesh")
                
                
        elif context.active_pose_bone is not None: #bone is selected on non-squad rig
            row = layout.row()
            
            if not context.active_pose_bone.constraints:
                row.label(text = "No Bone Constraints")
            else:
                row.label(text = "Bone Constraints:")
            
            for constraint in context.active_pose_bone.constraints:
                if constraint.type == "CHILD_OF":
                    if "Bip01_L_Hand" in constraint.name:
                        constraint_name = "Attach Left"
                    elif "Bip01_R_Hand" in constraint.name:
                        constraint_name = "Attach Right"
                    else:
                        constraint_name = constraint.name.replace("SQRig_attach_", "")
                    
                    box = layout.box()
                    row = box.row()
                    
                    row.prop(constraint, "influence", text = constraint_name)
                    
                    split = box.split(factor=0.333)
                    
                    op = split.operator("constraint.childof_set_inverse", icon = "ADD")
                    op.constraint = constraint.name
                    op.owner = "BONE"
                    
                    op = split.operator("constraint.childof_clear_inverse", icon = "PANEL_CLOSE")
                    op.constraint = constraint.name
                    op.owner = "BONE"
                    
                    op = split.operator("constraint.delete", text = "", icon = "PANEL_CLOSE")
                    op.constraint= constraint.name
                    op.owner='BONE'
                    
        #else:#invalid selection
        #    layout.label(text="Nothing to display.")

class SquadRig_PT_ToolsPanel(bpy.types.Panel):
    bl_idname = 'WM_PT_squadrig_tools'
    bl_label = 'Squad Rig Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Squad Rig"
    
    def draw_header(self, context):
        layout = self.layout
        #layout.prop(context.window_manager, 'enable_screenkeys', text='')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        #row.operator("squadrig.add_control_rig", text = "Create Squad Control Rig", icon =  "OUTLINER_OB_ARMATURE")

        layout.label(text="Object tools")
        split = layout.split(factor = 0.5, align=True)
        split.operator("squadrig.attach_to_weaponbone", text = "Attach to weapon bone", icon =  "DECORATE_LINKED")
        split.operator("squadrig.detach_from_weaponbone", text = "Dettach from weapon bone", icon = "UNLINKED")

        col_flow = layout.column_flow(columns=2, align=True)
        col_flow.scale_y = 1.25
        layout.label(text="Skin tools")
        col_flow.operator("squadrig.make_character_skin", text = "Convert to Rig Skin", icon = "MATCLOTH")
        col_flow.operator("squadrig.remove_character_skin", text = "Purge Rig Skin", icon = "X")
        col_flow.operator("squadrig.detach_character_skin", text = "Deconvert Rig Skin", icon = "MATCLOTH")
        
        layout.label(text="Bone tools")
        row = layout.column()
        op = row.operator("squadrig.make_child_of", text = "Attach Left Hand", icon = "CONSTRAINT_BONE")
        op.attach_target_bone = "Bip01_L_Hand"
        
        row = layout.column()
        op = row.operator("squadrig.make_child_of", text = "Attach Right Hand", icon = "CONSTRAINT_BONE")
        op.attach_target_bone = "Bip01_R_Hand"