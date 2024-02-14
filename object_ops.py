import bpy
from mathutils import Euler, Vector
import string
import random
import bmesh
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty

def getsquadrig(self):
    squadrigs = []
            
    for object in bpy.data.objects:
        try:
            if(object.get("squadrigtype") == 'character_control_rig'):
                squadrigs.append(object)
        except (AttributeError, KeyError, TypeError):
            continue
    if(len(squadrigs) == 0):
        #NO SQUAD RIGS
        self.report({'WARNING'}, 'No Squad rigs in scene!')
    if(len(squadrigs) == 1):
        #ONE SQUAD RIG
        #just pick the one squad rig in the scene
        return squadrigs[0]
    elif(len(squadrigs) > 1):
        #MULTIPLE SQUAD RIGS

        #if squad rig is active object
        if bpy.context.active_object.get("squadrigtype") == 'character_control_rig':
            return bpy.context.active_object

        #if exactly two objects are selected, get the one thats the squad rig
        #if both selected are squad rigs then its just whichever gets chosen on the first iteration of the for loop lol
        elif len(bpy.context.selected_objects) == 2:
            for object in bpy.context.selected_objects:
                if(object.get("squadrigtype") == 'character_control_rig'):
                    return object
    else:
        self.report({'WARNING'}, 'Couldn\'t find a squad rig.')
        return None
def is_squadrig_active():
    try:
        if(bpy.context.active_object.get("squadrigtype") == 'character_control_rig'):
            return True
    except (AttributeError, KeyError, TypeError):
        return False

def update_rig_skin(squadrig, rig_skin_root):

    for object in bpy.data.objects:
        if object.get("squadrigskinofid") == squadrig.get("squadrigid") and object.get("squadrigskinofid") != None:
            bpy.data.objects.remove(object, do_unlink=True)

    new_skin = rig_skin_root.copy()
    new_skin.name = rig_skin_root.name.replace("_skin_template","")
    #new_skin.name = rig_skin_root.name + "_skin"

    view_layer = bpy.context.view_layer
    view_layer.active_layer_collection.collection.objects.link(new_skin)
    new_skin.select_set(False)
            
    new_skin.parent = squadrig

    armature_modifier = new_skin.modifiers.new("SQRIG_armature", 'ARMATURE')
    armature_modifier.object = squadrig


    new_skin["squadrigskinid"] = rig_skin_root.get("squadrigrootskinid")
    #new_skin["squadrigrootskinid"] = None
    del new_skin["squadrigrootskinid"]
    new_skin["squadrigskinofid"] = squadrig.get("squadrigid")

    return new_skin

def GetDropAt(muzzle_velocity,gravity_scale,distance):
    gravity = -980
    unit_scale_diff = 100
    muzzle_velocity = muzzle_velocity/100
    gravity = gravity/100
    
    speed = muzzle_velocity
    flight_time = distance/muzzle_velocity
    gravity = gravity*gravity_scale
    drop = (0.5*gravity)*(distance/speed)**2
    
    return drop

class SquadRig_OT_AttachToSquadRig(bpy.types.Operator):
    """Attaches object to squad rig's weapon bone"""
    bl_idname = "squadrig.attach_to_weaponbone"
    bl_label = "Attach to object to weapon bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and not is_squadrig_active()

    def execute(self, context):
        ob = bpy.context.view_layer.objects.active

        squadrig = getsquadrig(self)
        if squadrig is not None:
            constraint = ob.constraints.new('COPY_TRANSFORMS')
            constraint.name = "SQRig_attach"
            constraint.target = squadrig
            constraint.subtarget = "SUP_Weapon1_ATTACH"
            ob["squadrigattachedtoid"] = str(squadrig.get("squadrigid"))
        
        return {'FINISHED'}
    
