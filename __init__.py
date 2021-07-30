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

class BARProps(bpy.types.PropertyGroup):
    input_path : StringProperty(default='None')
    output_path : StringProperty(default='None')

    num_cameras : IntProperty()
    radius_offset : FloatProperty()
    z_offset : FloatProperty()

    place_light : BoolProperty(default=True)
    light_intensity : FloatProperty()
    light_angle : FloatProperty()

class BAR_PT_Export(bpy.types.Panel):
    bl_label = "Blender Auto Renderer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_option = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.BARData, "input_path", text="Input Path:")
        layout.prop(context.scene.BARData, "output_path", text="Output Path:")


def register():
    bpy.utils.register_class(BARProps)
    bpy.utils.register_class(BAR_PT_Export)
    
    bpy.types.Scene.BARData = bpy.props.PointerProperty(type=BARProps)

def unregister():
    bpy.utils.unregister_class(BARProps)
    bpy.utils.unregister_class(BAR_PT_Export)

if __name__ == '__main__':
    register()