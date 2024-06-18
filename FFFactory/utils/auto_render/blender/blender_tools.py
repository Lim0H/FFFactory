from tempfile import TemporaryDirectory

from FFFactory.utils.systems_util import ExistsDirType, ExistsFileType


from contextlib import contextmanager
from math import radians
from typing import Generator, Tuple
import bpy
import os
from ..render_types import DctModelRenderConfig
from .consts import MODEL_NAME, MATERIAL_NAME, TEMP_FILE_NAME, CAMERA_NAME, TEMP_COLLECTION_NAME, DOT_BLEND


class BlenderModelHandler:
    def __init__(self, source_file: str, temp_file: str):
        self.source_file: str = source_file
        self.temp_file: str = temp_file
        self._save_source_model()

    def open_file(self, filepath: str) -> None:
        bpy.ops.wm.open_mainfile(filepath=filepath)

    def save_temp_file(self) -> None:
        bpy.ops.wm.save_as_mainfile(filepath=self.temp_file)

    def load_data_from_temp_file(self) -> None:
        with bpy.data.libraries.load(self.temp_file) as (data_from, data_to):
            if MODEL_NAME in data_from.objects:
                data_to.objects = [MODEL_NAME]
            if MATERIAL_NAME in data_from.materials:
                data_to.materials = [MATERIAL_NAME]

    def link_model_to_scene(self) -> bpy.types.Object:
        imported_model = bpy.data.objects[MODEL_NAME]
        bpy.context.scene.collection.objects.link(imported_model)
        return imported_model

    def apply_material_to_model(self, model: bpy.types.Object) -> None:
        if MATERIAL_NAME in bpy.data.materials:
            material = bpy.data.materials[MATERIAL_NAME]
            if model.data.materials:
                model.data.materials[0] = material
            else:
                model.data.materials.append(material)

    def save_file(self, filepath: str) -> None:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)

    def rotate_model(self, model: bpy.types.Object, rotation: Tuple[float, float, float]) -> None:
        model.rotation_euler = tuple(radians(angle) for angle in rotation)

    def _save_source_model(self) -> None:
        self.open_file(self.source_file)
        model = bpy.data.objects[MODEL_NAME]
        new_collection = bpy.data.collections.new(TEMP_COLLECTION_NAME)
        bpy.context.scene.collection.children.link(new_collection)
        new_collection.objects.link(model)
        self.save_temp_file()

    def set_camera(self, obj: bpy.types.Object) -> None:
        if CAMERA_NAME not in bpy.data.objects:
            bpy.ops.object.camera_add()

        camera = bpy.data.objects[CAMERA_NAME]
        bpy.context.scene.camera = camera
        camera.location = (0, -3, 2)
        camera.rotation_euler = (radians(80), 0, 0)
        bpy.context.view_layer.update()

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = camera
        bpy.ops.view3d.camera_to_view_selected()
        bpy.context.view_layer.update()

    def render_image(self, output_path: str):
        bpy.context.scene.render.filepath = output_path
        bpy.ops.render.render(write_still=True)


@contextmanager
def blender_context(source_file: ExistsFileType) -> Generator[BlenderModelHandler, None, None]:
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, TEMP_FILE_NAME)
        yield BlenderModelHandler(source_file.value, temp_file)


class RenderTemplate:
    def __init__(
        self,
        template_path: ExistsFileType,
        template_name: str,
        type: str
    ) -> None:
        self._template_path = template_path
        self._template_name = template_name
        self._type = type

    @property
    def type(self) -> str:
        return self._type

    @property
    def template_name(self) -> str:
        return self._template_name

    @property
    def template_path(self) -> str:
        return self._template_path.value

    def render_image(self, config: DctModelRenderConfig) -> None:
        file_name = os.path.basename(config['file_name']).removesuffix(DOT_BLEND)
        with blender_context(config['file_path']) as handler:
            handler.open_file(self.template_path)
            handler.load_data_from_temp_file()

            imported_model = handler.link_model_to_scene()
            handler.apply_material_to_model(imported_model)
            for i, angle in enumerate(range(-1, config['max_rotation_z'], config['angle_rotation_z']), 1):
                handler.rotate_model(imported_model, (0, 0, angle))
                handler.set_camera(imported_model)
                bpy.ops.outliner.orphans_purge()

                if i not in config['number_imgs']:
                    continue

                project_file_name = '_'.join((
                    file_name, str(angle), self.template_name
                )) + DOT_BLEND
                exists_project = os.path.exists(project_file_name)
                if (
                    config['save_project'] is True and
                    (
                        exists_project is False or
                        config['always_rerender'] is True
                    )
                ):
                    handler.save_file(os.path.join(
                        config['output_dir'].value,
                        project_file_name
                    ))

                image_file_name = '_'.join((
                    config['image_name'], self.template_name
                )) + '.' + config['save_as']
                exists_image = os.path.exists(image_file_name)
                if (
                    exists_image is False or
                    config['always_rerender'] is True
                ):
                    handler.render_image(os.path.join(
                        config['output_dir'].value,
                        image_file_name
                    ))


def get_render_templates(input_dir: ExistsDirType) -> list[RenderTemplate]:
    result = []
    for template_type in os.listdir(input_dir.value):
        output_dir_with_type = os.path.join(input_dir.value, template_type)
        for template_name in os.listdir(output_dir_with_type):
            result.append(RenderTemplate(
                ExistsFileType(os.path.join(output_dir_with_type, template_name)),
                template_name,
                template_type
            ))
    return result


__all__ = [
    'DctModelRenderConfig',
    'RenderTemplate',
]