class SquadRig_OT_MakeCharacterSkin(bpy.types.Operator):
    """Makes active object available for selection in the rig controls"""
    bl_idname = "squadrig.make_character_skin"
    bl_label = "Make active object available for selection in the rig controls"
    bl_options = {"REGISTER","UNDO"}
    
    preserve_volume : bpy.props.BoolProperty(
    name='Preserve Volume',
    description='Make armature modifier use "Preserve Volune"',
    default=False)
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and not is_squadrig_active() and context.active_object.type == "MESH"
    
    def execute(self, context):
        ob = bpy.context.view_layer.objects.active
        #squadrig = getsquadrig(self)
        
        
        #goal of this code block is to standardize the transform of the mesh to being 100x as big as its supposed to be and facing y+
        ob.parent = None
        ob.rotation_euler = 0,0,-1.57079632679
        ob.location = 0,0,0
        bpy.context.view_layer.update()
        #if the model isnt already nearish the right dimensions for being the correct scale, then scale it up
        if ob.dimensions <= Vector((20,20,100)):
            ob.scale = ob.scale * 100
        if ob.dimensions.x > ob.dimensions.y:
            #safe to assume here that the mesh is facing Y+ in its rest position
            #so we account for that
            ob.rotation_euler = 0,0,0

        
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        ob.name = ob.name + "_skin_template"
        #generate id
        ob['squadrigrootskinid'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        #ob.parent = squadrig
        ob.location = 0,0,0#squadrig.location
        #ob.rotation_euler = Euler((0, 0, 4.71239))
        
        bpy.context.active_object.use_fake_user = True
        bpy.context.active_object.users_collection[0].objects.unlink(ob)
        
        
        #bpy.ops.squadrig.change_character_object(new_object_name=ob.name)
        squadrig = getsquadrig(self)
        if squadrig is not None:
            view_layer = bpy.context.view_layer
            new_skin = update_rig_skin(squadrig, ob)
            new_skin.select_set(True)
            view_layer.objects.active = new_skin
        
        return {'FINISHED'}

class SquadRig_OT_RemoveCharacterSkin(bpy.types.Operator):
    """Purges rig skin from blend file."""
    bl_idname = "squadrig.remove_character_skin"
    bl_label = "Purges rig skin from blend file."
    bl_options = {"REGISTER","UNDO"}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH" and context.active_object.get("squadrigskinid") is not None
    
    def execute(self, context):
        ob = context.active_object
        
        skin_id = ob.get("squadrigskinid")
        if skin_id == None:
            skin_id = ob.get("squadrigrootskinid")


        for object in bpy.data.objects:
            if object.get("squadrigrootskinid") != None or object.get("squadrigskinid") != None:
                if object.get("squadrigrootskinid") == skin_id or object.get("squadrigskinid") ==skin_id:
                    bpy.data.objects.remove(object, do_unlink=True)

        return {'FINISHED'}

class SquadRig_OT_DetachCharacterSkin(bpy.types.Operator):
    """Removes object from rig controls skin"""
    bl_idname = "squadrig.detach_character_skin"
    bl_label = "Removes object from rig controls skin"
    bl_options = {"REGISTER","UNDO"}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "MESH"
    
    def execute(self, context):
        ob = context.active_object
        
        ob.parent = None
        ob.scale = (0.01,0.01,0.01)
        #ob.rotation_euler = Euler(0,0,1.57079632679)

        new_data = ob.data.copy()
        ob.data = new_data

        
        for modifier in ob.modifiers:
            if modifier.type == "ARMATURE":
                if modifier.object == getsquadrig(self) or modifier.name == "SQRIG_armature":
                    ob.modifiers.remove(modifier)
        
        vertexgroups = ob.vertex_groups
        for v_group in vertexgroups:
            name = v_group.name
            if '_L' in name and '_DEF_' in name:
                name = name.replace('_L', '')
                name = name.replace('_DEF_', '_L_')
            
            if '_R' in name and '_DEF_' in name:
                name = name.replace('_R', '')
                name = name.replace('_DEF_', '_R_')
            v_group.name = name
        
        ob.name = ob.name.replace("_skin_instance","")
        if ob.get("squadrigskinid") != None:
            del ob["squadrigskinid"]
        if ob.get("squadrigskinofid") != None:
            del ob["squadrigskinofid"]
        if ob.get("squadrigrootskinid") != None:
            del ob["squadrigrootskinid"]

        return {'FINISHED'}
    
class SquadRig_OT_DetachFromSquadRig(bpy.types.Operator):
    """Detaches object from squad rig's weapon bone"""
    bl_idname = "squadrig.detach_from_weaponbone"
    bl_label = "Detach object from weapon bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and not is_squadrig_active()

    def execute(self, context):
        ob = bpy.context.view_layer.objects.active
        
        for constraint in ob.constraints:
            #make sure were getting the constraints we made before even if the user changed them slightly
            if constraint.type == "COPY_TRANSFORMS":
                if constraint.subtarget == "SUP_Weapon1_ATTACH" or constraint.name == "SQRig_attach":
                    ob.constraints.remove(constraint)
        
        ob.rotation_euler = (0,0,0)
        ob.lock_rotation = (False,False,False)


        return {'FINISHED'}
    
class SquadRig_OT_MakeChildOf(bpy.types.Operator):
    """Attaches bone to squad rig"""
    bl_idname = "squadrig.make_child_of"
    bl_label = "Attach bone to squad rig"
    
    attach_target_bone : bpy.props.StringProperty("")
    
    @classmethod
    def poll(cls, context):
        return context.active_pose_bone is not None and not is_squadrig_active()

    def execute(self, context):
        ob = bpy.context.view_layer.objects.active

        #squadrig = getsquadrig(self)
        for object in bpy.data.objects:
            if object.get("squadrigid") == ob.get("squadrigattachedtoid"):
                squadrig = object
                break

        if squadrig is not None:
            constraint = context.active_pose_bone.constraints.new('CHILD_OF')
            constraint.target = squadrig
            constraint.subtarget = self.attach_target_bone
            constraint.name = "SQRig_attach_" + self.attach_target_bone
        else:
            self.report({'WARNING'}, 'No Squad rigs in scene!')

        return {'FINISHED'}

class SquadRig_OT_ChangeCharacterMesh(bpy.types.Operator):

    bl_idname = "squadrig.change_character_object"
    bl_label = "Changes Squad Character Object"
    bl_options = {"REGISTER","UNDO"}
    
    new_object_name : bpy.props.StringProperty("new_object_name")
    #object_name : bpy.props.StringProperty("object", default = "SQRIG_character_mesh")
    
    def execute(self, context):

        if self.new_object_name in bpy.data.objects:
            squadrig = bpy.context.active_object

            update_rig_skin(squadrig, bpy.data.objects[self.new_object_name])

        return {'FINISHED'}

class SquadRig_MT_CharacterMeshSelector(bpy.types.Menu):
    bl_label = "Character Mesh Selector Menu"
    bl_idname = "OBJECT_MT_squad_character_mesh_selector_menu"

    def draw(self, context):
        layout = self.layout
        for object in bpy.data.objects:
            #if "SQ_char" in object.name:
            if object.get("squadrigrootskinid") != None:
                #object_visual_name = object.name.replace("SQ_char_","")
                object_visual_name = object.name.replace("_skin_template","")
                
                if object.users > 0:#mesh is safe
                    icon = "COMMUNITY"
                else:#mesh has no users and will be lost upon blender restart
                    icon = "GHOST_DISABLED"
                
                row = layout.row()
                op = row.operator("squadrig.change_character_object", text = object_visual_name, icon = icon).new_object_name = object.name


class SquadRig_OT_CreateRangingObject(bpy.types.Operator):
    bl_idname = "squadrig.create_ranging_object"
    bl_label = "Creates object for setting up ranging in optics."
    bl_options = {"REGISTER","UNDO"}
    
    

    max_distance : IntProperty(
        name="Range",
        description="Range to draw ranging line out to.",
        default=1000,
        soft_max = 2000,
        soft_min = 0
    )

    muzzle_velocity : FloatProperty(
        name="Muzzle Velocity",
        description="Muzzle velocity of the projectile in cm/s",
        default=60000.0,
        soft_max = 100000.0,
        soft_min = 0.0
    )

    gravity_scale : FloatProperty(
        name="Gravity Scale",
        description="Gravity scalar for projectile.",
        default=1.0,
        soft_max = 2.0,
        soft_min = 0.0
    )

    ladder_width : FloatProperty(
        name="Ladder Width",
        description="Width of the range ladder steps.",
        default=5.0,
        soft_max = 20.0,
        soft_min = 0.0
    )
    ladder_step : FloatProperty(
        name="Ladder Step",
        description="Distance in meters between ladder steps.",
        default=100.0,
        soft_max = 1500.0,
        soft_min = 0.0
    )
    depth : IntProperty(
        name="Step",
        description="Distance between vertices in meters.",
        default= 5,
        soft_max = 100,
        soft_min = 0
    )
    make_grease_pencil : BoolProperty(
        name="Make Grease Pencil",
        description="Convert the generated mesh to a grease pencil object.",
        default = True
    )


    


    def execute(self, context):
        bm = bmesh.new()

        first_vert = bmesh.ops.create_vert(bm, co=(0,0,0))
        last_vert = first_vert['vert'][0]

        ranging_distances = range(0, self.max_distance + 1, self.depth)
        for distance in ranging_distances:
            if distance != 0:
                extrude = bmesh.ops.extrude_vert_indiv(bm, verts=[last_vert], use_select_history=False)
                last_vert = extrude['verts'][0]
                drop = GetDropAt(self.muzzle_velocity,self.gravity_scale,distance)
                last_vert.co = [distance,0,drop]
                
                if distance % self.ladder_step == 00:
                    #ladder
                    first_ladder_vert = bmesh.ops.create_vert(bm, co=(distance,self.ladder_width/2,drop))
                    ladder_extrude = bmesh.ops.extrude_vert_indiv(bm, verts=[first_ladder_vert['vert'][0]], use_select_history=False)
                    last_ladder_vert = ladder_extrude['verts'][0]
                    last_ladder_vert.co = [distance,-self.ladder_width/2,drop]
        

        # Finish up, write the bmesh into a new mesh
        me = bpy.data.meshes.new("Ranging_Mesh")
        bm.to_mesh(me)
        bm.free()
        
        # Add the mesh to the scene
        obj = bpy.data.objects.new("Ranging_Object", me)
        bpy.context.collection.objects.link(obj)

        # Select and make active
        for object in bpy.data.objects:
            object.select_set(False)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        obj.location = bpy.context.scene.cursor.location
        
        
        #gpencil stuff
        if (self.make_grease_pencil == True):
            bpy.ops.object.convert(target='GPENCIL')
            
            obj = bpy.context.active_object
            obj.name = 'Ranging_Object'
            obj.use_grease_pencil_lights = False
            obj.data.stroke_thickness_space = "SCREENSPACE"
            obj.data.layers[0].line_change = -100
            
            obj.material_slots[0].material.name = '_mat'
            obj.material_slots[0].material.grease_pencil.color = [1,1,1,1]

        return {'FINISHED'}