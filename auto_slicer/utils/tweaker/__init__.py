from .FileHandler import load_mesh
from .MeshTweaker import Tweak


def make_tweaked_file(input_file: str) -> str:
    lst_dct_mesh = load_mesh(input_file)
    info = dict()
    for part, content in enumerate(lst_dct_mesh):
        mesh = content["mesh"]
        info[part] = dict()
        x = Tweak(mesh, args.extended_mode, args.verbose, args.show_progress, args.favside, args.volume)
        info[part]["matrix"] = x.matrix
        info[part]["tweaker_stats"] = x

    try:
        FileHandler.write_mesh(lst_dct_mesh, info, args.outputfile, args.output_type)
    except FileNotFoundError:
        raise FileNotFoundError("Output File '{}' not found.".format(args.outputfile))