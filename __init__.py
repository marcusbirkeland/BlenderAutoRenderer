bl_info = {
    "name": "BlenderAutoRenderer",
    "author": "Zprite",
    "version": (0, 2, 00),
    "blender": (2, 80, 0),
    "location": "Output Properties",
    "description": "Auto Renderer",
    "category": "Rendering"}

import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty

class BlenderAutoRenderer_Export(bpy.types.Panel):
    bl_label = "Blender Auto Renderer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_option = {"DEFAULT_CLOSED"}

    input_path : StringProperty(default='None')
    output_path : StringProperty(default='None')

    num_cameras : IntProperty()
    radius_offset : FloatProperty()
    z_offset : FloatProperty()

    place_light : BoolProperty(default=True)
    light_intensity : FloatProperty()
    light_angle : FloatProperty()

    def draw(self, context):
        layout = self.layout
        


def register():
    bpy.utils.register_class(BlenderAutoRenderer_Export)

def unregister():
    bpy.utils.unregister_class(BlenderAutoRenderer_Export)

if __name__ == '__main__':
    register()