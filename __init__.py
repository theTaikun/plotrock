bl_info = {
    "name": "PlotRock",
    "description": "Create 3D plots from CSV data",
    "author": "Isaac Phillips (theTaikun)",
    "version": (1,0,0),
    "version_code": 4, # not used by blender, but keeping track here
    "blender": (2, 92, 0),
    "location": "File > Import > Import CSV for plotting",
    "tracker_url": "https://github.com/theTaikun/plotrock/issues/new",
    "category": "Object",
}

modulesNames = ['plot', 'operator_file_import', 'ui_panel', 'properties']


import sys
import importlib

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
        if currentModuleFullName in sys.modules:
            importlib.reload(sys.modules[currentModuleFullName])
        else:
            globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
            setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
