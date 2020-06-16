# Remove an existing zip file if any
rm -f btoon.zip

# Create a package
zip -o btoon.zip -r btoon

# Install the package to the blender
blender --background --python-expr "import bpy; bpy.ops.preferences.addon_install(overwrite=True, filepath=\"./btoon.zip\")"
