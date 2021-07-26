import bpy

# TODO: check if new data same as old,
#       if so, don't go through update process

class Plot:
    """"
    bl_idname = "plotrock.plot"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    """

    obj = None
    crv = None
    spline = None
    has_header = False
    deliminator = None

    def execute(self, **args):        # execute() is called when running the operator.
        #self.report({"ERROR"}, "error mes")
        #self.report({"INFO"}, "info mes")
        print("plotting")
        self.csv_data = args.get("csv_data")
        self.filepath= args.get("filepath")
        self.has_headers = args.get("has_headers")
        self.deliminator = args.get("deliminator")
        self.convertData()
        if self.obj is None:
            print("no class obj")
            self.create_obj()
            self.create_curve(self.pos_list)
        else:
            print("class obj found: {}".format(self.obj))
            self.update_curve()

        return {'FINISHED'}

    def create_curve(self, coords_list):
        print("create curve")
        spline = self.spline
        spline.points.add(len(coords_list) -1 )
        for i, val in enumerate(coords_list):
            spline.points[i].co = (val + [2.0] + [1.0])
        self.crv.plotrock_csv = self.csv_data

    def convertData(self):
        from io import StringIO
        import csv
        print("converting data")
        raw_data = self.csv_data.as_string()
        reader = csv.reader(StringIO(raw_data)) # read csv string as csv file
        string_list = list(reader)
        self.pos_list = [list(map(float, x)) for x in string_list] # convert list of strings to list of floats

    def create_obj(self):
        print("create new obj")
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '2D'
        crv.plotrock_type="plot"
        spline = crv.splines.new(type='POLY')
        self.crv = crv
        self.spline = spline
        self.obj = bpy.data.objects.new('object_name', crv)
        bpy.data.scenes[0].collection.objects.link(self.obj)

class updatePlot(bpy.types.Operator):
    bl_idname = "plotrock.update_plot"
    bl_label = "Update Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        # Need to check not None otherwise selecting nothing will result in True
        return obj is not None and obj.type == "CURVE" and obj.data.plotrock_type == "plot"

    def update_curve(self):
        print("updating curve")
        # num point length is diff than current spline
        if len(self.spline.points) != len(self.pos_list):
            print("point length diff")
            self.crv.splines.remove(self.spline)
            new_spline = self.crv.splines.new(type='POLY')
            new_spline.points.add(len(self.pos_list) -1 ) 
            self.spline = new_spline
        else:
            print("point length same")
        spline = self.spline
        for i, val in enumerate(self.pos_list):
            print("updating point {}".format(i))
            spline.points[i].co= (val + [2.0] + [1.0])

    def execute(self, context):
        import csv
        from io import StringIO
        print("updating")
        self.obj = context.active_object
        self.crv = self.obj.data
        self.spline = self.crv.splines[0]
        self.csv_data = self.crv.plotrock_csv

        raw_data = self.csv_data.as_string()
        reader = csv.reader(StringIO(raw_data)) # read csv string as csv file
        string_list = list(reader)

        self.pos_list = [list(map(float, x)) for x in string_list] # convert list of strings to list of floats

        self.update_curve()
        return {"FINISHED"}





def register():
    #bpy.utils.register_class(Plot)
    bpy.utils.register_class(updatePlot)
    print("Hello World")

def unregister():
    #bpy.utils.unregister_class(Plot)
    bpy.utils.unregister_class(updatePlot)
    print("Goodbye World")


if __name__ == "__main__":
    register()
