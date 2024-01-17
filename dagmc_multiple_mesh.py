import bpy
import subprocess
import platform
import os
import time
import sys
from bpy.props import *


class ExportToH5DOperator(bpy.types.Operator):
    bl_idname = "export.stl_to_h5m"
    bl_label = "Export to H5M"
    bl_description = "Export the selected object as DAGMC(.h5m)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            # Check if the stl-to-h5m package is installed
            package_installed = self.check_package_installed()

            if not package_installed:
                self.report({'INFO'}, "Installing package...")
                self.install_package()

            # Get the currently active scene
            scene = bpy.context.scene

            selected_meshes = []

            for obj in scene.objects:
                if obj.type == 'MESH' and obj.select_get():
                    selected_meshes.append(obj)

            stl_mesh_tuples = []
            base_path = bpy.data.filepath.rsplit("/", 1)[0]
            h5m_filepath = bpy.data.filepath.split(".")[0] + ".h5m"

            for obj in selected_meshes:
                stl_file_path = base_path + "/" + obj.name + ".stl"

                bpy.ops.export_mesh.stl(
                    filepath=stl_file_path, check_existing=False, use_selection=True)

                stl_mesh_tuples.append((stl_file_path, obj.name))

            self.report({'INFO'}, "Converting MESH to H5M...")
            self.report({'INFO'}, "Running conversion")
            self.run_conversion(stl_mesh_tuples, h5m_filepath)

            self.delete_stl_files(directory=base_path)

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
            subprocess.call(
                [python_exe, "-m", "pip", "install", "--upgrade", "pip"])

            # install required packages
            subprocess.call([python_exe, "-m", "pip", "install", "stl-to-h5m"])
            self.report({'INFO'}, "Package successfully installed")
        elif os_name == "Linux":
            # Windows command to install the package
            python_exe = os.path.join(sys.prefix, 'bin', 'python3.10')
            # upgrade pip
            subprocess.call([python_exe, "-m", "ensurepip"])
            subprocess.call(
                [python_exe, "-m", "pip", "install", "--upgrade", "pip"])

            # install required packages
            subprocess.call([python_exe, "-m", "pip", "install", "stl-to-h5m"])
            self.report({'INFO'}, "Package successfully installed")
        else:
            self.report({'ERROR'}, f"Unsupported operating system: {os_name}")

    def run_conversion(self, stl_file_touples, h5m_filepath):
        if self.check_package_installed():
            from stl_to_h5m import stl_to_h5m
            self.report({'INFO'}, "Module found")

            stl_to_h5m(
                files_with_tags=stl_file_touples,
                h5m_filename=h5m_filepath,
            )
            self.report({'INFO'}, "Conversion successful")
        else:
            raise Exception("Module not found.")

    def delete_stl_files(self, directory):
        file_list = os.listdir(directory)

        # Iterate through the files and delete STL files
        for file in file_list:
            if file.endswith(".stl"):
                file_path = os.path.join(directory, file)
                os.remove(file_path)


def menu_func_export(self, context):
    self.layout.operator(ExportToH5DOperator.bl_idname, text="DAGMC (.h5m)")


def register():
    bpy.utils.register_class(ExportToH5DOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportToH5DOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
