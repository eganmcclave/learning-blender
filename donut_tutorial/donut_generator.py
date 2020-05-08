
# Standard library imports
from random import random, sample, shuffle, uniform

# Third party library imports
import bpy
import bmesh

# Local library imports


######################
# Reusable functions #
######################

def rename_last_mesh(new_name):
    # Wrap to catch index errors for no objects
    try:
        # Change name and data.name the last object
        ob = bpy.context.selected_objects[-1]
        ob.name = new_name
        if ob.data.name is not None:
            ob.data.name = new_name
    except IndexError as err:
        pass
    

def select_vertices(prop=0.03, vertex_fxn_crit=lambda v: True):
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()

    # Get active mesh
    me = bpy.context.edit_object.data

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.select_flush(True)

    # Modify the BMesh
    for v in bm.verts:
        if random() < prop and vertex_fxn_crit(v):
            v.select = True
        else:
            v.select = False
            
    # Show the updates and recalculate n-gon tessellation
    bmesh.update_edit_mesh(me, True)


def select_faces(vertex_fxn_crit=lambda v: v.co.z > 0):
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
        
    # Get active mesh
    me = bpy.context.edit_object.data

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None

    # Modify the BMesh, can do anything here...
    for f in bm.faces:
        if all([vertex_fxn_crit(v) for v in f.verts]):
            f.select = True   
        else:
            f.select = False         
        
    # Show the updates and recalculate n-gon tessellation
    bmesh.update_edit_mesh(me, True)


def shift_vertices_along_axes(n_axes=1, shift_min=-0.008, shift_max=0.009, p_size=0.0355841):
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
        
    # Uniformly select random values between min/max provided then shuffle them
    shift_values = [uniform(shift_min, shift_max) for _ in range(n_axes)] + \
        [0 for _ in range(3-n_axes)]
    shuffle(shift_values)
    
    # Limit movement to the appropriate axes
    constraint_axis = [bool(value) for value in shift_values]
    
    # Translate the vertices based on specifications above
    bpy.ops.transform.translate(
        value=shift_values, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL', constraint_axis=constraint_axis, mirror=True, 
        use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=p_size, 
        use_proportional_connected=False, use_proportional_projected=False
    )
    
    # Switch back into edit mode
    bpy.ops.object.editmode_toggle()


def shift_duplicated_faces(shift_dims=[0, 0, 0]):
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
    
    # Duplicate and shift selected faces of a given mesh
    bpy.ops.mesh.duplicate_move(
        MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={
            "value":shift_dims, "orient_type":'GLOBAL', 
            "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', 
            "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, 
            "proportional_edit_falloff":'SMOOTH', "proportional_size":1, 
            "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, 
            "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, 
            "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, 
            "texture_space":False, "remove_on_cancel":False, "release_confirm":False, 
            "use_accurate":False
        }
    )
    
    # Initialize the duplicated mesh as a separte mesh
    bpy.ops.mesh.separate(type='SELECTED')
    
    # Switch back into edit mode
    bpy.ops.object.editmode_toggle()


###############
# Set-up Code #
###############

# Enables Proportional Editing mode
bpy.context.scene.tool_settings.use_proportional_edit = True

# Checks if in `Edit` mode and toggle to `Object` mode
if 'EDIT' in bpy.context.mode:
    bpy.ops.object.editmode_toggle()

# Deletes all existing objects in scene
bpy.ops.object.delete(use_global=False)

# Removes their mesh data as well
for k in bpy.data.meshes.keys():
    mesh = bpy.data.meshes[k]
    bpy.data.meshes.remove(mesh)

#######################
# Dobut Creation Code #
#######################

# Converts units to Metric Unit System
bpy.context.scene.unit_settings.system = 'METRIC'

# Converts units to Imperial Unit System
#bpy.context.scene.unit_settings.system = 'IMPERIAL'

# Add torus mesh object
bpy.ops.mesh.primitive_torus_add(
    align='WORLD', major_segments=28, minor_segments=12, major_radius=0.0325, minor_radius=0.0151
)
rename_last_mesh('Donut')

# Select and alter vertices to give imperfections
select_vertices()
shift_vertices_along_axes()

# Add Subdivision Surface modifier to increase subdivisions
bpy.ops.object.modifier_add(type='SUBSURF')

## Select and duplicated faces on top of object to create glaze
select_faces()
shift_duplicated_faces()
rename_last_mesh('Icing')

