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
Widget for controlling user settings.

:author: P. Savolainen (VTT)
:date:   17.1.2018
"""

import os
from PySide2.QtWidgets import QWidget, QStyle, QFileDialog, QMessageBox, QColorDialog
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPixmap
import ui.settings
from config import DEFAULT_PROJECT_DIR, DEFAULT_WORK_DIR, SETTINGS_SS


class SettingsWidget(QWidget):
    """A widget to change user's preferred settings.

    Attributes:
        toolbox (ToolboxUI): Parent widget.
    """

    def __init__(self, toolbox):
        """Initialize class."""
        # FIXME: setting the parent to toolbox causes the checkboxes in the
        # groupBox_general to not layout correctly, this might be caused elsewhere?
        super().__init__(parent=None)  # Do not set parent. Uses own stylesheet.
        self._toolbox = toolbox  # QWidget parent
        self._project = self._toolbox.project()
        self._qsettings = self._toolbox.qsettings()
        self.orig_work_dir = ""  # Work dir when this widget was opened
        self.orig_python_env = ""  # Used in determining if Python environment was changed
        # Initial scene bg color. Is overridden immediately in read_settings() if it exists in qSettings
        self.bg_color = self._toolbox.ui.graphicsView.scene().bg_color
        # Set up the ui from Qt Designer files
        self.ui = ui.settings.Ui_SettingsForm()
        self.ui.setupUi(self)
        self.ui.toolButton_browse_gams.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.ui.toolButton_browse_julia.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.ui.toolButton_browse_python.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.ui.toolButton_browse_work.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        # Ensure this window gets garbage-collected when closed
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet(SETTINGS_SS)
        self.ui.pushButton_ok.setDefault(True)
        self._mousePressPos = None
        self._mouseReleasePos = None
        self._mouseMovePos = None
        self.connect_signals()
        self.read_settings()
        self.read_project_settings()

    def connect_signals(self):
        """Connect signals."""
        self.ui.pushButton_ok.clicked.connect(self.ok_clicked)
        self.ui.pushButton_cancel.clicked.connect(self.close)
        self.ui.toolButton_browse_gams.clicked.connect(self.browse_gams_path)
        self.ui.toolButton_browse_julia.clicked.connect(self.browse_julia_path)
        self.ui.toolButton_browse_python.clicked.connect(self.browse_python_path)
        self.ui.toolButton_browse_work.clicked.connect(self.browse_work_path)
        self.ui.toolButton_bg_color.clicked.connect(self.show_color_dialog)
        self.ui.radioButton_bg_grid.clicked.connect(self.update_scene_bg)
        self.ui.radioButton_bg_solid.clicked.connect(self.update_scene_bg)

    @Slot(bool, name="browse_gams_path")
    def browse_gams_path(self, checked=False):
        """Open file browser where user can select a GAMS program."""
        # noinspection PyCallByClass, PyArgumentList
        answer = QFileDialog.getOpenFileName(
            self, "Select GAMS Program (e.g. gams.exe on Windows)", os.path.abspath('C:\\')
        )
        if answer[0] == "":  # Canceled (american-english), cancelled (british-english)
            return
        # Check that it's not a directory
        if os.path.isdir(answer[0]):
            msg = "Please select a valid GAMS program (file) and not a directory"
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid GAMS Program", msg)
            return
        # Check that it's a file that actually exists
        if not os.path.exists(answer[0]):
            msg = "File {0} does not exist".format(answer[0])
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid GAMS Program", msg)
            return
        # Check that selected file at least starts with string 'gams'
        path, selected_file = os.path.split(answer[0])
        if not selected_file.lower().startswith("gams"):
            msg = "Selected file <b>{0}</b> may not be a valid GAMS program".format(selected_file)
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid GAMS Program", msg)
            return
        self.ui.lineEdit_gams_path.setText(answer[0])
        return

    @Slot(bool, name="browse_julia_path")
    def browse_julia_path(self, checked=False):
        """Open file browser where user can select a Julia interpreter (i.e. julia.exe on Windows)."""
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getOpenFileName(
            self, "Select Julia Interpreter (e.g. julia.exe on Windows)", os.path.abspath('C:\\')
        )
        if answer[0] == "":  # Canceled (american-english), cancelled (british-english)
            return
        # Check that it's not a directory
        if os.path.isdir(answer[0]):
            msg = "Please select a valid Julia interpreter (file) and not a directory"
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid Julia Interpreter", msg)
            return
        # Check that it's a file that actually exists
        if not os.path.exists(answer[0]):
            msg = "File {0} does not exist".format(answer[0])
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid Julia Interpreter", msg)
            return
        # Check that selected file at least starts with string 'julia'
        path, selected_file = os.path.split(answer[0])
        if not selected_file.lower().startswith("julia"):
            msg = "Selected file <b>{0}</b> is not a valid Julia interpreter".format(selected_file)
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid Julia Interpreter", msg)
            return
        self.ui.lineEdit_julia_path.setText(answer[0])
        return

    @Slot(bool, name="browse_python_path")
    def browse_python_path(self, checked=False):
        """Open file browser where user can select a python interpreter (i.e. python.exe on Windows)."""
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getOpenFileName(
            self, "Select Python Interpreter (e.g. python.exe on Windows)", os.path.abspath('C:\\')
        )
        if answer[0] == "":  # Canceled
            return
        # Check that it's not a directory
        if os.path.isdir(answer[0]):
            msg = "Please select a valid Python interpreter (file) and not a directory"
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid Python Interpreter", msg)
            return
        # Check that selected file at least starts with string 'python'
        path, selected_file = os.path.split(answer[0])
        if not selected_file.lower().startswith("python"):
            msg = "Selected file <b>{0}</b> is not a valid Python interpreter".format(selected_file)
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, "Invalid Python Interpreter", msg)
            return
        self.ui.lineEdit_python_path.setText(answer[0])
        return

    @Slot(bool, name="browse_work_path")
    def browse_work_path(self, checked=False):
        """Open file browser where user can select the path to wanted work directory."""
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        answer = QFileDialog.getExistingDirectory(self, 'Select Work Directory', os.path.abspath('C:\\'))
        if answer == '':  # Cancel button clicked
            return
        selected_path = os.path.abspath(answer)
        self.ui.lineEdit_work_dir.setText(selected_path)

    @Slot(bool, name="show_color_dialog")
    def show_color_dialog(self, checked=False):
        """Let user pick the bg color.

        Args:
            checked (boolean): Value emitted with clicked signal
        """
        # noinspection PyArgumentList
        color = QColorDialog.getColor(initial=self.bg_color)
        if not color.isValid():
            return  # Canceled
        self.ui.radioButton_bg_solid.setChecked(True)
        self.bg_color = color
        self.update_bg_color()

    def update_bg_color(self):
        """Set tool button icon as the selected color and update
        Design View scene background color."""
        pixmap = QPixmap(16, 16)
        pixmap.fill(self.bg_color)
        self.ui.toolButton_bg_color.setIcon(pixmap)
        self._toolbox.ui.graphicsView.scene().set_bg_color(self.bg_color)
        self._toolbox.ui.graphicsView.scene().update()

    @Slot(bool, name="update_scene_bg")
    def update_scene_bg(self, checked):
        """Draw background on scene depending on radiobutton states.

        Args:
            checked (boolean): Toggle state
        """
        if self.ui.radioButton_bg_grid.isChecked():
            self._toolbox.ui.graphicsView.scene().set_bg_grid(True)
            self._toolbox.ui.graphicsView.scene().update()
        elif self.ui.radioButton_bg_solid.isChecked():
            self._toolbox.ui.graphicsView.scene().set_bg_grid(False)
            self._toolbox.ui.graphicsView.scene().update()

    def read_settings(self):
        """Read saved settings from app QSettings instance and update UI to display them."""
        # checkBox check state 0: unchecked, 1: partially checked, 2: checked
        # QSettings value() method returns a str even if a boolean was stored
        open_previous_project = int(self._qsettings.value("appSettings/openPreviousProject", defaultValue="2"))
        show_exit_prompt = int(self._qsettings.value("appSettings/showExitPrompt", defaultValue="2"))
        save_at_exit = int(self._qsettings.value("appSettings/saveAtExit", defaultValue="1"))  # tri-state
        datetime = int(self._qsettings.value("appSettings/dateTime", defaultValue="2"))
        delete_data = int(self._qsettings.value("appSettings/deleteData", defaultValue="0"))
        smooth_zoom = self._qsettings.value("appSettings/smoothZoom", defaultValue="false")
        bg_grid = self._qsettings.value("appSettings/bgGrid", defaultValue="false")
        bg_color = self._qsettings.value("appSettings/bgColor", defaultValue="false")
        gams_path = self._qsettings.value("appSettings/gamsPath", defaultValue="")
        use_embedded_julia = self._qsettings.value("appSettings/useEmbeddedJulia", defaultValue="2")
        julia_path = self._qsettings.value("appSettings/juliaPath", defaultValue="")
        use_embedded_python = self._qsettings.value("appSettings/useEmbeddedPython", defaultValue="0")
        python_path = self._qsettings.value("appSettings/pythonPath", defaultValue="")
        commit_at_exit = int(self._qsettings.value("appSettings/commitAtExit", defaultValue="1"))  # tri-state
        if open_previous_project == 2:
            self.ui.checkBox_open_previous_project.setCheckState(Qt.Checked)
        if show_exit_prompt == 2:
            self.ui.checkBox_exit_prompt.setCheckState(Qt.Checked)
        if save_at_exit == 0:  # Not needed but makes the code more readable.
            self.ui.checkBox_save_at_exit.setCheckState(Qt.Unchecked)
        elif save_at_exit == 1:
            self.ui.checkBox_save_at_exit.setCheckState(Qt.PartiallyChecked)
        else:  # save_at_exit == 2:
            self.ui.checkBox_save_at_exit.setCheckState(Qt.Checked)
        if datetime == 2:
            self.ui.checkBox_datetime.setCheckState(Qt.Checked)
        if delete_data == 2:
            self.ui.checkBox_delete_data.setCheckState(Qt.Checked)
        if smooth_zoom == "true":
            self.ui.checkBox_use_smooth_zoom.setCheckState(Qt.Checked)
        if bg_grid == "true":
            self.ui.radioButton_bg_grid.setChecked(True)
        else:
            self.ui.radioButton_bg_solid.setChecked(True)
        if bg_color == "false":
            pass
        else:
            self.bg_color = bg_color
        self.update_bg_color()
        if commit_at_exit == 0:  # Not needed but makes the code more readable.
            self.ui.checkBox_commit_at_exit.setCheckState(Qt.Unchecked)
        elif commit_at_exit == 1:
            self.ui.checkBox_commit_at_exit.setCheckState(Qt.PartiallyChecked)
        else:  # commit_at_exit == "2":
            self.ui.checkBox_commit_at_exit.setCheckState(Qt.Checked)
        proj_dir = ""  # Unused. Save/read this using QSettings, if we want to change the projects dir at some point
        if not proj_dir:
            proj_dir = DEFAULT_PROJECT_DIR
        self.ui.lineEdit_project_dir.setText(proj_dir)
        self.ui.lineEdit_gams_path.setText(gams_path)
        if use_embedded_julia == "2":
            self.ui.checkBox_use_embedded_julia.setCheckState(Qt.Checked)
        self.ui.lineEdit_julia_path.setText(julia_path)
        if use_embedded_python == "2":
            self.ui.checkBox_use_embedded_python.setCheckState(Qt.Checked)
        self.ui.lineEdit_python_path.setText(python_path)
        self.orig_python_env = python_path

    def read_project_settings(self):
        """Read project settings from config object and update settings widgets accordingly."""
        work_dir = DEFAULT_WORK_DIR
        if self._project:
            self.ui.lineEdit_project_name.setText(self._project.name)
            self.ui.textEdit_project_description.setText(self._project.description)
            work_dir = self._project.work_dir
        self.ui.lineEdit_work_dir.setText(work_dir)
        self.orig_work_dir = work_dir

    @Slot(name="ok_clicked")
    def ok_clicked(self):
        """Get selections and save them to persistent memory.
        Note: On Linux, True and False are saved as boolean values into QSettings.
        On Windows, booleans and integers are saved as strings. To make it consistent,
        we should use strings.
        """
        # checkBox check state 0: unchecked, 1: partially checked, 2: checked
        # checkBox check states are casted from integers to string because of Linux
        # General
        open_prev_proj = str(int(self.ui.checkBox_open_previous_project.checkState()))
        self._qsettings.setValue("appSettings/openPreviousProject", open_prev_proj)
        exit_prompt = str(int(self.ui.checkBox_exit_prompt.checkState()))
        self._qsettings.setValue("appSettings/showExitPrompt", exit_prompt)
        save_at_exit = str(int(self.ui.checkBox_save_at_exit.checkState()))
        self._qsettings.setValue("appSettings/saveAtExit", save_at_exit)
        datetime = str(int(self.ui.checkBox_datetime.checkState()))
        self._qsettings.setValue("appSettings/dateTime", datetime)
        delete_data = str(int(self.ui.checkBox_delete_data.checkState()))
        self._qsettings.setValue("appSettings/deleteData", delete_data)
        smooth_zoom = "true" if int(self.ui.checkBox_use_smooth_zoom.checkState()) else "false"
        self._qsettings.setValue("appSettings/smoothZoom", smooth_zoom)
        bg_grid = "true" if self.ui.radioButton_bg_grid.isChecked() else "false"
        self._qsettings.setValue("appSettings/bgGrid", bg_grid)
        self._qsettings.setValue("appSettings/bgColor", self.bg_color)
        # GAMS
        gams_path = self.ui.lineEdit_gams_path.text().strip()
        if not self.file_is_valid(gams_path, "Invalid GAMS Program"):  # Check it's a file and it exists
            return
        self._qsettings.setValue("appSettings/gamsPath", gams_path)
        # Julia (cast to str because of Linux)
        use_emb_julia = str(int(self.ui.checkBox_use_embedded_julia.checkState()))  # Cast to str because of Linux
        self._qsettings.setValue("appSettings/useEmbeddedJulia", use_emb_julia)
        julia_path = self.ui.lineEdit_julia_path.text().strip()
        if not self.file_is_valid(julia_path, "Invalid Julia Interpreter"):  # Check it's a file and it exists
            return
        self._qsettings.setValue("appSettings/juliaPath", julia_path)
        # Python
        use_emb_python = str(int(self.ui.checkBox_use_embedded_python.checkState()))  # Cast to str because of Linux
        self._qsettings.setValue("appSettings/useEmbeddedPython", use_emb_python)
        python_path = self.ui.lineEdit_python_path.text().strip()
        if not self.file_is_valid(python_path, "Invalid Python Interpreter"):  # Check it's a file and it exists
            return
        self._qsettings.setValue("appSettings/pythonPath", python_path)
        # Data Store Views
        commit_at_exit = str(int(self.ui.checkBox_commit_at_exit.checkState()))
        self._qsettings.setValue("appSettings/commitAtExit", commit_at_exit)
        # Check if something in the app needs to be updated
        self._toolbox.show_datetime = self._toolbox.update_datetime()
        self.check_if_python_env_changed(python_path)
        # Project
        self.update_project_settings()
        self.close()

    def update_project_settings(self):
        """Update project settings when Ok has been clicked."""
        if not self._project:
            return
        save = False
        if not self.ui.lineEdit_work_dir.text():
            work_dir = DEFAULT_WORK_DIR
        else:
            work_dir = self.ui.lineEdit_work_dir.text()
        # Check if work directory was changed
        if not self.orig_work_dir == work_dir:
            if not self._project.change_work_dir(work_dir):
                self._toolbox.msg_error.emit(
                    "Could not change project work directory. Creating new dir:{0} failed.".format(work_dir)
                )
            else:
                save = True
        if not self._project.description == self.ui.textEdit_project_description.toPlainText():
            # Set new project description
            self._project.set_description(self.ui.textEdit_project_description.toPlainText())
            save = True
        if save:
            self._toolbox.msg.emit("Project settings changed. Saving project...")
            self._toolbox.save_project()

    def check_if_python_env_changed(self, new_path):
        """Checks if Python environment was changed.
        This indicates that the Python Console may need a restart."""
        if not self.orig_python_env == new_path:
            self._toolbox.python_repl.may_need_restart = True
        else:
            self._toolbox.python_repl.may_need_restart = False

    def file_is_valid(self, file_path, msgbox_title):
        """Checks that given path is not a directory and it's a file that actually exists.
        Needed because the QLineEdits are editable."""
        if file_path == "":
            return True
        if os.path.isdir(file_path):
            msg = "Please select a file and not a directory"
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, msgbox_title, msg)
            return False
        if not os.path.exists(file_path):
            msg = "File {0} does not exist".format(file_path)
            # noinspection PyCallByClass, PyArgumentList
            QMessageBox.warning(self, msgbox_title, msg)
            return False
        return True

    def keyPressEvent(self, e):
        """Close settings form when escape key is pressed.

        Args:
            e (QKeyEvent): Received key press event.
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event=None):
        """Handle close window.

        Args:
            event (QEvent): Closing event if 'X' is clicked.
        """
        if event:
            event.accept()

    def mousePressEvent(self, e):
        """Save mouse position at the start of dragging.

        Args:
            e (QMouseEvent): Mouse event
        """
        self._mousePressPos = e.globalPos()
        self._mouseMovePos = e.globalPos()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """Save mouse position at the end of dragging.

        Args:
            e (QMouseEvent): Mouse event
        """
        if self._mousePressPos is not None:
            self._mouseReleasePos = e.globalPos()
            moved = self._mouseReleasePos - self._mousePressPos
            if moved.manhattanLength() > 3:
                e.ignore()
                return

    def mouseMoveEvent(self, e):
        """Moves the window when mouse button is pressed and mouse cursor is moved.

        Args:
            e (QMouseEvent): Mouse event
        """
        currentpos = self.pos()
        globalpos = e.globalPos()
        if not self._mouseMovePos:
            e.ignore()
            return
        diff = globalpos - self._mouseMovePos
        newpos = currentpos + diff
        self.move(newpos)
        self._mouseMovePos = globalpos
