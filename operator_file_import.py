import bpy


def read_some_data(context, filepath, use_some_setting):
    # Everything below up to print statement only needed for debugging
    # TODO: Remove in production
    print("running read_some_data...")
    f = open(filepath, 'r', encoding='utf-8')
    data = f.read()
    f.close()

    # would normally load the data here
    print(data)

    # Load csv into internal memory
    # shows up in text editor
    # TODO: Decide if I truly want data to be internal
    csv_mem = bpy.data.texts.load(filepath, internal=True)

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from . import plot


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
    has_headers: BoolProperty(
        name="Has Headers",
        description="Select this option if first row is a header.",
        default=True,
    )

    deliminator: EnumProperty(
        name="Deliminator",
        description="Choose deliminator used in file (typically a comma)",
        items=(
            ("comma", ", Comma", "Items seperated by comma"),
            ("semi", "; Semicolon", "Items seperated by semicolon"),
            ("NONE", "None", "None"),
        ),
        default="comma",
    )

    def execute(self, context):
        self.csv_textdata = bpy.data.texts.load(self.filepath, internal=True)

        new_plot = plot.NewPlot
        new_plot().execute(
                context = context,
                csv_textdata = self.csv_textdata,
                filepath = self.filepath,
                has_headers = self.has_headers,
                deliminator = self.deliminator
                )
        #return read_some_data(context, self.filepath, self.use_setting)
        return {"FINISHED"}


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
