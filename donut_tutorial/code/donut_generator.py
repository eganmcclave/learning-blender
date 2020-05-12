
# Standard library imports
from random import random, sample, shuffle, uniform

# Third party library imports
import bpy
import bmesh

# Local library imports
from bpy_helper import *


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

select_border_edges(prop=0.01)
extrude_edges(1, -0.005, 0, force_coords=(False, False, True))
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

