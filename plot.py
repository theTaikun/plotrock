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

# findRoot function courtesy of MMDTools addon
def findRoot(obj):
    if obj:
        if obj.plotrock_type == 'ROOT':
            return obj
        return findRoot(obj.parent)
    return None


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

        # Size of Empty same for all axis => set as max of x and y value
        max_x = max(coords_list)[0] # Max of nested list checks first val
        max_y = max(coords_list, key=lambda x: x[1])[1] # Funct to check max by second val, and return that val
        self.root.empty_display_size = max(max_x, max_y) # compares the 2 maxes

        self.root.plotrock_settings.max_x = max_x
        self.root.plotrock_settings.max_y = max_y
        self.crv.plotrock_csv = self.csv_textdata

    def create_obj(self):
        print("create new obj")

        self.root = bpy.data.objects.new("rockplot_root", None)
        self.root.empty_display_type = "ARROWS"
        self.root.plotrock_type = "ROOT"
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
        self.grid = self.create_grid()
        self.grid.parent = self.root
        bpy.data.scenes[0].collection.objects.link(self.grid)


    def create_grid(self):
        gridGeo = bpy.data.node_groups.new("gridNodeTree", "GeometryNodeTree")
        gridMesh = bpy.data.meshes.new("gridMesh")
        gridObj = bpy.data.objects.new("gridObj", gridMesh )
        geoModifier = gridObj.modifiers.new("gridGeoNodes", "NODES")
        geoModifier.node_group = gridGeo
        wireModifier = gridObj.modifiers.new("gridWire", "WIREFRAME")
        wireModifier.thickness = 0.125

        nodes = gridGeo.nodes

        gridGeo.inputs.new("NodeSocketGeometry", "Geometry")
        gridGeo.outputs.new("NodeSocketGeometry", "Geometry")
        input_node = nodes.new("NodeGroupInput")
        input_node.location.x = -300 - input_node.width
        output_node = nodes.new("NodeGroupOutput")
        output_node.is_active_output = True
        output_node.location.x = 200


        gridGeo.inputs.new("NodeSocketVector", "Size")
        gridGeo.inputs[1].default_value=[10,10,0]

        node = nodes.new("GeometryNodeMeshGrid")
        node.location.x = -200 - node.width
        node.name = "MESH_GRID"

        node = nodes.new("GeometryNodeTransform")
        node.name = "XLATE_XFORM"

        node = nodes.new("ShaderNodeVectorMath")
        node.name = "DIV_BY_TWO"
        node.location.x = -50 - node.width
        node.location.y = -100
        node.operation = "DIVIDE"
        node.inputs[1].default_value=[2,2,1]

        node = nodes.new("ShaderNodeVectorMath")
        node.name = "ADD_GRID_LINE"
        node.location.x = -75 - node.width
        node.location.y = -200
        node.operation = "ADD"
        node.inputs[1].default_value=[1,1,0]

        node = nodes.new("ShaderNodeSeparateXYZ")
        node.name = "SepXYZ_size"

        node = nodes.new("ShaderNodeSeparateXYZ")
        node.name = "SepXYZ_verts"

        gridGeo.links.new(output_node.inputs[0], nodes["XLATE_XFORM"].outputs[0])
        gridGeo.links.new(nodes["XLATE_XFORM"].inputs["Geometry"], nodes["MESH_GRID"].outputs[0])
        gridGeo.links.new(nodes["XLATE_XFORM"].inputs[1], nodes["DIV_BY_TWO"].outputs[0])
        gridGeo.links.new(nodes["SepXYZ_size"].inputs[0], input_node.outputs[1])
        gridGeo.links.new(nodes["DIV_BY_TWO"].inputs[0], input_node.outputs[1])
        gridGeo.links.new(nodes["ADD_GRID_LINE"].inputs[0], input_node.outputs[1])
        gridGeo.links.new(nodes["MESH_GRID"].inputs[0], nodes["SepXYZ_size"].outputs[0])
        gridGeo.links.new(nodes["MESH_GRID"].inputs[1], nodes["SepXYZ_size"].outputs[1])

        gridGeo.links.new(nodes["MESH_GRID"].inputs[2], nodes["SepXYZ_verts"].outputs[0])
        gridGeo.links.new(nodes["MESH_GRID"].inputs[3], nodes["SepXYZ_verts"].outputs[1])

        gridGeo.links.new(nodes["SepXYZ_verts"].inputs[0], nodes["ADD_GRID_LINE"].outputs[0])
        gridGeo.links.new(nodes["ADD_GRID_LINE"].inputs[0], input_node.outputs[1])

        return gridObj


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

    def update_axis(self):
        coords_list = self.pos_list
        # Size of Empty same for all axis => set as max of x and y value
        max_x = max(coords_list)[0] # Max of nested list checks first val
        max_y = max(coords_list, key=lambda x: x[1])[1] # Funct to check max by second val, and return that val
        self.root.empty_display_size = max(max_x, max_y) # compares the 2 maxes

        self.root.plotrock_settings.max_x = max_x
        self.root.plotrock_settings.max_y = max_y

    def execute(self, context):
        print("updating")
        self.obj = context.active_object
        self.crv = self.obj.data
        self.spline = self.crv.splines[0]
        self.csv_textdata = self.crv.plotrock_csv
        self.delimiter = self.csv_textdata['delimiter']
        self.has_headers = self.csv_textdata['has_headers']
        self.root = findRoot(self.obj)

        self.pos_list, self.headers = convertData(self.csv_textdata, self.delimiter, self.has_headers)

        self.update_curve()
        self.update_axis()
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
