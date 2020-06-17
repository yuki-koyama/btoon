import bpy

bl_info = {
    "name": "BToon",
    "author": "Yuki Koyama",
    "version": (0, 0),
    "blender": (2, 83, 0),
    "location": "Shader Editor, Compositor, Texture Node Editor > Node",
    "description": "Toon shading",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "https://github.com/yuki-koyama/btoon",
    "tracker_url": "https://github.com/yuki-koyama/btoon/issues",
    "category": "Node"
}


# ------------------------------------------------------------------------------
# Copied from blender-cli-rendering:
# https://github.com/yuki-koyama/blender-cli-rendering
# ------------------------------------------------------------------------------
# https://docs.blender.org/api/current/bpy.types.SolidifyModifier.html
def add_solidify_modifier(mesh_object: bpy.types.Object,
                          thickness: float = 0.01,
                          flip_normal: bool = False,
                          fill_rim: bool = True,
                          material_index_offset: int = 0,
                          shell_vertex_group: str = "",
                          rim_vertex_group: str = "") -> None:

    modifier: bpy.types.SolidifyModifier = mesh_object.modifiers.new(name="Solidify", type='SOLIDIFY')

    modifier.material_offset = material_index_offset
    modifier.thickness = thickness
    modifier.use_flip_normals = flip_normal
    modifier.use_rim = fill_rim

    # TODO: Check whether shell_vertex_group is either empty or defined
    # TODO: Check whether rim_vertex_group is either empty or defined

    modifier.shell_vertex_group = shell_vertex_group
    modifier.rim_vertex_group = rim_vertex_group
# ------------------------------------------------------------------------------


class BTOON_OP_SetContour(bpy.types.Operator):

    bl_idname = "node.set_contour"
    bl_label = "TODO"
    bl_description = "TODO"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):

        add_solidify_modifier(bpy.context.object, -0.01, True, False, 1, "Contour", "")

        self.report({'INFO'}, "Set contour.")
        return {'FINISHED'}


def menu_func(self, context: bpy.types.Context) -> None:
    self.layout.separator()
    self.layout.operator(BTOON_OP_SetContour.bl_idname)


classes = [
    BTOON_OP_SetContour,
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
