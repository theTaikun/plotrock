import bpy

type_property= bpy.props.EnumProperty(
        name="Type",
        # Warnings meant for end user, not to alter within UI
        description="PlotRock Component Type (DO NOT CHANGE)",
        default = "NONE",
        items=(
            ("plot", "Plot", "DO NOT CHANGE", 1),
            ("ROOT", "Root", "DO NOT CHANGE", 2),
            ("NONE", "None", "DO NOT CHANGE", 3)
        )
    )

class RootSettings(bpy.types.PropertyGroup):
        min_x: bpy.props.FloatProperty()
        min_y: bpy.props.FloatProperty()
        max_x: bpy.props.FloatProperty()
        max_y: bpy.props.FloatProperty()
        x_axis_label: bpy.props.PointerProperty(type=bpy.types.Object)
        y_axis_label: bpy.props.PointerProperty(type=bpy.types.Object)

csv_file = bpy.props.PointerProperty(type=bpy.types.Text)

def register():
    bpy.utils.register_class(RootSettings)

    bpy.types.Curve.plotrock_type = type_property
    bpy.types.Object.plotrock_type = type_property
    bpy.types.Curve.plotrock_csv = csv_file
    bpy.types.Object.plotrock_settings = bpy.props.PointerProperty(type=RootSettings)

def unregister():
    del bpy.types.Curve.plotrock_type
    del bpy.types.Object.plotrock_type
    del bpy.types.Curve.plotrock_csv
    del bpy.types.Object.plotrock_settings

    bpy.utils.unregister_class(RootSettings)
