import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty


#create anim data if there is none (stops an error)
def create_animation_data(ob):
    ob.keyframe_insert(data_path='location',frame=0)
    bpy.data.actions.remove(ob.animation_data.action)

class SquadRig_OT_MarkForExport(bpy.types.Operator):
    """Marks action for export with Squad Rig"""
    bl_idname = "squadrig.markforexport"
    bl_label = "Mark Action For Export"
    bl_options = {"REGISTER","UNDO"}
    
    action_to_mark : StringProperty("")

    #@classmethod
    #def poll(cls, context):
    #    return context.active_object.animation_data is not None

    def execute(self, context):
        
        ob = context.object

        if ob.animation_data is None:
            create_animation_data(ob)
        
        #creata an NLA track and strap a new strip to it with our action
        if(self.action_to_mark in bpy.data.actions):
            new_track = ob.animation_data.nla_tracks.new()
            new_track.mute = True
            new_strip = new_track.strips.new("beans",0,bpy.data.actions[self.action_to_mark])
            new_track.name = "BST_ExportTrack_" + new_strip.name
        return {'FINISHED'}

class SquadRig_OT_UnmarkForExport(bpy.types.Operator):
    """Unmarks action for export with Squad Rig"""
    bl_idname = "squadrig.unmarkforexport"
    bl_label = "Unmark Action For Export"
    bl_options = {"REGISTER","UNDO"}
    
    action_to_unmark : StringProperty("")


    def execute(self, context):
        ob = context.object
        if(self.action_to_unmark in ob.animation_data.nla_tracks):

            unmark_index = ob.animation_data.nla_tracks.find(self.action_to_unmark)
        
            ob.animation_data.nla_tracks.remove(ob.animation_data.nla_tracks[unmark_index])
        
        return {'FINISHED'}

class SquadRig_OT_LinkAction(bpy.types.Operator):
    """Marks action for export with Squad Rig"""
    bl_idname = "squadrig.link_action"
    bl_label = "Mark Action For Export"
    bl_options = {"REGISTER","UNDO"}
    
    action_to_link : StringProperty("")

    @classmethod
    def poll(cls, context):
        return context.active_object.animation_data.action is not None

    def execute(self, context):
        ob = bpy.context.active_object
        active_action = ob.animation_data.action

        active_action.SquadLinkedAction = self.action_to_link

        return {'FINISHED'}


class SquadRig_OT_CreateAction(bpy.types.Operator):
    """Creates an Action"""
    bl_idname = "squadrig.create_action"
    bl_label = "Create An Action"
    bl_options = {"REGISTER","UNDO"}
    
    name: bpy.props.StringProperty(name="Name",description="Name of new created action", default="new_action")
    
    def execute(self, context):
        
        ob = bpy.context.object
        
        #clear previous action
        if ob.animation_data:
            if ob.animation_data.action is not None:
                ob.animation_data.action = None
        
        #create the action
        ob.keyframe_insert(data_path='location',frame=0)
        new_action = ob.animation_data.action
        ob.keyframe_delete(data_path='location',frame=0)
        
        #setup new action
        ob.animation_data.action = new_action
        new_action.use_fake_user = True
        
        new_action.name = self.name
        
        #update() list index so new action is selected
        ob.SquadRigExportProperties.action_list_index = bpy.data.actions.find(new_action.name)
        
        return {'FINISHED'}
    
class SquadRig_OT_DeleteAction(bpy.types.Operator):
    """Deletes an Action"""
    bl_idname = "squadrig.delete_action"
    bl_label = "Delete Action"
    bl_options = {"REGISTER","UNDO"}
    
    @classmethod
    def poll(cls, context):
        if  context.active_object.animation_data is not None:
            return context.active_object.animation_data.action is not None

    def execute(self, context):
           
        ob = bpy.context.object
        
        if ob.animation_data.action is not None:
            bpy.data.actions.remove(ob.animation_data.action)

        ob.SquadRigExportProperties.action_list_index -=1
        
        return {'FINISHED'}

class SquadRig_OT_DuplicateAction(bpy.types.Operator):

    """Creates an Action"""
    bl_idname = "squadrig.duplicate_action"
    bl_label = "Create An Action"
    bl_options = {"REGISTER","UNDO"}
    
    #name: bpy.props.StringProperty(name="Name",description="Name of new created action", default="new_action")
    
    @classmethod
    def poll(cls, context):
        if  context.active_object.animation_data is not None:
            return context.active_object.animation_data.action is not None

    def execute(self, context):
        
        ob = bpy.context.object
        
        #clear previous action
        if ob.animation_data:
            if ob.animation_data.action is not None:
                original_action = ob.animation_data.action 
                duplicated_action = original_action.copy()
                #duplicated_action.name = original_action

                duplicated_action.use_fake_user = True
                ob.animation_data.action = duplicated_action
                
                ob.SquadRigExportProperties.action_list_index = bpy.data.actions.find(duplicated_action.name)
                
        return {'FINISHED'}

class SquadRig_OT_AddFakeUser(bpy.types.Operator):
    """HIGHLY RECOMMENDED. Adds fake user to action. Without a user the action may be lost when exiting the blend file (doesn't matter if the blend file itself gets saved or not), adding a fake user ensures that this never happens."""
    bl_idname = "squadrig.action_add_fake_user"
    bl_label = "Add Fake User To Action"
    bl_options = {"REGISTER","UNDO"}
    
    action_name: bpy.props.StringProperty(name="Name",description="Name of action to add fake user to.", default="")

    def execute(self, context):
        
        if self.action_name is not "":
            bpy.data.actions[self.action_name].use_fake_user = True
                
        return {'FINISHED'}

class SquadRig_MT_NewActionMenu(bpy.types.Menu):
    bl_label = "New Action Type"
    bl_idname = "OBJECT_MT_new_action_menu"

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        op = col.operator("squadrig.apply_pose", text = "New 1p", icon = "HIDE_OFF")
        op.new_pose = 'FIRST_PERSON'
        op.do_gun_pose = True
        op.do_keyframe = True
        op.do_new_action = True

        col.label(text = "")#spacer

        op = col.operator("squadrig.apply_pose", text = "New 3p Stand", icon = "SMOOTHCURVE")
        op.new_pose = 'THIRD_PERSON_STAND'
        op.do_gun_pose = True
        op.do_keyframe = True
        op.do_new_action = True
        op = col.operator("squadrig.apply_pose", text = "New 3p Crouch", icon = "SPHERECURVE")
        op.new_pose = 'THIRD_PERSON_CROUCH'
        op.do_gun_pose = True
        op.do_keyframe = True
        op.do_new_action = True
        op = col.operator("squadrig.apply_pose", text = "New 3p Prone", icon = "NOCURVE")
        op.new_pose = 'THIRD_PERSON_PRONE'
        op.do_gun_pose = True
        op.do_keyframe = True
        op.do_new_action = True

        col.label(text = "")#spacer

        op = col.operator("squadrig.create_action", text = "New Blank Action", icon = "META_PLANE")

class SquadRig_MT_LinkActionMenu(bpy.types.Menu):
    bl_label = "Link Action"
    bl_idname = "OBJECT_MT_link_action"

    def draw(self, context):
        layout = self.layout
        
        ob = bpy.context.active_object
        active_action = ob.animation_data.action

        for action in bpy.data.actions:
            #skip active_action so we cant link the action to itself
            if action == active_action:
                continue
            row = layout.row()
            op = row.operator("squadrig.link_action", text = action.name).action_to_link = action.name
