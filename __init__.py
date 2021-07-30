bl_info = {
    "name": "BlenderAutoRenderer",
    "author": "Zprite",
    "version": (0, 2, 00),
    "blender": (2, 80, 0),
    "location": "Output Properties",
    "description": "Auto Renderer",
    "category": "Rendering"}

import bpy
import os
from bpy_extras.io_utils import ImportHelper
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

class BARPathSelector(bpy.types.Operator, ImportHelper):
    """Select Path"""
    bl_idname = "bar.select_path"
    bl_label = "Select Directory"
    filename_ext = ""

    dir_path : StringProperty(name = "", description="Select Directory:", subtype="DIR_PATH")
    path_type : StringProperty(options={"HIDDEN"})

    def execute(self, context):
        self.dir_path = self.filepath
        directory = os.path.dirname(self.dir_path)
        if self.path_type == "input_path":
            context.scene.BARData.input_path = directory
        elif self.path_type == "output_path":
            context.scene.BARData.output_path = directory
        else:
            print("Incorrect Path Type")

        return {"FINISHED"}

class BAR_PT_Export(bpy.types.Panel):
    bl_label = "Blender Auto Renderer"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_option = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        input_path_row = layout.row()
        input_path_row.prop(context.scene.BARData, "input_path", text="Input Path")
        input_path_row.operator("bar.select_path", icon="FILE_FOLDER", text="").path_type = "input_path"

        output_path_row = layout.row()
        output_path_row.prop(context.scene.BARData, "output_path", text="Output Path")
        output_path_row.operator("bar.select_path", icon="FILE_FOLDER", text="").path_type = "output_path"


def register():
    bpy.utils.register_class(BARProps)
    bpy.utils.register_class(BARPathSelector)
    bpy.utils.register_class(BAR_PT_Export)
    
    bpy.types.Scene.BARData = bpy.props.PointerProperty(type=BARProps)

def unregister():
    bpy.utils.unregister_class(BARProps)
    bpy.utils.unregister_class(BARPathSelector)
    bpy.utils.unregister_class(BAR_PT_Export)

if __name__ == '__main__':
    register()