import bpy

#check if an action is marked for export, used in the action list for graying out the mark for export button
def isActionMarkedForExport(action):
    ob = bpy.context.object
    if ob.animation_data:
        for nla_track in ob.animation_data.nla_tracks:
            if len(nla_track.strips) == 1:
                if nla_track.strips[0].action == action:
                    return True
    return False

class ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        if self.layout_type in {'DEFAULT', 'GRID'}:
            
            #change icon based on if action is already marked for export
            mark_icon = 'CHECKMARK' if isActionMarkedForExport(item) else 'EXPORT'
            
            #display mark for export button
            row = layout.row()
            row.enabled = not isActionMarkedForExport(item)
            row.operator("squadrig.markforexport",text='', icon=mark_icon).action_to_mark = item.name
            
            #display name of action
            if item.use_fake_user == False:
                row.prop(item, "name", text="", emboss=False, icon="FAKE_USER_OFF")
                row.operator("squadrig.action_add_fake_user", text = "ADD FAKE USER", icon= "FAKE_USER_OFF").action_name = item.name
            else:
                row.prop(item, "name", text="", emboss=False, icon="ACTION")

        elif self.layout_type in {'GRID'}:
            pass

class NLA_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        if self.layout_type in {'DEFAULT', 'GRID'}:
            #unmark action button
            
            unmark_row = layout.row()
            unmark_row.ui_units_x = 1
            unmark_row.operator("SquadRig.unmarkforexport",text='', icon='REMOVE').action_to_unmark = item.name
            
            
            #DISPLAY
            if len(item.strips) == 1:
                if item.strips[0].action is not None:#track is healthy
                    #display NLA track info stuff
                    layout.prop(item.strips[0], "name", text="", emboss=False, icon='EXPORT')
                    layout.prop(item.strips[0].action, "name", text="", emboss=False, icon='ACTION')
                    
                else:#strip is either being moved or is missing an assigned action
                    layout.label(text ="Export strip is missing action!", icon = "ERROR")
            else:
                #when the NLA track has an amount of strips that is not 1
                #track has to be deleted for export, otherwise Blender's FBX exporter will try to export whats inside of it
                #might add a little tickbox to the interactive exporter that lets you choose if you want it to export these as well or not idk
                layout.label(text = ("NLA track has " + str(len(item.strips)) + " strips! Track will be removed upon export."), icon = "ERROR")
        
        elif self.layout_type in {'GRID'}:
            pass#dunno what this does

class CONTROLS_ACTION_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        if self.layout_type in {'DEFAULT', 'GRID'}:
            #display name of action
            row = layout.row()

            if item.use_fake_user == False:
                row.prop(item, "name", text="", emboss=False, icon="FAKE_USER_OFF")
                row.operator("squadrig.action_add_fake_user", text = "ADD FAKE USER", icon= "FAKE_USER_OFF").action_name = item.name
            else:
                row.prop(item, "name", text="", emboss=False, icon="ACTION")
            #row.operator("wm.call_menu", text = "", icon = 'ADD' ).name = "OBJECT_MT_link_action"

        elif self.layout_type in {'GRID'}:
            pass