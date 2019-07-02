######################################################################################################################
# Copyright (C) 2017-2019 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
An editor widget for editing duration database (relationship) parameter values.

:author: A. Soininen (VTT)
:date:   28.6.2019
"""

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget
from spinedb_api import Duration, duration_to_relativedelta, ParameterValueFormatError, relativedelta_to_duration
from ui.duration_editor import Ui_DurationEditor


class _DurationModel:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = Duration(duration_to_relativedelta(value))


class DurationEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = _DurationModel(Duration(duration_to_relativedelta("1 hour")))
        self._ui = Ui_DurationEditor()
        self._ui.setupUi(self)
        self._ui.duration_edit.editingFinished.connect(self._change_duration)
        self._ui.duration_edit.setText(relativedelta_to_duration(self._model.value.value))

    @Slot(name="_change_duration")
    def _change_duration(self):
        try:
            self._model.value = self._ui.duration_edit.text()
        except ParameterValueFormatError:
            self._ui.duration_edit.setText(relativedelta_to_duration(self._model.value.value))
            return

    def set_value(self, value):
        self._model = _DurationModel(value)
        self._ui.duration_edit.setText(relativedelta_to_duration(value.value))

    def value(self):
        return self._model.value
