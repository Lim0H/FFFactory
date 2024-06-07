# Python 2.7 and 3.5
# Author: Christoph Schranz, Salzburg Research

from abc import ABC, abstractmethod
from io import BufferedReader
import struct
import time
from typing import Callable, Generator, Optional, TypedDict
import numpy as np
from xtyping import OpenBinaryModeReading, OpenBinaryModeWriting

from auto_slicer.utils.consts.tweaker_const import FILE
from . import ThreeMF
from decorator import decorator


class DctMesh(TypedDict):
    mesh: list[list]
    name: str


class WriterMeshBase(ABC):
    FILE_TYPE: str = None
    METHOD_READ_FILE: Optional[OpenBinaryModeWriting] = None

    def __init__(self, lst_dct_mesh: list[DctMesh]):
        self.__lst_dct_mesh = lst_dct_mesh

    @abstractmethod
    def generate_content_to_write(self) -> Generator[DctMesh, None, None]:
        raise NotImplementedError()

    def write(self):
        generator = self.generate_content_to_write()
        for dct_mesh in generator:
            with open(dct_mesh["name"], self.METHOD_READ_FILE) as outfile:
                outfile.write(dct_mesh["mesh"])


class WriterAsciiStl(WriterMeshBase):
    FILE_TYPE = "stl"
    METHOD_READ_FILE = "w"

    def rotate_ascii_stl(rotation_matrix, content, filename):
        """Rotate the mesh array and save as ASCII STL."""
        mesh = np.array(content, dtype=np.float64)

        # prefix area vector, if not already done (e.g. in STL format)
        if len(mesh[0]) == 3:
            row_number = int(len(content) / 3)
            mesh = mesh.reshape(row_number, 3, 3)

        # upgrade numpy with: "pip install numpy --upgrade"
        mesh = np.matmul(mesh, rotation_matrix)

        v0 = mesh[:, 0, :]
        v1 = mesh[:, 1, :]
        v2 = mesh[:, 2, :]
        normals = np.cross(np.subtract(v1, v0), np.subtract(v2, v0)) \
            .reshape(int(len(mesh)), 1, 3)
        mesh = np.hstack((normals, mesh))

        tweaked = list("solid %s" % filename)
        tweaked += list(map(write_facett, list(mesh)))
        tweaked.append("\nendsolid %s\n" % filename)
        tweaked = "".join(tweaked)
        return tweaked

    def generate_content_to_write(self) -> Generator[DctMesh, None, None]:
        for content in self.__lst_dct_mesh:
            mesh = content["mesh"]
            filename = content["name"]

            mesh = rotate_ascii_stl(info[part]["matrix"], mesh, filename)
            if len(objects.keys()) == 1:
                outname = outputfile
            else:
                outname = ".".join(outputfile.split(".")[:-1]) + "_{}.stl".format(part)


def write_mesh(objects, info, outputfile, output_type="binarystl"):
    if output_type == "asciistl":
        # Create seperate files with rotated content. If an IDE supports multipart placement,
        # set outname = outputfile
        for part, content in objects.items():
            mesh = content["mesh"]
            filename = content["name"]

            mesh = rotate_ascii_stl(info[part]["matrix"], mesh, filename)
            if len(objects.keys()) == 1:
                outname = outputfile
            else:
                outname = ".".join(outputfile.split(".")[:-1]) + "_{}.stl".format(part)
            with open(outname, 'w') as outfile:
                outfile.write(mesh)

    else:  # binary STL, binary stl can't support multiparts
        # Create seperate files with rotated content.
        header = "Tweaked on {}".format(time.strftime("%a %d %b %Y %H:%M:%S")
                                        ).encode().ljust(79, b" ") + b"\n"
        for part, content in objects.items():
            mesh = objects[part]["mesh"]
            partlength = int(len(mesh) / 3)
            mesh = rotate_bin_stl(info[part]["matrix"], mesh)

            if len(objects.keys()) == 1:
                outname = outputfile
            else:
                outname = ".".join(outputfile.split(".")[:-1]) + "_{}.stl".format(part)
            length = struct.pack("<I", partlength)
            with open(outname, 'wb') as outfile:
                outfile.write(bytearray(header + length + b"".join(mesh)))


