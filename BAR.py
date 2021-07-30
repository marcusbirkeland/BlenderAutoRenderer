import bpy
from mathutils import Vector
import math
import os
import sys

# Remove 1st argument from the
# list of command line arguments

# COMMAND TO RUN : blender -b -P blenderAutoRender.py "indir" "outdir"

argumentList = sys.argv[3:]
 
# -----------------------------------------------------------------------------


""" add_cameras
- (string) 	target_name
            name of the 'to be caputred' object in blender 
- (int) 	levels
            number of levels in z direction
- (int) 	density
            number of cameras on one level
- (int) 	r_offset
            offset distance for the radius
- (int) 	z_offset
            offset distance in z direction
            
>>> None
add_cameras places cameras around the target object according to the given
parameters. The placement is based on the bounding box of the target object.
Offsets are based on the side length of the bounding box.
"""

def joinAllObjects():
    #Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    ARM_OBJS = []
    MSH_OBJS = []
    
    try:
    
        ARM_OBJS = [m for m in bpy.context.scene.objects if m.type == 'ARMATURE']
        
    except:
        print("there was no collection")
        
    #delete armature
    if(len(ARM_OBJS) > 0):
        bpy.data.objects.remove(ARM_OBJS[0])

    try:
        #Mesh objects

        MSH_OBJS = [m for m in bpy.context.scene.objects if m.type == 'MESH']
    
    except:
        print("there was no collection")
        
    finally:

        for OBJS in MSH_OBJS:
            #Select all mesh objects
            OBJS.select_set(state=True)

            #Makes one active
            bpy.context.view_layer.objects.active = OBJS
        #Joins objects
        try:
            bpy.ops.object.join()
        except:
            print("unable to join objects")
    
def getFirstObject():
    objectName = ""   
    try:
        objectName = bpy.data.collections[0].objects[0].name
    except:
        try:
            objectName = bpy.context.scene.objects[0].name
        except:
            return ""
    return  objectName

def add_cameras(target_name='target', levels=0, density=4, r_offset=1.5, z_offset=8):
    if(target_name==""):
        return
    # find target object
    target_obj = bpy.data.objects[target_name]
    target_origin = target_obj.location
    # get bounding box side lengths
    bb_sides = get_min(target_obj.bound_box) - get_max(target_obj.bound_box)
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
            
            


""" get_min
- (bound_box)	bound_box
                utilized bound_box
>>> (Vector) (x,y,z)
get_min estimates the minimal x, y, z values
"""
def get_min(bound_box):
    min_x = min([bound_box[i][0] for i in range(0, 8)])
    min_y = min([bound_box[i][1] for i in range(0, 8)])
    min_z = min([bound_box[i][2] for i in range(0, 8)])
    return Vector((min_x, min_y, min_z))


""" get_max
- (bound_box)	bound_box
                utilized bound_box
>>> (Vector) (x,y,z)
get_max estimates the maximal x, y, z values
"""
def get_max(bound_box):
    max_x = max([bound_box[i][0] for i in range(0, 8)])
    max_y = max([bound_box[i][1] for i in range(0, 8)])
    max_z = max([bound_box[i][2] for i in range(0, 8)])
    return Vector((max_x, max_y, max_z))


def get_origin(v1, v2):
     return v1 + 0.5 * (v2 - v1)


""" capture
- (string)	path
            path to image directory
>>> None
this function iterates over all camera and renders their viewpoint
"""
def capture(path, filename):
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
            bpy.context.scene.render.film_transparent = True
            bpy.ops.render.render(write_still=True)
            counter += 1
                  
        
def clearScene():
    all_data = bpy.data.objects
    for obj in all_data:
        bpy.data.objects.remove(obj, do_unlink=True)
    
def addLight():
    # create light datablock, set attributes
    light_data = bpy.data.lights.new(name="ambient", type='SUN')
    light_data.energy = 10

    # create new object with our light datablock
    light_object = bpy.data.objects.new(name="ambient", object_data=light_data)

    # link light object
    bpy.context.collection.objects.link(light_object)

    # make it active 
    bpy.context.view_layer.objects.active = light_object

    #change location
    light_object.location = (5, 5, 5)

    # update scene, if needed
    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()    

def main (dir_path , output_folder):
    addLight()
    files = [f for f in os.listdir(dir_path) if os.path.isfile (os.path.join(dir_path,f))]
    for f in files:
        filepath = dir_path + "/" + f 
        if f.endswith('.dtt'):
            try:
                bpy.ops.import_scene.dtt_data(filepath = filepath, reset_blend = False)
            except:
                print("could not open .dtt, continuing")
                continue

            joinAllObjects()
            add_cameras(getFirstObject())
            capture(output_folder,f)
            deleteCollection()
    print("\n\n-----------------------------------\n\nRendering completed! \n\n")
            
# use for objects imported manually into the scene
def captureScene(f = "filename.dtt"):
    joinAllObjects()
    add_cameras(getFirstObject())
    capture('C:/tmp/render',f)
    deleteCollection()

