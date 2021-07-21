import bpy

class PlotRock(bpy.types.Operator):
    bl_idname = "object.plotrock"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        #self.report({"ERROR"}, "error mes")
        #self.report({"INFO"}, "info mes")
        self.convertData()
        self.create_curve(self.pos_list)

        return {'FINISHED'}

    def create_curve(self, coords_list):
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '2D'
        spline = crv.splines.new(type='POLY')
        spline.points.add(len(coords_list) -1 ) 
        for i, val in enumerate(coords_list):
            spline.points[i].co= (val + [2.0] + [1.0])
        obj = bpy.data.objects.new('object_name', crv)
        bpy.data.scenes[0].collection.objects.link(obj)

    def convertData(self):
        from io import StringIO
        import csv
        raw_data = bpy.data.texts[0].as_string()
        reader = csv.reader(StringIO(raw_data)) # read csv string as csv file
        string_list = list(reader)
        self.pos_list = [list(map(float, x)) for x in string_list] # convert list of strings to list of floats



def register():
    bpy.utils.register_class(PlotRock)
    print("Hello World")

def unregister():
    bpy.utils.unregister_class(PlotRock)
    print("Goodbye World")


if __name__ == "__main__":
    register()
