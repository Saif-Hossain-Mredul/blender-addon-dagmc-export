import bpy
import subprocess
import platform
import os
import time
import sys
from bpy.props import*


class ExportToH5DOperator(bpy.types.Operator):
    bl_idname = "export.stl_to_h5m"
    bl_label = "Export to H5M"
    bl_description = "Export the selected object as H5M"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            # Check if the stl-to-h5m package is installed
            package_installed = self.check_package_installed()

            if not package_installed:
                self.report({'INFO'}, "Installing stl-to-h5m package...")
                self.install_package()
                
            # Get the selected object
            selected_object = bpy.context.active_object

            # Ensure the selected object is in STL format
            if selected_object.type == 'MESH':
                # Construct the file paths
                base_path = bpy.data.filepath.split(".")[0]
                stl_filepath = base_path + ".stl"
                h5m_filepath =  base_path + ".h5m"

                # Export the selected object to STL format
                bpy.ops.export_mesh.stl(filepath=stl_filepath)

                # Convert the STL file to H5D using stl-to-h5m package
                self.report({'INFO'}, "Converting STL to H5M...")

                self.report({'INFO'}, "Running conversion")
                self.run_conversion(stl_filepath, h5m_filepath)
                
                # Cleanup: remove the temporary STL file
                os.remove(stl_filepath)

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")

        return {'FINISHED'}

    def check_package_installed(self):
        try:
            import stl_to_h5m
            return True
        except ImportError:
            return False

    def install_package(self):
        os_name = platform.system()

        if os_name == "Windows":
            # Windows command to install the package
            python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
            # upgrade pip
            subprocess.call([python_exe, "-m", "ensurepip"])
            subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
             
            # install required packages
            subprocess.call([python_exe, "-m", "pip", "install", "stl-to-h5m"])
            self.report({'INFO'}, "Package successfully installed")
        elif os_name == "Linux":
            # Windows command to install the package
            python_exe = os.path.join(sys.prefix, 'bin', 'python3.10')
            # upgrade pip
            subprocess.call([python_exe, "-m", "ensurepip"])
            subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
             
            # install required packages
            subprocess.call([python_exe, "-m", "pip", "install", "stl-to-h5m"])
            self.report({'INFO'}, "Package successfully installed")
        else:
            self.report({'ERROR'}, f"Unsupported operating system: {os_name}")

    def run_conversion(self, stl_filepath, h5m_filepath):
        if self.check_package_installed():
            from stl_to_h5m import stl_to_h5m
            self.report({'INFO'}, "Package successfully found")
            
            stl_to_h5m(
                files_with_tags=[(stl_filepath, 'mat1')],
                h5m_filename=h5m_filepath,
            )
            self.report({'INFO'}, "Conversion successful")
        else: 
            raise Exception("Module not found.")


def menu_func_export(self, context):
    self.layout.operator(ExportToH5DOperator.bl_idname, text="Export to .h5m")

def register():
    bpy.utils.register_class(ExportToH5DOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportToH5DOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
