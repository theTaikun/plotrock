import bpy

type_property= bpy.props.EnumProperty(
        name="Type",
        description="PlotRock Component Type",
        default = "NONE",
        items=(
            ("plot", "Plot", "", 1),
            ("test_prop", "Test Property", "", 2),
            ("NONE", "None", "", 3)
        )
    )

csv_file = bpy.props.PointerProperty(type=bpy.types.Text)

def register():
    bpy.types.Curve.plotrock_type = type_property
    bpy.types.Curve.plotrock_csv = csv_file

def unregister():
    del bpy.types.Curve.plotrock_type
    del bpy.types.Curve.plotrock_csv
