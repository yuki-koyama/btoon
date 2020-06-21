import bpy
import os
from typing import Tuple


bl_info = {
    "name": "BToon",
    "author": "Yuki Koyama",
    "version": (0, 0),
    "blender": (2, 83, 0),
    "location": "TODO",
    "description": "Toon shading utilities",
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


def add_displace_modifier(mesh_object: bpy.types.Object,
                          texture_name: str,
                          vertex_group: str = "",
                          mid_level: float = 0.5,
                          strength: float = 1.0) -> None:
    '''
    https://docs.blender.org/api/current/bpy.types.DisplaceModifier.html
    '''

    modifier = mesh_object.modifiers.new(name="Displace", type='DISPLACE')

    modifier.mid_level = mid_level
    modifier.strength = strength

    # TODO: Check whether texture_name is properly defined
    modifier.texture = bpy.data.textures[texture_name]

    # TODO: Check whether vertex_group is either empty or defined
    modifier.vertex_group = vertex_group


# https://docs.blender.org/api/current/bpy.types.VertexGroups.html
# https://docs.blender.org/api/current/bpy.types.VertexGroup.html
def add_vertex_group(mesh_object: bpy.types.Object, name: str = "Group") -> bpy.types.VertexGroup:

    # TODO: Check whether the object has a mesh data
    # TODO: Check whether the object already has a vertex group with the specified name

    vertex_group = mesh_object.vertex_groups.new(name=name)

    return vertex_group


def build_emission_nodes(node_tree: bpy.types.NodeTree,
                         color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                         strength: float = 1.0) -> None:
    '''
    https://docs.blender.org/api/current/bpy.types.ShaderNodeEmission.html
    '''
    output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    emission_node = node_tree.nodes.new(type='ShaderNodeEmission')

    output_node.location[0] += 100.0
    emission_node.location[0] -= 100.0

    emission_node.inputs["Color"].default_value = color + (1.0, )
    emission_node.inputs["Strength"].default_value = strength

    node_tree.links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])


def add_clouds_texture(name: str = "Clouds Texture",
                       size: float = 0.25,
                       depth: int = 2,
                       nabla: float = 0.025,
                       brightness: float = 1.0,
                       contrast: float = 1.0) -> bpy.types.CloudsTexture:
    '''
    https://docs.blender.org/api/current/bpy.types.BlendDataTextures.html
    https://docs.blender.org/api/current/bpy.types.Texture.html
    https://docs.blender.org/api/current/bpy.types.CloudsTexture.html
    '''

    # TODO: Check whether the name is already used or not

    tex = bpy.data.textures.new(name, type='CLOUDS')

    tex.noise_scale = size
    tex.noise_depth = depth
    tex.nabla = nabla

    tex.intensity = brightness
    tex.contrast = contrast

    return tex


def append_material(blend_file_path: str, material_name: str) -> bool:
    '''
    https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
    '''

    # Load the library file
    with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
        # Check whether the specified material exists in the blend file
        if material_name in data_from.materials:
            # Append the material and return True
            data_to.materials = [material_name]
            return True
        else:
            # If the material is not found, return False without doing anything
            return False

    # TODO: Handle the exception of not being able to load the library file
    # TODO: Remove the linked library from byp.data.libraries
# ------------------------------------------------------------------------------


class BTOON_OP_set_contours(bpy.types.Operator):

    bl_idname = "btoon.set_contours"
    bl_label = "Set Contours"
    bl_description = "Set contours to the selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):

        contour_group_name = "BToon Contour"
        contour_noise_name = "BToon Contour Displace Noise"
        mat_name = "BToon Contour"

        if not context.selected_objects:
            self.report({'WARNING'}, "BToon: No objects are selected.")

            return {'FINISHED'}

        if mat_name in bpy.data.materials:
            self.report({'INFO'}, "BToon: The material append process is skipped since {} already exists.".format(mat_name))
        else:
            blend_file_path = os.path.dirname(os.path.abspath(__file__)) + "/library.blend"
            append_material(blend_file_path, mat_name)

            assert mat_name in bpy.data.materials

            self.report({'INFO'}, "BToon: A material named {} is appended.".format(mat_name))

        mat = bpy.data.materials[mat_name]

        if not contour_noise_name in bpy.data.textures:
            add_clouds_texture(contour_noise_name, brightness=0.5)

        for object in context.selected_objects:
            add_vertex_group(object, contour_group_name)
            add_solidify_modifier(object, -0.01, True, False, 1, shell_vertex_group=contour_group_name)
            add_displace_modifier(object, texture_name=contour_noise_name, vertex_group=contour_group_name, mid_level=0.0, strength=-0.05)

            object.data.materials.append(mat)

            self.report({'INFO'}, "BToon: The contour for {} is set.".format(object.name))

        return {'FINISHED'}


class BTOON_OP_append_skin_material(bpy.types.Operator):

    bl_idname = "btoon.append_skin_material"
    bl_label = "Append Skin Material"
    bl_description = "Append the skin material to the selected objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):

        mat_name = "BToon Skin"

        if not context.selected_objects:
            self.report({'WARNING'}, "BToon: No objects are selected.")

            return {'FINISHED'}

        if mat_name in bpy.data.materials:
            self.report({'INFO'}, "BToon: The material append process is skipped since {} already exists.".format(mat_name))
        else:
            blend_file_path = os.path.dirname(os.path.abspath(__file__)) + "/library.blend"
            append_material(blend_file_path, mat_name)

            assert mat_name in bpy.data.materials

            self.report({'INFO'}, "BToon: A material named {} is appended.".format(mat_name))

        mat = bpy.data.materials[mat_name]

        for object in context.selected_objects:
            object.data.materials.append(mat)

            self.report({'INFO'}, "BToon: The skin material is appended to {}.".format(object.name))

        return {'FINISHED'}


op_classes = [
    BTOON_OP_set_contours,
    BTOON_OP_append_skin_material,
]


class BTOON_MT_show_menu(bpy.types.Menu):
    bl_idname = "BTOON_MT_show_menu"
    bl_label = "BToon Utilities"
    bl_description = "Toon shading utilities"

    def draw(self, context: bpy.types.Context) -> None:
        for op_class in op_classes:
            self.layout.operator(op_class.bl_idname)


def menu_func(self, context: bpy.types.Context) -> None:
    self.layout.separator()
    self.layout.menu(BTOON_MT_show_menu.bl_idname)


def register():
    bpy.utils.register_class(BTOON_MT_show_menu)
    for op_class in op_classes:
        bpy.utils.register_class(op_class)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(BTOON_MT_show_menu)
    for op_class in op_classes:
        bpy.utils.unregister_class(op_class)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
