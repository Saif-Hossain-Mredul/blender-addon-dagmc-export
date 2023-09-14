import bpy

# Define the Panel class
class CustomPropertiesPanel(bpy.types.Panel):
    bl_label = "Mesh ID"
    bl_idname = "PT_CustomProperties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mesh Properties'
    
    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Create a text field for entering the integer ID
        layout.prop(obj, "id")

# Define a custom property for the integer ID
bpy.types.Object.id = bpy.props.IntProperty(
    name="Mesh ID",
    description="Enter an integer ID",
    default=0,
    min=0  # You can set a minimum value if needed
)

# Register the panel and custom property
def register():
    bpy.utils.register_class(CustomPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(CustomPropertiesPanel)

# This allows you to run the script directly from the text editor
if __name__ == "__main__":
    register()
