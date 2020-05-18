import bpy

bpy.ops.object.camera_add(location=(23.42714, -23.42714, 37.4478)) # Create Camera. I would love to set the rotation here too. Blender not. Not that there are no tutorials around which shows that it should work ... .

#So that's what the next two lines are good for. Setting the rotation of the camera ...

object = bpy.context.active_object
object.rotation_euler = (0.724312, 0, 0.785398)#Attention, these are radians. Euler angles are (41.5,0,45) Here we set the rotation for a isometric view that is used in 2D games. Not to mix with the mathematical correct Isoview!

# ------------------------------Here we adjust some settings ---------------------------------
object.data.type = 'ORTHO' # We want Iso, so set the type of the camera to orthographic
object.data.ortho_scale = 14.123  # Let's fit the camera to our basetile in size of 10
object.name = "GameIso4to3Cam" # let's rename the cam so that it cannot be confused with other cameras.
bpy.ops.view3d.object_as_camera() # Set the current camera as the active one to look through
