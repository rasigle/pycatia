# !/usr/bin/python3.10

"""
This script is strictly for the use of generating the pyv5.exe executable.
"""

import argparse
import textwrap
from pathlib import Path

from pyv5.version import __version__ as version

if __name__ == "__main__":
    prog = "pyv5"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
        =====================================================================
                                 pyv5
        =====================================================================
           This executable is currently provided for testing purposes only.
        Documentation: https://pyv5.readthedocs.io/en/latest/
        =====================================================================
        """),
        prog=prog,
        usage="pyv5.exe file_name.py",
    )

    parser.add_argument(
        "filename", type=str, help="The full path filename of the python script file."
    )
    parser.add_argument("--version", action="version", version=f"{prog} {version}")

    filename = Path(parser.parse_args().filename)

    if not filename.exists():
        raise FileNotFoundError(
            f'Could not find file "{filename}". Try using the full path name.'
        )

    with open(str(filename)) as f:
        exec(f.read())
    