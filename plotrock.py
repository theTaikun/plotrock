import bpy

num_data = [
        [0,0],
        [1,0.5],
        [2,1],
        [3,2],
        [4,4]
        ]

class PlotRock(bpy.types.Operator):
    bl_idname = "object.plotrock"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    def execute(self, context):        # execute() is called when running the operator.
       #self.report({"ERROR"}, "error mes")
        self.report({"INFO"}, "info mes")
        self.create_curve()
        return {'FINISHED'}
    def create_curve(coords_list):
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '2D'
        spline = crv.splines.new(type='POLY')
        spline.points.add(len(num_data) -1 ) 
        for i, val in enumerate(num_data):
            spline.points[i].co= (val + [2.0] + [1.0])
        obj = bpy.data.objects.new('object_name', crv)
        bpy.data.scenes[0].collection.objects.link(obj)
        return {'FINISHED'}




def register():
    bpy.utils.register_class(PlotRock)
    print("Hello World")
def unregister():
    bpy.utils.unregister_class(PlotRock)
    print("Goodbye World")

if __name__ == "__main__":
    register()