def rotate_3mf(*arg):
    ThreeMF.rotate3MF(*arg)


def rotate_ascii_stl(rotation_matrix, content, filename):
    """Rotate the mesh array and save as ASCII STL."""
    mesh = np.array(content, dtype=np.float64)

    # prefix area vector, if not already done (e.g. in STL format)
    if len(mesh[0]) == 3:
        row_number = int(len(content) / 3)
        mesh = mesh.reshape(row_number, 3, 3)

    # upgrade numpy with: "pip install numpy --upgrade"
    mesh = np.matmul(mesh, rotation_matrix)

    v0 = mesh[:, 0, :]
    v1 = mesh[:, 1, :]
    v2 = mesh[:, 2, :]
    normals = np.cross(np.subtract(v1, v0), np.subtract(v2, v0)) \
        .reshape(int(len(mesh)), 1, 3)
    mesh = np.hstack((normals, mesh))

    tweaked = list("solid %s" % filename)
    tweaked += list(map(write_facett, list(mesh)))
    tweaked.append("\nendsolid %s\n" % filename)
    tweaked = "".join(tweaked)
    return tweaked


def write_facett(facett):
    return """\nfacet normal %f %f %f
    outer loop
        vertex %f %f %f
        vertex %f %f %f
        vertex %f %f %f
    endloop
endfacet""" % (
        facett[0, 0], facett[0, 1], facett[0, 2], facett[1, 0],
        facett[1, 1], facett[1, 2], facett[2, 0], facett[2, 1],
        facett[2, 2], facett[3, 0], facett[3, 1], facett[3, 2]
    )


def rotate_bin_stl(rotation_matrix, content):
    """Rotate the object and save as binary STL. This module is currently replaced
    by the ascii version. If you want to use binary STL, please do the
    following changes in Tweaker.py: Replace "rotatebinSTL" by "rotateSTL"
    and set in the write sequence the open outfile option from "w" to "wb".
    However, the ascii version is much faster in Python 3."""
    mesh = np.array(content, dtype=np.float64)

    # prefix area vector, if not already done (e.g. in STL format)
    if len(mesh[0]) == 3:
        row_number = int(len(content) / 3)
        mesh = mesh.reshape(row_number, 3, 3)

    # upgrade numpy with: "pip install numpy --upgrade"
    mesh = np.matmul(mesh, rotation_matrix)

    v0 = mesh[:, 0, :]
    v1 = mesh[:, 1, :]
    v2 = mesh[:, 2, :]
    normals = np.cross(
        np.subtract(v1, v0),
        np.subtract(v2, v0)
    ).reshape(int(len(mesh)), 1, 3)
    mesh = np.hstack((normals, mesh))
    # header = "Tweaked on {}".format(time.strftime("%a %d %b %Y %H:%M:%S")
    #                                 ).encode().ljust(79, b" ") + b"\n"
    # header = struct.pack("<I", int(len(content) / 3))  # list("solid %s" % filename)

    mesh = list(map(write_bin_facett, mesh))

    # return header + b"".join(tweaked_array)
    # return b"".join(tweaked_array)
    return mesh


def write_bin_facett(facett):
    tweaked = struct.pack("<fff", facett[0][0], facett[0][1], facett[0][2])
    tweaked += struct.pack("<fff", facett[1][0], facett[1][1], facett[1][2])
    tweaked += struct.pack("<fff", facett[2][0], facett[2][1], facett[2][2])
    tweaked += struct.pack("<fff", facett[3][0], facett[3][1], facett[3][2])
    tweaked += struct.pack("<H", 0)

    return tweaked


