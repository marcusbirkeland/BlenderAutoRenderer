import bpy
from mathutils import Vector
import math
import os
import sys

#TODO: 
# 1. Find bounding box for ALL objects
# 2. Set cameras to target center of that box
        
# -----------------------------------------------------------------------------

# TO ADD CUSTOM IMPORTS, PASTE THIS into the elif chain:
""" 
elif f.endswith("[YOUR FILE EXTENSION]"):
        try:
            bpy.ops.[BLENDER COMMAND FOR IMPORT](filepath = filepath)
        except:
            print("could not open, continuing")
            return -1
"""


def import_file(dir_path, f):
    filepath = dir_path + "/" + f
    if f.endswith(".ply"):
        try:
            bpy.ops.import_mesh.ply(filepath = filepath)
            return 0
        except:
            print("could not open ply, continuing")
    elif f.endswith(".stl"):
        try:
            bpy.ops.import_mesh.stl(filepath = filepath)
            return 0
        except:
            print("could not open stl, continuing")
    elif f.endswith(".fbx"):
        try:
            bpy.ops.import_scene.fbx(filepath = filepath)
            return 0
        except:
            print("could not open fbx, continuing")
    elif f.endswith(".gltf") or f.endswith(".glb"):
        try:
            bpy.ops.import_scene.gltf(filepath = filepath)
            return 0
        except:
            print("could not open gltf/glb, continuing")             
    elif f.endswith(".obj"):
        try:
            bpy.ops.import_scene.obj(filepath = filepath)
            return 0
        except:
            print("could not open obj, continuing")
    elif f.endswith(".x3d") or f.endswith(".wrl"):
        try:
            bpy.ops.import_scene.x3d(filepath = filepath)
            return 0
        except:
            print("could not open x3d/wrl, continuing")
    elif f.endswith(".dtt"):
        try:
            bpy.ops.import_scene.dtt_data_ac(filepath = filepath, reset_blend = False)
            return 0
        except:
            print("could not open dtt, continuing")
    return -1  
  

def apply_all_transforms():
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            #print("NAME:" , obj.name)
            obj.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation= True, scale=True)
            obj.select_set(False)
    
def get_total_min_BB():

    objects = bpy.context.scene.objects
    min_x = objects[0].bound_box[0][0]
    min_y = objects[0].bound_box[0][1]
    min_z = objects[0].bound_box[0][2]

    for obj in objects:
        if obj.type == "MESH":
            temp_min_x = min([obj.bound_box[i][0] for i in range(0, 8)])
            temp_min_y = min([obj.bound_box[i][1] for i in range(0, 8)])
            temp_min_z = min([obj.bound_box[i][2] for i in range(0, 8)])
            if temp_min_x < min_x:
                min_x = temp_min_x
            if temp_min_y < min_y:
                min_y = temp_min_y
            if temp_min_z < min_z:
                min_z = temp_min_z 
    return Vector((min_x,min_y,min_z))
    
def get_total_max_BB():

    objects = bpy.context.scene.objects
    max_x = objects[0].bound_box[0][0]
    max_y = objects[0].bound_box[0][1]
    max_z = objects[0].bound_box[0][2]

    for obj in objects:
        if obj.type == "MESH":
            temp_max_x = max([obj.bound_box[i][0] for i in range(0, 8)])
            temp_max_y = max([obj.bound_box[i][1] for i in range(0, 8)])
            temp_max_z = max([obj.bound_box[i][2] for i in range(0, 8)])
            if temp_max_x > max_x:
                max_x = temp_max_x
            if temp_max_y > max_y:
                max_y = temp_max_y
            if temp_max_z > max_z:
                max_z = temp_max_z 
    return Vector((max_x,max_y,max_z))               

def getFirstObject():
    objectName = ""   
    try:
        objectName = bpy.data.objects[0].name
    except:
        return None
    return  objectName

