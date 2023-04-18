######################################################################################################################
# Copyright (C) 2017-2022 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
cx-Freeze setup file for Spine Toolbox.

Requires: Python3.7-64bit. cx_Freeze 6.6.

NOTE: This file is for release-0.6 branch.

To make a Spine Toolbox installation bundle, follow these steps:

On Windows:

1. Build application with command 'python cx_Freeze_setup.py build'
2. Check version numbers and CHANGELOG
3. Compile setup.iss file with Inno Setup. This will create a single-file (.exe) installer.

On other platforms (not tested):
1. Build the application into build/ directory with command 'python cx_Freeze_setup.py build'
2. Use cx_Freeze_setup.py (this file) and Cx_Freeze (see Cx_Freeze documentation for help)

:author: P. Savolainen (VTT)
:date:   29.5.2018
"""

import os
import sys
from cx_Freeze import setup, Executable
from spinetoolbox.config import APPLICATION_PATH

version = {}
with open("spinetoolbox/version.py") as fp:
    exec(fp.read(), version)


def main(argv):
    """Main of cx_Freeze_setup.py."""
    python_dir, python_exe = os.path.split(sys.executable)
    python37_dll = os.path.join(python_dir, "python37.dll")
    os.environ['TCL_LIBRARY'] = os.path.join(python_dir, "tcl", "tcl8.6")
    os.environ['TK_LIBRARY'] = os.path.join(python_dir, "tcl", "tk8.6")
    # tcl86t.dll and tk86t.dll are required by tkinter, which in turn is required by matplotlib
    tcl86t_dll = os.path.join(python_dir, "DLLs", "tcl86t.dll")
    tk86t_dll = os.path.join(python_dir, "DLLs", "tk86t.dll")
    # Path to built documentation (No need for sources)
    doc_path = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "docs", "build"))
    # Paths to files that should be included as is (changelog, readme, licence files, alembic version files)
    changelog_file = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "CHANGELOG.md"))
    readme_file = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "README.md"))
    copying_file = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "COPYING"))
    copying_lesser_file = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "COPYING.LESSER"))
    alembic_version_files = alembic_files(python_dir)
    pyvenv_cfg = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "build_utils", "pyvenv.cfg"))
    path_pth = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "build_utils", "path.pth"))
    site_customize = os.path.abspath(os.path.join(APPLICATION_PATH, os.path.pardir, "build_utils", "sitecustomize.py"))
    # Most dependencies are automatically detected but some need to be manually included.
    build_exe_options = {
        "packages": ["packaging", "pkg_resources", "spine_engine", "spine_items", "spinedb_api"],
        "excludes": [],
        "includes": [
            "atexit",
            "pygments.lexers.markup",
            "pygments.lexers.python",
            "pygments.lexers.shell",
            "pygments.lexers.julia",
            "pygments.styles.default",
            "qtconsole.client",
            "sqlalchemy.sql.default_comparator",
            "sqlalchemy.ext.baked",
            "ijson.compat",
            "ijson.backends.__init__",
            "ijson.backends.python",
            "ijson.backends.yajl",
            "ijson.backends.yajl2",
            "ijson.backends.yajl2_c",
            "ijson.backends.yajl2_cffi",
        ],
        "include_files": [
            (doc_path, "docs/"),
            tcl86t_dll,
            tk86t_dll,
            changelog_file,
            readme_file,
            copying_file,
            copying_lesser_file,
            (sys.executable, os.path.join("tools/", python_exe)),
            (python37_dll, os.path.join("tools/", "python37.dll")),
            pyvenv_cfg,
            path_pth,
            site_customize,
        ]
        + alembic_version_files,
        "include_msvcr": True
    }
    # Windows specific options
    base = "Win32GUI" if os.name == "nt" else None
    executables = [Executable("spinetoolbox.py", base=base, icon="spinetoolbox/ui/resources/app.ico")]
    setup(
        name="Spine Toolbox",
        version=version["__version__"],
        description="An application to define, manage, and execute various energy system simulation models.",
        author="Spine project consortium",
        options={"build_exe": build_exe_options},
        executables=executables,
    )


def alembic_files(python_dir):
    """Returns a list of tuples of files in python/Lib/site-packages/spinedb_api/alembic/versions.
    First item in tuple is the source file. Second item is the relative destination path to the install directory.
    We are including these .py files into 'include_files' list because adding them to the 'includes' list
    would require us to give the whole explicit file name.
    """
    dest_dir = os.path.join("lib", "spinedb_api", "alembic", "versions")
    p = os.path.join(python_dir, "Lib", "site-packages", "spinedb_api", "alembic", "versions")
    return [
        (os.path.abspath(os.path.join(p, f)), os.path.join(dest_dir, f))
        for f in os.listdir(p)
        if f.endswith(".py")
    ]


if __name__ == '__main__':
    sys.exit(main(sys.argv))
