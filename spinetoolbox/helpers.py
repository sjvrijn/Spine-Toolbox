######################################################################################################################
# Copyright (C) 2017 - 2019 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
General helper functions and classes.

:authors: P. Savolainen (VTT)
:date:   10.1.2018
"""

import sys
import logging
import datetime
import os
import time
import shutil
import glob
import json
import spinedb_api
from PySide2.QtCore import Qt, Slot, QFile, QIODevice, QSize, QRect, QPoint
from PySide2.QtCore import __version__ as qt_version
from PySide2.QtCore import __version_info__ as qt_version_info
from PySide2.QtWidgets import QApplication, QMessageBox, QGraphicsScene
from PySide2.QtGui import (
    QCursor,
    QImageReader,
    QPixmap,
    QPainter,
    QColor,
    QIcon,
    QIconEngine,
    QFont,
    QStandardItemModel,
    QStandardItem,
)
from .config import DEFAULT_PROJECT_DIR, REQUIRED_SPINEDB_API_VERSION


def set_taskbar_icon():
    """Set application icon to Windows taskbar."""
    if os.name == "nt":
        import ctypes

        myappid = "{6E794A8A-E508-47C4-9319-1113852224D3}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


@Slot(name="supported_img_formats")
def supported_img_formats():
    """Function to check if reading .ico files is supported."""
    img_formats = QImageReader().supportedImageFormats()
    img_formats_str = '\n'.join(str(x) for x in img_formats)
    logging.debug("Supported Image formats:\n%s", img_formats_str)


def pyside2_version_check():
    """Check that PySide2 version is older than 5.12, since this is not supported yet.
    Issue #238 in GitLab.

    qt_version is the Qt version used to compile PySide2 as string. E.g. "5.11.2"
    qt_version_info is a tuple with each version component of Qt used to compile PySide2. E.g. (5, 11, 2)
    """
    # print("Your QT version info is:{0} version string:{1}".format(qt_version_info, qt_version))
    if qt_version_info[0] == 5 and qt_version_info[1] >= 12:
        print(
            """Sorry for the inconvenience but,

            Spine Toolbox does not support PySide2 version {0} yet.
            Please downgrade PySide2 to version 5.11.x and try to start the application again.

            To downgrade PySide2 to a compatible version, run

                pip install "pyside2<5.12"

            """.format(
                qt_version
            )
        )
        return False
    return True


def spinedb_api_version_check():
    """Check if spinedb_api is the correct version and explain how to upgrade if it is not."""
    try:
        current_version = spinedb_api.__version__
        current_split = [int(x) for x in current_version.split(".")]
        required_split = [int(x) for x in REQUIRED_SPINEDB_API_VERSION.split(".")]
        if current_split >= required_split:
            return True
    except AttributeError:
        current_version = "not reported"
    script = "upgrade_spinedb_api.bat" if sys.platform == "win32" else "upgrade_spinedb_api.sh"
    print(
        """ERROR:
        Spine Toolbox failed to start because spinedb_api is outdated.
        (Required version is {0}, whereas current is {1})
        Please upgrade spinedb_api to v{0} and start Spine Toolbox again.

        To upgrade, run script '{2}' in the '/bin' folder.

        Or upgrade it manually by running,

            pip install --upgrade git+https://github.com/Spine-project/Spine-Database-API.git

        """.format(
            REQUIRED_SPINEDB_API_VERSION, current_version, script
        )
    )
    return False


def busy_effect(func):
    """ Decorator to change the mouse cursor to 'busy' while a function is processed.

    Args:
        func: Decorated function.
    """

    def new_function(*args, **kwargs):
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QApplication.setOverrideCursor(QCursor(Qt.BusyCursor))
        try:
            return func(*args, **kwargs)
        finally:
            # noinspection PyArgumentList
            QApplication.restoreOverrideCursor()

    return new_function


def project_dir(qsettings):
    """Returns current project directory.

    Args:
        qsettings (QSettings): Settings object
    """
    # NOTE: This is not actually used. The key is not saved to qsettings anywhere. This is a placeholder for code
    # if we want to be able to change the projects directory at some point.
    proj_dir = qsettings.value("appSettings/projectsDir", defaultValue="")
    if not proj_dir:
        return DEFAULT_PROJECT_DIR
    return proj_dir


def get_datetime(show):
    """Returns date and time string for appending into Event Log messages.

    Args:
        show (boolean): True returns date and time string. False returns empty string.
    """
    if show:
        t = datetime.datetime.now()
        return "[{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}] ".format(t.day, t.month, t.year, t.hour, t.minute, t.second)
    return ""


def create_dir(base_path, folder='', verbosity=False):
    """Create (input/output) directories recursively.

    Args:
        base_path (str): Absolute path to wanted dir
        folder (str): (Optional) Folder name. Usually short name of item.
        verbosity (bool): True prints a message that tells if the directory already existed or if it was created.

    Returns:
        True if directory already exists or if it was created successfully.

    Raises:
        OSError if operation failed.
    """
    directory = os.path.join(base_path, folder)
    if os.path.exists(directory) and verbosity:
        logging.debug("Directory found: %s", directory)
    else:
        os.makedirs(directory, exist_ok=True)
        if verbosity:
            logging.debug("Directory created: %s", directory)
    return True


def create_output_dir_timestamp():
    """ Creates a new timestamp string that is used as Tool output
    directory.

    Returns:
        Timestamp string or empty string if failed.
    """
    try:
        # Create timestamp
        stamp = datetime.datetime.fromtimestamp(time.time())
    except OverflowError:
        logging.error('Timestamp out of range.')
        return ''
    extension = stamp.strftime('%Y-%m-%dT%H.%M.%S')
    return extension


def create_log_file_timestamp():
    """ Creates a new timestamp string that is used as Data Interface and Data Store error log file.

    Returns:
        Timestamp string or empty string if failed.
    """
    try:
        # Create timestamp
        stamp = datetime.datetime.fromtimestamp(time.time())
    except OverflowError:
        logging.error('Timestamp out of range.')
        return ''
    extension = stamp.strftime('%Y%m%dT%H%M%S')
    return extension


@busy_effect
def copy_files(src_dir, dst_dir, includes=None, excludes=None):
    """Method for copying files. Does not copy folders.

    Args:
        src_dir (str): Source directory
        dst_dir (str): Destination directory
        includes (list): Included files (wildcards accepted)
        excludes (list): Excluded files (wildcards accepted)

    Returns:
        count (int): Number of files copied
    """
    if not includes:
        includes = ['*']
    if not excludes:
        excludes = []
    src_files = []
    for pattern in includes:
        src_files += glob.glob(os.path.join(src_dir, pattern))
    exclude_files = []
    for pattern in excludes:
        exclude_files += glob.glob(os.path.join(src_dir, pattern))
    count = 0
    for filename in src_files:
        if os.path.isdir(filename):
            continue
        if filename not in exclude_files:
            shutil.copy(filename, dst_dir)
            count += 1
    return count


@busy_effect
def erase_dir(path, verbosity=False):
    """Delete directory and all its contents without prompt.

    Args:
        path (str): Path to directory
        verbosity (bool): Print logging messages or not
    """
    if not os.path.exists(path):
        if verbosity:
            logging.debug("Path does not exist: %s", path)
        return False
    if verbosity:
        logging.debug("Deleting directory %s", path)
    shutil.rmtree(path)
    return True


@busy_effect
def copy_dir(widget, src_dir, dst_dir):
    """Make a copy of a directory. All files and folders are copied.

    Args:
        widget (QWidget): Parent widget for QMessageBoxes
        src_dir (str): Absolute path to directory that will be copied
        dst_dir (str): Absolute path to new directory
    """
    try:
        shutil.copytree(src_dir, dst_dir)
    except FileExistsError:
        msg = "Directory<br/><b>{0}</b><br/>already exists".format(dst_dir)
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "Copying directory failed", msg)
        return False
    except PermissionError as pe_e:
        logging.error(pe_e)
        msg = (
            "Access to directory <br/><b>{0}</b><br/>denied."
            "<br/><br/>Possible reasons:"
            "<br/>1. Permission error"
            "<br/>2. Windows Explorer is open in the directory"
            "<br/><br/>Check these and try again.".format(dst_dir)
        )
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "Permission Error", msg)
        return False
    except OSError as os_e:
        logging.error(os_e)
        msg = (
            "Copying directory "
            "<br/><b>{0}</b> "
            "<br/>to "
            "<br/><b>{1}</b> "
            "<br/>failed."
            "<br/><br/>Possibly reasons:"
            "<br/>1. Windows Explorer is open in the source or destination directory."
            "<br/>2. A file in these directories is open in another program. "
            "<br/><br/>Check these and try again.".format(src_dir, dst_dir)
        )
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "OS Error", msg)
        return False
    return True


def rename_dir(widget, old_dir, new_dir):
    """Rename directory. Note: This is not used in renaming projects due to unreliability.
    Looks like it works fine in renaming project items though.

    Args:
        widget (QWidget): Parent widget for QMessageBoxes
        old_dir (str): Absolute path to directory that will be renamed
        new_dir (str): Absolute path to new directory
    """
    try:
        shutil.move(old_dir, new_dir)
    except FileExistsError:
        msg = "Directory<br/><b>{0}</b><br/>already exists".format(new_dir)
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "Renaming directory failed", msg)
        return False
    except PermissionError as pe_e:
        logging.error(pe_e)
        msg = (
            "Access to directory <br/><b>{0}</b><br/>denied."
            "<br/><br/>Possible reasons:"
            "<br/>1. You don't have a permission to edit the directory"
            "<br/>2. Windows Explorer is open in the directory"
            "<br/><br/>Check these and try again.".format(old_dir)
        )
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "Renaming directory failed (Permission Error)", msg)
        return False
    except OSError as os_e:
        logging.error(os_e)
        msg = (
            "Renaming directory "
            "<br/><b>{0}</b> "
            "<br/>to "
            "<br/><b>{1}</b> "
            "<br/>failed."
            "<br/><br/>Possibly reasons:"
            "<br/>1. Windows Explorer is open in the directory."
            "<br/>2. A file in the directory is open in another program. "
            "<br/><br/>Check these and try again.".format(old_dir, new_dir)
        )
        # noinspection PyTypeChecker, PyArgumentList, PyCallByClass
        QMessageBox.information(widget, "Renaming directory failed (OS Error)", msg)
        return False
    return True


def fix_name_ambiguity(name_list, offset=0):
    """Modify repeated entries in name list by appending an increasing integer."""
    ref_name_list = name_list.copy()
    ocurrences = {}
    for i, name in enumerate(name_list):
        n_ocurrences = ref_name_list.count(name)
        if n_ocurrences == 1:
            continue
        ocurrence = ocurrences.setdefault(name, 1)
        name_list[i] = name + str(offset + ocurrence)
        ocurrences[name] = ocurrence + 1


def tuple_itemgetter(itemgetter_func, num_indexes):
    """Change output of itemgetter to always be a tuple even for one index"""
    return (lambda item: (itemgetter_func(item),)) if num_indexes == 1 else itemgetter_func


def format_string_list(str_list):
    """Return an unordered html list with all elements in str_list.
    Intended to print error logs as returned by spinedb_api.

    Args:
        str_list (list(str))
    """
    return "<ul>" + "".join(["<li>" + str(x) + "</li>" for x in str_list]) + "</ul>"


def get_db_map(url, upgrade=False, codename=None):
    """Returns a DiffDatabaseMapping instance from url.
    If the db is not the latest version, asks the user if they want to upgrade it.
    """
    try:
        db_map = do_get_db_map(url, upgrade, codename)
        return db_map
    except spinedb_api.SpineDBVersionError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Incompatible database version")
        msg.setText(
            "The database at <b>{}</b> is from an older version of Spine "
            "and needs to be upgraded in order to be used with the current version.".format(url)
        )
        msg.setInformativeText(
            "Do you want to upgrade it now?"
            "<p><b>WARNING</b>: After the upgrade, "
            "the database may no longer be used "
            "with previous versions of Spine."
        )
        msg.addButton(QMessageBox.Cancel)
        msg.addButton("Upgrade", QMessageBox.YesRole)
        ret = msg.exec_()  # Show message box
        if ret == QMessageBox.Cancel:
            return None
        return get_db_map(url, upgrade=True, codename=codename)


_db_maps = {}


@busy_effect
def do_get_db_map(url, upgrade, codename):
    """Returns a DiffDatabaseMapping instance from url.
    Called by `get_db_map`.
    """
    if (url, upgrade, codename) not in _db_maps:
        _db_maps[url, upgrade, codename] = spinedb_api.DiffDatabaseMapping(url, upgrade=upgrade, codename=codename)
    return _db_maps[url, upgrade, codename]


def rows_to_row_count_tuples(rows):
    """Breaks a list of rows into a list of (row, count) tuples corresponding
    to chunks of successive rows.
    """
    if not rows:
        return []
    sorted_rows = sorted(set(rows))
    break_points = [k + 1 for k in range(len(sorted_rows) - 1) if sorted_rows[k] + 1 != sorted_rows[k + 1]]
    break_points = [0] + break_points + [len(sorted_rows)]
    ranges = [(break_points[l], break_points[l + 1]) for l in range(len(break_points) - 1)]
    return [(sorted_rows[start], stop - start) for start, stop in ranges]


class Singleton(type):
    """A singleton class from SO."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class IconListManager:
    """A class to manage icons for icon list widgets."""

    def __init__(self, icon_size):
        self._icon_size = icon_size
        self.searchterms = {}
        self.model = QStandardItemModel()
        self.model.data = self._model_data

    @busy_effect
    def init_model(self):
        """Init model that can be used to display all icons in a list."""
        if self.searchterms:
            return
        qfile = QFile(":/fonts/fontawesome5-searchterms.json")
        qfile.open(QIODevice.ReadOnly | QIODevice.Text)
        data = str(qfile.readAll().data(), "utf-8")
        qfile.close()
        self.searchterms = json.loads(data)
        items = []
        for codepoint, searchterms in self.searchterms.items():
            item = QStandardItem()
            display_icon = int(codepoint, 16)
            item.setData(display_icon, Qt.UserRole)
            item.setData(searchterms, Qt.UserRole + 1)
            items.append(item)
        self.model.invisibleRootItem().appendRows(items)

    def _model_data(self, index, role):
        """Replacement method for model.data().
        Create pixmaps as they're requested by the data() method, to reduce loading time.
        """
        if role == Qt.DisplayRole:
            return None
        if role != Qt.DecorationRole:
            return QStandardItemModel.data(self.model, index, role)
        display_icon = index.data(Qt.UserRole)
        pixmap = self.create_object_pixmap(display_icon)
        return QIcon(pixmap)

    def create_object_pixmap(self, display_icon):
        """Create and return a pixmap corresponding to display_icon."""
        icon_code, color_code = interpret_icon_id(display_icon)
        engine = CharIconEngine(chr(icon_code), color_code)
        return engine.pixmap(self._icon_size)