def add_cameras(target_name='target', levels=0, density=4, r_offset=1.5, z_offset=8):
    if(target_name==""):
        return
    # find target object
    target_obj = bpy.data.objects[target_name]
    #target_origin = get_origin(get_min(target_obj.bound_box), get_max(target_obj.bound_box))
    target_origin = get_origin(get_total_max_BB(), get_total_min_BB())
    #print("Target origin:" , target_origin)

    # Set cursor to target_origin
    bpy.context.scene.cursor.location = target_origin
    #print("total max bb: ", get_total_max_BB())
    #print("total min bb:", get_total_min_BB())
    # Set origin to 3d-cursor
    target_obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    target_obj.select_set(False)

    # get bounding box side lengths
    bb_sides = get_total_min_BB() - get_total_max_BB()
    (dist_x, dist_y, dist_z) = tuple([abs(c) for c in bb_sides])
    originated_dist_y = .5 * dist_y
    # calc the radius by taking the longer side in x-y-direction + r_offset
    radius = 1.5 * max(dist_x, dist_z) + r_offset
    # iterate over number of levels
    # (levels / 2) above and under the origin and the origin itself 
    for l in range(-levels, levels + 1):
        # get actual z value
        # origin.z + offset based on current level and z_offset
        if(levels != 0):
            leveled_z = (l / levels) * (originated_dist_y + z_offset * originated_dist_y)
        else:
            leveled_z = 1  * (originated_dist_y + z_offset * originated_dist_y)
        z = target_origin.z + leveled_z
        # iterate over given density
        for angle in [(i * 2 * math.pi) / density for i in range(0, density)]:
            # estimate new direction based on the angle in the unit circle
            d = Vector((math.cos(angle), math.sin(angle)))
            (x, y) = Vector((target_origin.x, target_origin.y)) + radius * d
            # build absolute position 
            position = (x, y, z)
            # instantiate camera object
            camera = bpy.data.cameras.new('Camera')
            camera_obj = bpy.data.objects.new(camera.name, camera)
            camera_obj.location = Vector(position)	
            # Create a new collection and link it to the scene.
            # apply track-to constraint
            # Set up camera tracking
            ttc = camera_obj.constraints.new(type='TRACK_TO')
            ttc.target = target_obj
            ttc.track_axis = 'TRACK_NEGATIVE_Z'
            ttc.up_axis = 'UP_Y'
            bpy.ops.object.select_all(action='DESELECT')

            # Remove object from all collections not used in a scene
            bpy.ops.collection.objects_remove_all()
            # add it to our specific collection
            try:
                bpy.data.collections[0].objects.link(camera_obj)
            except:
                collection = bpy.data.collections.new("collection")
                bpy.data.collections[0].objects.link(camera_obj)
            bpy.ops.object.visual_transform_apply()
            #camera_obj.select_set(True)
            
def get_origin(v1, v2):
     return v1 + 0.5 * (v2 - v1)

def capture(path, filename, use_transparent):
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    # iterate over all objects
    counter = 0
    if(not bpy.data.collections):
        print("No objects to render!!! Continuing")
        return
    for ob in bpy.data.collections[0].objects:
        # make sure object is a camera
        if ob.type == 'CAMERA':
            # capture camera's view
            bpy.context.scene.camera = ob
            file = os.path.join(path, 'img', filename.split(".")[0] + "_" + str(counter))
            bpy.context.scene.render.filepath = file
            bpy.context.scene.render.image_settings.color_mode ='RGBA'
            bpy.context.scene.render.film_transparent = use_transparent
            bpy.ops.render.render(write_still=True)
            counter += 1
                    
def clearScene():
    all_data = bpy.data.objects
    for obj in all_data:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.outliner.orphans_purge()
    
def addLight(enabled,intensity, angle):
    if(not enabled):
        return
    # create light datablock, set attributes
    light_data = bpy.data.lights.new(name="ambient", type='SUN')
    light_data.energy = intensity
    light_data.angle = angle

    # create new object with our light datablock
    light_object = bpy.data.objects.new(name="ambient", object_data=light_data)

    # link light object
    bpy.context.collection.objects.link(light_object)

    # update scene, if needed
    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()    

def main (dir_path , output_folder, levels, density , r_offset, z_offset, enabled, intensity, angle, only_place, use_transparent):
    clearScene()
    files = [f for f in os.listdir(dir_path) if os.path.isfile (os.path.join(dir_path,f))]
    for f in files:
        if import_file(dir_path, f) == -1:
            continue
        apply_all_transforms()
        addLight(enabled, intensity, angle)
        add_cameras(getFirstObject(), levels, density, r_offset, z_offset)
        if only_place:
            return
        capture(output_folder,f, use_transparent)
        clearScene()
    print("\n\n-----------------------------------\n\nRendering completed! \n\n")

