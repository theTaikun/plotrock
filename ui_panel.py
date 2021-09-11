import bpy
from . import plot # to use plot.findRoot()


class OperatorPanel(bpy.types.Panel):
    bl_label = "Operator"
    bl_idname = "OBJECT_PT_plotrock_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ""
    bl_category = "RockPlot"

    def draw(self, context):
        layout = self.layout

        """ Original Template Inputs for reference
        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("render.render")

        # Different sizes in a row
        layout.label(text="Different button sizes:")
        row = layout.row(align=True)
        row.operator("render.render")

        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("render.render")

        row.operator("render.render")
        """

        # CSV Import Button
        layout.label(text="Import/Re-import CSV")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("plotrock.import_csv")

        # Big plot button
        layout.label(text="Plot data from modified CSV")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("plotrock.update_plot")


class PlotPanel(bpy.types.Panel):
    bl_label = "Plot Settings"
    bl_idname = "OBJECT_PT_plotrock_plot"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ""
    bl_category = "RockPlot"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if(obj is not None and obj.type == "CURVE" and obj.data.plotrock_type == "plot"):
            split = layout.split()
            col=split.column()
            col.label(text="Line Shape")

            # Line Depth
            col=split.column()
            col.prop(obj.data, 'extrude', text="Depth")

            # Line Width
            col.prop(obj.data, 'bevel_depth', text='Width')

            row = layout.row()
            row.prop(obj.data.splines[0], 'use_smooth')

            row = layout.row()
            row.prop(obj, 'location', index=2, text="Z-Position")
        else:
            layout.label(text="Select a Plot")
        return

class AxisPanel(bpy.types.Panel):
    bl_label = "Axis Settings"
    bl_idname = "OBJECT_PT_plotrock_axis"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ""
    bl_category = "RockPlot"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        root = plot.findRoot(obj)

        if(obj is not None and plot.findRoot(obj)):
            #layout.label(text="Axis Label Depth")
            #row = layout.row()
            # Axis Label Depth
            split = layout.split()
            col=split.column(align=True)
            col.label(text=None)
            col.label(text="Depth")
            col.label(text="Size")
            col.label(text="Use Min")

            col=split.column(align=True)
            col.label(text="X")
            col.prop(root.plotrock_settings.x_axis_label.data, 'extrude', text="")
            col.prop(root.plotrock_settings.x_axis_label.data, 'size', text="")
            col.prop(root.plotrock_settings, 'use_min_x', text="")

            col=split.column()
            col.label(text="Y")
            col.prop(root.plotrock_settings.y_axis_label.data, 'extrude', text="")
            col.prop(root.plotrock_settings.y_axis_label.data, 'size', text="")
            col.prop(root.plotrock_settings, 'use_min_y', text="")

            split = layout.split()
            col=split.column()
            col=split.column()
            if(not root.plotrock_settings.use_min_x):
                col.enabled=False
            col.prop(root.plotrock_settings, 'min_x', text="")

            col=split.column()
            if(not root.plotrock_settings.use_min_y):
                col.enabled=False
            col.prop(root.plotrock_settings, 'min_y', text="")

        else:
            layout.label(text="Select an Axis")
        return


def register():
    bpy.utils.register_class(OperatorPanel)
    bpy.utils.register_class(PlotPanel)
    bpy.utils.register_class(AxisPanel)


def unregister():
    bpy.utils.unregister_class(OperatorPanel)
    bpy.utils.unregister_class(PlotPanel)
    bpy.utils.unregister_class(AxisPanel)


if __name__ == "__main__":
    register()