class IconManager:
    """A class to manage object class icons for data store forms."""

    ICON_SIZE = QSize(512, 512)

    def __init__(self):
        self.obj_cls_icon_cache = {}  # A mapping from object class name to display icon
        self.icon_pixmap_cache = {}  # A mapping from display_icon to associated pixmap
        self.rel_cls_icon_cache = {}  # A mapping from object class name list to associated pixmap
        self.searchterms = {}

    def create_object_pixmap(self, display_icon):
        """Create a pixmap corresponding to display_icon, cache it, and return it."""
        pixmap = self.icon_pixmap_cache.get(display_icon, None)
        if pixmap is None:
            icon_code, color_code = interpret_icon_id(display_icon)
            engine = CharIconEngine(chr(icon_code), color_code)
            pixmap = engine.pixmap(self.ICON_SIZE)
            self.icon_pixmap_cache[display_icon] = pixmap
        return pixmap

    def setup_object_pixmaps(self, object_classes):
        """Called after adding or updating object classes.
        Create the corresponding object pixmaps and clear obsolete entries
        from the relationship class icon cache."""
        for object_class in object_classes:
            self.create_object_pixmap(object_class["display_icon"])
            self.obj_cls_icon_cache[object_class["name"]] = object_class["display_icon"]
        object_class_names = [x["name"] for x in object_classes]
        dirty_keys = [k for k in self.rel_cls_icon_cache if any(x in object_class_names for x in k)]
        for k in dirty_keys:
            del self.rel_cls_icon_cache[k]

    def object_pixmap(self, object_class_name):
        """A pixmap for the given object class."""
        if object_class_name in self.obj_cls_icon_cache:
            display_icon = self.obj_cls_icon_cache[object_class_name]
            if display_icon in self.icon_pixmap_cache:
                return self.icon_pixmap_cache[display_icon]
        engine = CharIconEngine("\uf1b2", 0)
        return engine.pixmap(self.ICON_SIZE)

    def object_icon(self, object_class_name):
        """An icon for the given object class."""
        return QIcon(self.object_pixmap(object_class_name))

    def relationship_pixmap(self, str_object_class_name_list):
        """A pixmap for the given object class name list,
        created by rendering several object pixmaps next to each other."""
        if not str_object_class_name_list:
            engine = CharIconEngine("\uf1b3", 0)
            return engine.pixmap(self.ICON_SIZE)
        object_class_name_list = tuple(str_object_class_name_list.split(","))
        if object_class_name_list in self.rel_cls_icon_cache:
            return self.rel_cls_icon_cache[object_class_name_list]
        scene = QGraphicsScene()
        x = 0
        for j, object_class_name in enumerate(object_class_name_list):
            pixmap = self.object_pixmap(object_class_name)
            pixmap_item = scene.addPixmap(pixmap)
            if j % 2 == 0:
                y = 0
            else:
                y = -0.875 * 0.75 * pixmap_item.boundingRect().height()
                pixmap_item.setZValue(-1)
            pixmap_item.setPos(x, y)
            x += 0.875 * 0.5 * pixmap_item.boundingRect().width()
        pixmap = QPixmap(scene.itemsBoundingRect().toRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        scene.render(painter)
        painter.end()
        self.rel_cls_icon_cache[object_class_name_list] = pixmap
        return pixmap

    def relationship_icon(self, str_object_class_name_list):
        """An icon for the given object class name list."""
        return QIcon(self.relationship_pixmap(str_object_class_name_list))


class CharIconEngine(QIconEngine):
    """Specialization of QIconEngine used to draw font-based icons."""

    def __init__(self, char, color):
        super().__init__()
        self.char = char
        self.color = color
        self.font = QFont('Font Awesome 5 Free Solid')

    def paint(self, painter, rect, mode=None, state=None):
        painter.save()
        size = 0.875 * round(rect.height())
        self.font.setPixelSize(size)
        painter.setFont(self.font)
        painter.setPen(QColor(self.color))
        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, self.char)
        painter.restore()

    def pixmap(self, size, mode=None, state=None):
        pm = QPixmap(size)
        pm.fill(Qt.transparent)
        self.paint(QPainter(pm), QRect(QPoint(0, 0), size), mode, state)
        return pm


def make_icon_id(icon_code, color_code):
    """Take icon and color codes, and return equivalent integer."""
    return icon_code + (color_code << 16)


def interpret_icon_id(display_icon):
    """Take a display icon integer and return an equivalent tuple of icon and color code."""
    if not isinstance(display_icon, int) or display_icon < 0:
        return 0xF1B2, 0
    icon_code = display_icon & 65535
    try:
        color_code = display_icon >> 16
    except OverflowError:
        color_code = 0
    return icon_code, color_code


def default_icon_id():
    return make_icon_id(*interpret_icon_id(None))
