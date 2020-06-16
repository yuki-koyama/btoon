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


class BTOON_OP_SetContour(bpy.types.Operator):

    bl_idname = "node.set_contour"
    bl_label = "TODO"
    bl_description = "TODO"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):
        self.report({'INFO'}, "TODO.")
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
