bl_info = {
    "name": "PlotRock",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

class PlotRock(bpy.types.Operator):
    bl_idname = "object.plotrock"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    def execute(self, context):        # execute() is called when running the operator.
        return {'FINISHED'}



def register():
    bpy.utils.register_class(PlotRock)
    print("Hello World")
def unregister():
    bpy.utils.unregister_class(PlotRock)
    print("Goodbye World")

if __name__ == "__main__":
    register()
