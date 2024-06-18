import os
from typing import Optional

from FFFactory.utils.systems_util import ExistsDirType, ExistsFileType
from .render_types import ConfigImporterBase, DctModelRenderConfig


RENDER_IMAGE = 'render_image'


class BlenderConfigImporter(ConfigImporterBase):
    def _import_config(self, yaml_output: Optional[dict]) -> list[DctModelRenderConfig]:
        if yaml_output is None:
            raise ValueError('Yaml output is None')
        yaml_output: dict = yaml_output[RENDER_IMAGE]
        templates_number_img: list[dict[str, int | str]] = yaml_output.pop('templates_number_img')
        result: list[DctModelRenderConfig] = []
        for template in templates_number_img:
            for template_name, number_img in template.items():
                lst_number_img = []
                if number_img == 'all':
                    lst_number_img = list(map(
                        lambda x: x + 1,
                        range(-1, yaml_output['max_rotation_z'], yaml_output['angle_rotation_z'])
                    ))
                elif isinstance(number_img, str) and ',' in number_img:
                    lst_number_img = list(map(int, number_img.split(',')))
                else:
                    lst_number_img = [int(number_img)]

                result.append(DctModelRenderConfig(
                    template_name=template_name,
                    output_dir=ExistsDirType(os.path.dirname(self.file_name)),
                    file_path=ExistsFileType(os.path.join(
                        os.path.dirname(self.file_name),
                        yaml_output['file_name']
                    )),
                    file_name=yaml_output['file_name'],
                    image_name=yaml_output['image_name'],
                    angle_rotation_z=yaml_output['angle_rotation_z'],
                    max_rotation_z=yaml_output['max_rotation_z'],
                    save_as=yaml_output['save_as'],
                    save_project=yaml_output['save_project'],
                    always_rerender=yaml_output['always_rerender'],
                    number_imgs=lst_number_img,  # type: ignore
                ))
        return result

    def import_config(self) -> list[DctModelRenderConfig]:
        return super().import_config()


__all__ = [
    'BlenderConfigImporter',
]
