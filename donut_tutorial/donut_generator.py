
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
    

def select_border_edges(prop=0.25):
    
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
        
    # Get the active mesh
    me = bpy.context.edit_object.data

    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None

    for f in bm.faces:
        for e in f.edges:
            if len(e.link_faces) == 1 and random() < prop:
                e.select = True    

    # Show the updates in the viewport
    bmesh.update_edit_mesh(me, True)
    
    
def shift_vertices_along_axes(n_axes=1, shift_min=-0.008, shift_max=0.009, p_size=0.0355841,
    force_coords=(False, False, False)):

    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
        
    # Uniformly select random values between min/max provided then shuffle them
    values = [uniform(shift_min, shift_max) for _ in range(n_axes)]
    zeros = [0 for _ in range(3-n_axes)]

    if force_coords[0]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(0, values[0])
    elif force_coords[1]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(1, values[0])
    elif force_coords[2]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(2, values[0])
    else:
        shift_values = values + zeros
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

    # Deselect all components of mesh object
    bpy.ops.mesh.select_all(action='DESELECT')
        
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
    
    # Deselect all components of mesh object
    bpy.ops.mesh.select_all(action='DESELECT')

    # Switch back into edit mode
    bpy.ops.object.editmode_toggle()


def extrude_edges(n_axes=1, shift_min=-0.002, shift_max=0.002, p_size=0.0200863,
    force_coords=(False, False, False)):
        
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()

    # Uniformly select random values between min/max provided then shuffle them
    values = [uniform(shift_min, shift_max) for _ in range(n_axes)]
    zeros = [0 for _ in range(3-n_axes)]

    if force_coords[0]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(0, values[0])
    elif force_coords[1]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(1, values[0])
    elif force_coords[2]:
        shift_values = values[1:] + zeros
        shuffle(shift_values)
        shift_values.insert(2, values[0])
    else:
        shift_values = values + zeros
        shuffle(shift_values)
                    
    # Extrudes the selected edges by a given amount
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, 
        TRANSFORM_OT_translate={
            "value":shift_values, "orient_type":'GLOBAL', 
            "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
            "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), 
            "mirror":False, "use_proportional_edit":False, 
            "proportional_edit_falloff":'SHARP', "proportional_size":p_size, 
            "use_proportional_connected":False, "use_proportional_projected":False, 
            "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), 
            "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, 
            "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, 
            "release_confirm":False, "use_accurate":False
        }
    )

    # Deselect all components of mesh object
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Switch back into edit mode
    bpy.ops.object.editmode_toggle()
        

def resize(val=0.2, p_size=0.0137192):
    
    # Checks if in `Edit` mode and toggle to `Object` mode
    if 'EDIT' not in bpy.context.mode:
        bpy.ops.object.editmode_toggle()
        
    bpy.ops.transform.resize(
        value=(val, val, val), orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
        mirror=True, use_proportional_edit=True, proportional_edit_falloff='SHARP', 
        proportional_size=p_size, use_proportional_connected=False, 
        use_proportional_projected=False
    )
    
    # Deselect all components of mesh object
    bpy.ops.mesh.select_all(action='DESELECT')
    
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
# Donut Creation Code #
#######################

# Converts units to Metric Unit System
bpy.context.scene.unit_settings.system = 'METRIC'

# Converts units to Imperial Unit System
#bpy.context.scene.unit_settings.system = 'IMPERIAL'

# Add torus mesh object and name it `Donut`
bpy.ops.mesh.primitive_torus_add(
    align='WORLD', major_segments=28, minor_segments=12, major_radius=0.0325, minor_radius=0.0151
)
rename_last_mesh('Donut')

# Add Subdivision Surface modifier to increase subdivisions
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.context.object.modifiers["Subdivision"].levels = 2

# Select and alter vertices to give imperfections
select_vertices()
shift_vertices_along_axes(2, -0.003, 0.003, 0.017, force_coords=(True, False, True))

select_vertices()
shift_vertices_along_axes(1, -0.003, 0.0015, 0.02, force_coords=(False, False, True))

# Select and duplicated faces on top of object to create glaze
select_faces()
shift_duplicated_faces()
rename_last_mesh('Icing')

# Change the active object to `Icing` and apply the Solidify modifier
bpy.context.view_layer.objects.active = bpy.data.objects['Icing']
bpy.ops.object.modifier_add(type='SOLIDIFY')

# Change placement of Solidify modifier and the thickness & offset values
bpy.ops.object.modifier_move_up(modifier="Solidify")
bpy.context.object.modifiers["Solidify"].thickness = 0.0015
bpy.context.object.modifiers["Solidify"].offset = 1
bpy.context.object.modifiers["Solidify"].edge_crease_inner = 1

# Add subdivide modifier to `Icing`
select_faces()
bpy.ops.mesh.subdivide(smoothness=1)
bpy.ops.mesh.select_all(action='DESELECT')

# Change snap element settings
bpy.context.scene.tool_settings.use_snap = True
bpy.context.scene.tool_settings.snap_elements = {'FACE'}
bpy.context.scene.tool_settings.use_snap_project = True

# Change proportional edit settings
bpy.context.scene.tool_settings.proportional_edit_falloff = 'SHARP'

# Repeatedly grab border edges and extrude them at different ranges
select_border_edges(prop=0.5)
shift_vertices_along_axes(1, -0.003, 0, 0.010, (False, False, True))

select_border_edges(prop=0.03)
extrude_edges(1, -0.003, 0, force_coords=(False, False, True))
resize(val=0.4)

#select_border_edges(prop=0.05)
#extrude_edges(1, -0.003, 0, p_size=0.08, force_coords=(False, False, True))
#resize(val=0.8)

# Change proportional edit settings back to normal
bpy.context.scene.tool_settings.proportional_edit_falloff = 'SMOOTH'

# Change snap element settings back to normal
bpy.context.scene.tool_settings.use_snap_project = False
bpy.context.scene.tool_settings.snap_elements = {'INCREMENT'}
bpy.context.scene.tool_settings.use_snap = False
