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

    num_cameras : IntProperty(min = 1, max = 360)
    radius_offset : FloatProperty(min = 0, max = 2000)
    z_offset : FloatProperty()

    place_light : BoolProperty(default=True)
    light_intensity : FloatProperty(min = 0)
    light_angle : FloatProperty(min = 0, max = 360)


class BARExecuteButton(bpy.types.Operator):
    """Execute Batch Render"""
    bl_idname = "bar.exec_render"
    bl_label = "Execute Batch Render"
    
    def execute(self, context):
        from .BAR import main
        main(dir_path = context.scene.BARData.input_path, output_folder=context.scene.BARData.output_path)
        return{"FINISHED"}
        

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
        #CAMERAS
        layout.label(text = "Cameras")
        layout.prop(context.scene.BARData, "num_cameras", text="Num Cameras")
        layout.prop(context.scene.BARData, "radius_offset", text="Radius Offset")
        layout.prop(context.scene.BARData, "z_offset", text="Z-Offset")

        #LIGHT
        layout.label(text = "Light")
        layout.prop(context.scene.BARData, "place_light", text="Place Light (SUN)")
        layout.prop(context.scene.BARData, "light_intensity", text="Light Intensity")
        layout.prop(context.scene.BARData, "light_angle", text="Light Angle")
        #PATHS
        input_path_row = layout.row()
        input_path_row.prop(context.scene.BARData, "input_path", text="Input Path")
        input_path_row.operator("bar.select_path", icon="FILE_FOLDER", text="").path_type = "input_path"

        output_path_row = layout.row()
        output_path_row.prop(context.scene.BARData, "output_path", text="Output Path")
        output_path_row.operator("bar.select_path", icon="FILE_FOLDER", text="").path_type = "output_path"
        layout.operator("bar.exec_render")


def register():
    bpy.utils.register_class(BARProps)
    bpy.utils.register_class(BARPathSelector)
    bpy.utils.register_class(BARExecuteButton)
    bpy.utils.register_class(BAR_PT_Export)
    
    bpy.types.Scene.BARData = bpy.props.PointerProperty(type=BARProps)

def unregister():
    bpy.utils.unregister_class(BARProps)
    bpy.utils.unregister_class(BARPathSelector)
    bpy.utils.unregister_class(BARExecuteButton)
    bpy.utils.unregister_class(BAR_PT_Export)

if __name__ == '__main__':
    register()