class LoaderMeshBase(ABC):
    METHOD_READ_FILE: Optional[OpenBinaryModeReading] = None
    FILE_TYPE: str = None

    def __init__(self, input_file: str) -> None:
        self.__input_file = input_file
        self.__buffered_file: Optional[BufferedReader] = None

    @property
    def input_file(self) -> str:
        return self.__input_file

    @property
    def buffered_file(self) -> BufferedReader:
        if self.__buffered_file is None:
            raise ValueError("File not opened.")
        return self.__buffered_file

    @property
    def mesh_name(self) -> str:
        if self.FILE_TYPE is None:
            raise ValueError("Mesh name not set.")
        return self.FILE_TYPE + ' ' + FILE

    @abstractmethod
    def _load(self) -> list[list]:
        return NotImplementedError()

    @abstractmethod
    def load(self) -> list[DctMesh]:
        return [
            {
                "mesh": x,
                "name": self.mesh_name + ' ' + str(i)
            } for i, x in enumerate(self._load())
        ]

    @decorator
    def open_file(self, func: Callable, *args, **kwargs) -> None:
        if self.METHOD_READ_FILE is not None:
            f = open(self.input_file, self.METHOD_READ_FILE)
            if not f.readable():
                raise Exception("File is not readable.")
            self.__buffered_file = f
        func(self, *args, **kwargs)
        if self.__buffered_file is not None:
            self.__buffered_file.close()
        self.__buffered_file = None


class Loader3mf(LoaderMeshBase):
    FILE_TYPE = '3mf'

    def _load(self) -> list[list]:
        object = ThreeMF.Read3mf(self.input_file)
        return [object[0]["mesh"]]


class LoaderObj(LoaderMeshBase):
    METHOD_READ_FILE = 'rb'
    FILE_TYPE = 'obj'

    @LoaderMeshBase.open_file
    def _load(self) -> list[list]:
        mesh = []
        vertices = []
        for line in filter(lambda x: "v" in x, self.buffered_file):
            data = line.split()[1:]
            vertices.append([float(data[0]), float(data[1]), float(data[2])])
        self.buffered_file.seek(0, 0)
        for line in filter(lambda x: "f" in x, self.buffered_file):
            data = line.split()[1:]
            mesh.append(vertices[int(data[0]) - 1])
            mesh.append(vertices[int(data[1]) - 1])
            mesh.append(vertices[int(data[2]) - 1])
        return [mesh]


class LoaderAsciiStl(LoaderMeshBase):
    METHOD_READ_FILE = 'r'
    FILE_TYPE = 'ascii stl'

    @LoaderMeshBase.open_file
    def _load(self) -> list[list]:
        lst_mesh: list[DctMesh] = []
        part = 0
        lst_mesh.append({"mesh": [], "name": "ascii stl"})
        for line in self.buffered_file:
            if "vertex" in line:
                data = line.split()[1:]
                lst_mesh[part]["mesh"].append([float(data[0]), float(data[1]), float(data[2])])
            if "endsolid" in line:
                lst_mesh[part]["name"] = line.split()[-1]
                part += 1
                lst_mesh.append({"mesh": [], "name": "ascii stl"})

        return [v["mesh"] for v in lst_mesh if len(v["mesh"]) > 3]


class LoaderBinaryStl(LoaderMeshBase):
    METHOD_READ_FILE = 'rb'
    FILE_TYPE = 'binary stl'

    @LoaderMeshBase.open_file
    def _load(self) -> list[list]:
        self.buffered_file.read(80 - 5)
        face_count = struct.unpack('<I', self.buffered_file.read(4))[0]
        mesh: list = []
        for _ in range(face_count):
            data = struct.unpack("<ffffffffffffH", self.buffered_file.read(50))
            mesh.append([data[3], data[4], data[5]])
            mesh.append([data[6], data[7], data[8]])
            mesh.append([data[9], data[10], data[11]])
        return [mesh]


class LoaderStl(LoaderMeshBase):
    METHOD_READ_FILE = 'rb'
    FILE_TYPE = 'stl'

    @LoaderMeshBase.open_file
    def _load(self) -> list[list]:
        loaded_result: list[DctMesh] = []
        if "solid" in str(self.buffered_file.read(5).lower()):
            try:
                loaded_result = LoaderAsciiStl(self.input_file).load()
            except UnicodeDecodeError:
                loaded_result = LoaderBinaryStl(self.input_file).load()
        else:
            loaded_result = LoaderBinaryStl(self.input_file).load()
        return [v['mesh'] for v in loaded_result]


TYPE_FILES_LOADER = {
    '3mf': Loader3mf,
    'obj': LoaderObj,
    'stl': LoaderStl
}


def load_mesh(input_file: str) -> list[DctMesh]:
    for file_type, loader in TYPE_FILES_LOADER.items():
        if input_file.endswith('.' + file_type):
            return loader(input_file).load()
    raise Exception("File type %s is not supported" % input_file)
