# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "dagmc_export",
    "author" : "Saif Hossain",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from . import auto_load
 
auto_load.init()

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
