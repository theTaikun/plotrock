import bpy

# TODO: check if new data same as old,
#       if so, don't go through update process

class PlotRock(bpy.types.Operator):
    bl_idname = "object.plotrock"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    obj = None
    crv = None
    spline = None

    def execute(self, context):        # execute() is called when running the operator.
        #self.report({"ERROR"}, "error mes")
        #self.report({"INFO"}, "info mes")
        print("plotting")
        self.convertData()
        if PlotRock.obj is None:
            print("no class obj")
            self.create_obj()
            self.create_curve(self.pos_list)
        else:
            print("class obj found: {}".format(PlotRock.obj))
            self.update_curve()

        return {'FINISHED'}

    def create_curve(self, coords_list):
        print("create curve")
        spline = PlotRock.spline
        spline.points.add(len(coords_list) -1 ) 
        for i, val in enumerate(coords_list):
            spline.points[i].co= (val + [2.0] + [1.0])

    def convertData(self):
        from io import StringIO
        import csv
        print("converting data")
        raw_data = bpy.data.texts["imported_csv"].as_string()
        reader = csv.reader(StringIO(raw_data)) # read csv string as csv file
        string_list = list(reader)
        self.pos_list = [list(map(float, x)) for x in string_list] # convert list of strings to list of floats

    def create_obj(self):
        print("create new obj")
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '2D'
        spline = crv.splines.new(type='POLY')
        PlotRock.spline = spline
        PlotRock.crv = crv
        PlotRock.obj = bpy.data.objects.new('object_name', crv)
        bpy.data.scenes[0].collection.objects.link(PlotRock.obj)

    def update_curve(self):
        print("updating curve")
        # num point length is diff than current spline
        if len(PlotRock.spline.points) != len(self.pos_list):
            print("point length diff")
            PlotRock.crv.splines.remove(PlotRock.spline)
            new_spline = PlotRock.crv.splines.new(type='POLY')
            new_spline.points.add(len(self.pos_list) -1 ) 
            PlotRock.spline = new_spline
        else:
            print("point length same")
        spline = PlotRock.spline
        for i, val in enumerate(self.pos_list):
            print("updating point {}".format(i))
            spline.points[i].co= (val + [2.0] + [1.0])






def register():
    bpy.utils.register_class(PlotRock)
    print("Hello World")

def unregister():
    bpy.utils.unregister_class(PlotRock)
    print("Goodbye World")


if __name__ == "__main__":
    register()
