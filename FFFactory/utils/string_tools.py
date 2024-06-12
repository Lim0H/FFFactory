from ..auto_slicer.utils.consts.string_utils_const import TO_REPLACE_LETTERS, TO_DELETE_LIST


def clean_name(name: str) -> str:
    for i, j in TO_REPLACE_LETTERS.items():
        name = name.replace(i, j)
    for i in TO_DELETE_LIST:
        name = name.replace(i, "")
    return name
