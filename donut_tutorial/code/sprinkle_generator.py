
# Standard library imports
from random import random, sample, shuffle, uniform

# Third party library imports
import bpy
import bmesh

# Local library imports
from bpy_helper import *


##########################
# Sprinkle Creation Code #
##########################

rad_val = uniform(0.0005, 0.0015)
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=12, ring_count=6, radius=rad_val, enter_editmode=False, location=(0, 0, 0)
)

select_faces(lambda v: v.co.z >= -0.0001)
extrude_edges(shift_min=0.002, shift_max=0.005, force_coords=(False, False, True), exit_edit_mode=False)
resize(n_axes=1, shift_min=0.1, shift_max=0.3, p_size=1, force_coords=(False, False, True))
select_faces(lambda v: v.co.z < 0.0001)
resize(n_axes=1, shift_min=0.1, shift_max=0.3, p_size=1, force_coords=(False, False, True))

