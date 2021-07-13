# BlenderAutoRenderer

This script lets you automatically import and render files in Blender. 
This is configured for NieR:Automata files, but can be used for all blender imports. 
Based off [this script.](https://gist.github.com/der-Daniel/cfc93a4661f47e66bfd4ebd81efbb943)

![output example](https://user-images.githubusercontent.com/36818485/123545506-a3322b00-d758-11eb-90e6-36227326429d.png)

## How to use 

**NOTE: This script is configured to work with .dtt files out of the box. How to change input filetype is outlined below!**

1. Open a terminal window, and move to the folder containing your Blender 2.8+ exe file.
    - (Optional) You can add Blender to PATH if you don't want to navigate to the Blender folder everytime
2. Use this command to batch render all files in a folder:
```
blender -P "[path to BAR.py]" "[path to folder with files to render]" "[Render output folder]"
```

NOTE: No other command will run this script. Also running blender in background mode does not work with this script.

## Customization

### Changing import file type
This script can import any blender supported format. By default it is configured to import .dtt files (NieR:Automata files).
To change this, just modify these lines in the main() method:
![Modify import type](https://user-images.githubusercontent.com/36818485/123545554-e2607c00-d758-11eb-901c-b8b6b10e6e1f.png)

### Customizing rendering
This script places four cameras around the bounding box of the imported object. 
Camera placement and ammount can be customized in the add_cameras() method.

![bilde](https://user-images.githubusercontent.com/36818485/123545662-70d4fd80-d759-11eb-8357-763721bac528.png)

### Known issues

- Flat objects with a large area are problematic with the default camera configuration.
- Really large objects and objects that are really off center from origin don't produce good results.
