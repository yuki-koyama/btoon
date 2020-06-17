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
def clean_nodes(nodes: bpy.types.Nodes) -> None:
    for node in nodes:
        nodes.remove(node)


def add_material(name: str = "Material", use_nodes: bool = False, make_node_tree_empty: bool = False) -> bpy.types.Material:
    '''
    https://docs.blender.org/api/current/bpy.types.BlendDataMaterials.html
    https://docs.blender.org/api/current/bpy.types.Material.html
    '''

    # TODO: Check whether the name is already used or not

    material = bpy.data.materials.new(name)
    material.use_nodes = use_nodes

    if use_nodes and make_node_tree_empty:
        clean_nodes(material.node_tree.nodes)

    return material


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


# https://docs.blender.org/api/current/bpy.types.VertexGroups.html
# https://docs.blender.org/api/current/bpy.types.VertexGroup.html
def add_vertex_group(mesh_object: bpy.types.Object, name: str = "Group") -> bpy.types.VertexGroup:

    # TODO: Check whether the object has a mesh data
    # TODO: Check whether the object already has a vertex group with the specified name

    vertex_group = mesh_object.vertex_groups.new(name=name)

    return vertex_group
# ------------------------------------------------------------------------------


class BTOON_OP_SetContour(bpy.types.Operator):

    bl_idname = "node.set_contour"
    bl_label = "TODO"
    bl_description = "TODO"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):

        mat_name = "BToon Contour"
        mat = None
        if mat_name in bpy.data.materials:
            print("BToon: Skip the material creation process.")
            mat = bpy.data.materials[mat_name]
        else:
            mat = add_material(mat_name, use_nodes=True)
            mat.use_backface_culling = True
        assert mat is not None

        contour_group_name = "Contour"
        object = bpy.context.object

        add_vertex_group(object, contour_group_name)
        add_solidify_modifier(object, -0.01, True, False, 1, shell_vertex_group=contour_group_name)

        object.data.materials.append(mat)

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
