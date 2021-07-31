# BlenderAutoRenderer

This script lets you automatically import and render files in Blender! 
Based off [this script.](https://gist.github.com/der-Daniel/cfc93a4661f47e66bfd4ebd81efbb943)

<img height="400" alt="output example" src="https://user-images.githubusercontent.com/36818485/123545506-a3322b00-d758-11eb-90e6-36227326429d.png">

## How to use 

1. Download this as a zip, and install and enable as a Blender 2.8+ Plugin.
2. "Blender Auto Renderer" should now be in the output properties tab.
3. Set the parameters for cameras and lighting, and then select the path to the folder with your import files as "Input Path". All files within this folder will automatically be imported, and then rendered.
4. Select where you want the rendered images as "Output Path"
5. Press "Execute Batch Render"

<img width="300" alt="bar" src="https://user-images.githubusercontent.com/36818485/127747435-ffde6756-e6f5-433d-b4c9-2ea353f1f376.PNG">


## Customization

### Custom import file-types
This add-on by default only supports the default Blender imports, but you can easily add custom ones this way:

1. Open BAR.py, and paste this into the elif chain in the ```import_file() ``` function:

```py
elif f.endswith("[YOUR FILE EXTENSION]"):
    try:
        bpy.ops.[BLENDER COMMAND FOR IMPORT](filepath = filepath)
        return 0
    except:
        print("could not open, continuing")
```

- Tip: to find the blender command for the custom import, go to Blender Preferences -> interface -> Enable Python tooltips. Now you should see the python command when hovering over the import option in Blender.  
