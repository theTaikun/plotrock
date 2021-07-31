import bpy

# TODO: check if new data same as old,
#       if so, don't go through update process

def convertData(csv_textdata, entry_delimiter=",", has_headers=True):
    from io import StringIO
    import csv
    print("converting data")
    raw_data = csv_textdata.as_string()
    reader = csv.reader(StringIO(raw_data), delimiter=entry_delimiter) # read csv string as csv file
    if(has_headers):
        headers = next(reader)
        print("headers: {}".format(headers))
    else:
        headers = None
    string_list = list(reader)
    pos_list = [list(map(float, x)) for x in string_list] # convert list of strings to list of floats
    return pos_list, headers


class NewPlot:
    """"
    bl_idname = "plotrock.plot"
    bl_label = "Create Simple Plot"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    """

    obj = None
    crv = None
    spline = None
    has_header = False
    delimiter = None

    def execute(self, **args):        # execute() is called when running the operator.
        #self.report({"ERROR"}, "error mes")
        #self.report({"INFO"}, "info mes")
        print("plotting")
        self.csv_textdata = args.get("csv_textdata")
        self.filepath= args.get("filepath")
        self.has_headers = args.get("has_headers")
        #self.delimiter = args.get("delimiter")
        self.pos_list, self.headers = convertData(self.csv_textdata, self.csv_textdata['delimiter'], self.has_headers)


        if self.obj is None:
            print("no class obj")
            self.create_obj()
            if(self.has_headers):
                print("x-axis: {}, y-axis: {}".format(self.headers[0], self.headers[1]))
                self.create_axis_text()
            self.create_curve(self.pos_list)
        else:
            print("class obj found: {}".format(self.obj))
            self.update_curve()

        return {'FINISHED'}

    def create_axis_text(self):
        xaxis_crv = bpy.data.curves.new(type="FONT",name="xAxisCrv")
        xaxis_crv.offset_x = 2
        xaxis_crv.offset_y = -1
        xaxis_obj = bpy.data.objects.new("xAxisObj", xaxis_crv)
        xaxis_obj.data.body = self.headers[0]
        xaxis_obj.parent = self.root
        bpy.data.scenes[0].collection.objects.link(xaxis_obj)

        yaxis_crv = bpy.data.curves.new(type="FONT",name="yAxisCrv")
        yaxis_crv.offset_x = -2
        yaxis_crv.offset_y = 2
        yaxis_obj = bpy.data.objects.new("yAxisObj", yaxis_crv)
        yaxis_obj.data.body = self.headers[1]
        yaxis_obj.parent = self.root
        bpy.data.scenes[0].collection.objects.link(yaxis_obj)

    def create_curve(self, coords_list):
        print("create curve")
        spline = self.spline
        spline.points.add(len(coords_list) -1 )
        for i, val in enumerate(coords_list):
            spline.points[i].co = (val + [2.0] + [1.0])
        self.crv.plotrock_csv = self.csv_textdata

    def create_obj(self):
        print("create new obj")

        self.root = bpy.data.objects.new("rockplot_root", None)
        self.root.empty_display_type = "ARROWS"
        crv = bpy.data.curves.new('crv', 'CURVE')
        crv.dimensions = '2D'
        crv.plotrock_type="plot"
        spline = crv.splines.new(type='POLY')
        self.crv = crv
        self.spline = spline
        self.obj = bpy.data.objects.new('object_name', crv)
        self.obj.parent = self.root
        bpy.data.scenes[0].collection.objects.link(self.obj)
        bpy.data.scenes[0].collection.objects.link(self.root)

class UpdatePlot(bpy.types.Operator):
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
        print("updating")
        self.obj = context.active_object
        self.crv = self.obj.data
        self.spline = self.crv.splines[0]
        self.csv_textdata = self.crv.plotrock_csv
        self.delimiter = self.csv_textdata['delimiter']
        self.has_headers = self.csv_textdata['has_headers']

        self.pos_list, self.headers = convertData(self.csv_textdata, self.delimiter, self.has_headers)

        self.update_curve()
        return {"FINISHED"}





def register():
    #bpy.utils.register_class(Plot)
    bpy.utils.register_class(UpdatePlot)
    print("Hello World")

def unregister():
    #bpy.utils.unregister_class(Plot)
    bpy.utils.unregister_class(UpdatePlot)
    print("Goodbye World")


if __name__ == "__main__":
    register()
