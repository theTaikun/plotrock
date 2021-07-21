import bpy


def read_some_data(context, filepath, use_some_setting):
    print("running read_some_data...")
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()

    # would normally load the data here
    print(data)

    # Load csv into internal memory
    # shows up in text editor
    csv_mem = bpy.data.texts.new("imported_csv")
    csv_mem.write(data)

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "plotrock.import_csv"  # important since its how bpy.ops.plotrock.import_csv is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv;*.txt",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Has Headers",
        description="Select this option if first row is a header.",
        default=True,
    )

    type: EnumProperty(
        name="Deliminator",
        description="Choose deliminator used in file (typically a comma)",
        items=(
            ('OPT_A', ", Comma", "Items seperated by comma"),
            ('OPT_B', "; Semicolon", "Items seperated by semicolon"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return read_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="Import CSV for plotting (.csv, .txt)")


def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.plotrock.import_csv('INVOKE_DEFAULT')
