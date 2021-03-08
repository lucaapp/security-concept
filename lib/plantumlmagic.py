"""adapted from https://github.com/jbn/IPlantUML"""

import argparse
import os
import subprocess
import uuid

from IPython.core.magic import register_cell_magic
from IPython.display import Image, SVG


def _exec_and_get_paths(cmd, file_names, output_format):
    subprocess.check_call(cmd, shell=False, stderr=subprocess.STDOUT)

    return [os.path.splitext(f)[0] + "." + output_format for f in file_names]


def plantuml_exec(*file_names, **kwargs):
    plantuml_path = kwargs.get("plantuml_path")
    output_format = kwargs.get("output_format")

    cmd = ["java", "-splash:no", "-jar", plantuml_path, "-t" + output_format] + list(
        file_names
    )

    return _exec_and_get_paths(cmd, file_names, output_format)


@register_cell_magic
def plantuml(line, cell):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=None,
        help="persist as <name>.uml and <name>.svg after rendering",
    )
    args = parser.parse_args(line.split() if line else "")
    retain = args.name is not None
    base_name = args.name or str(uuid.uuid4())

    uml_path = base_name + ".uml"
    with open(uml_path, "w") as fp:
        fp.write(cell)

    output_format = os.getenv("PLANTUMLFORMAT", default="svg")
    if output_format not in ["svg", "png"]:
        raise Error("unsupported image format '{}'".format(output_format))

    plantuml_path = os.getenv("PLANTUMLPATH", default="/usr/local/bin/plantuml.jar")

    try:
        output = plantuml_exec(
            uml_path, plantuml_path=plantuml_path, output_format=output_format
        )
        image_name = output[0]

        if output_format == "svg":
            return SVG(filename=image_name)
        elif output_format == "png":
            return Image(filename=image_name)
        else:
            raise Error("unsupported image format '{}'".format(output_format))

    finally:
        if not retain:
            if os.path.exists(uml_path):
                os.unlink(uml_path)
            image_path = base_name + ".{}".format(output_format)
            if os.path.exists(image_path):
                os.unlink(image_path)
