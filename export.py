import os
import cadquery as cq
from tempfile import mkstemp

def stl(object):
    (_, file) = mkstemp(suffix=".stl")
    data = None

    cq.exporters.export(object, file)

    with open(file, mode="rb") as f:
        data = f.read()

    os.remove(file)

    return data


def glb(assembly):
    (_, file) = mkstemp(suffix=".glb")
    data = None

    assembly.export(file)

    with open(file, mode="rb") as f:
        data = f.read()

    os.remove(file)

    return data
