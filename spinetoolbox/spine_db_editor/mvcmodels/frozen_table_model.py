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
Contains FrozenTableModel class.

:author: P. Vennström (VTT)
:date:   24.9.2019
"""

from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel


class FrozenTableModel(QAbstractItemModel):
    """Used by custom_qtableview.FrozenTableView"""

    def __init__(self, parent, headers=None, data=None):
        """
        Args:
            parent (TabularViewMixin)
        """
        super().__init__()
        self._parent = parent
        self.db_mngr = parent.db_mngr
        if headers is None:
            headers = []
        if data is None:
            data = []
        self._data = data
        self._headers = headers

    def parent(self, child=None):
        return QModelIndex()

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, parent)

    def reset_model(self, data, headers):
        if data and len(data[0]) != len(headers):
            raise ValueError("'data[0]' must be same length as 'headers'")
        self._headers = list(headers)
        data = [self._headers] + data
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def clear_model(self):
        self._headers = []
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self._headers)

    def row(self, index):
        if index.isValid():
            return self._data[index.row()]

    def data(self, index, role):
        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
            return
        header_id = self._data[index.row()][index.column()]
        if index.row() == 0:
            return header_id
        index_id = self._data[0][index.column()]
        if index_id == "parameter":
            db_map, id_ = header_id
            item = self.db_mngr.get_item(db_map, "parameter_definition", id_)
            name = item.get("parameter_name")
        elif index_id == "alternative":
            db_map, id_ = header_id
            item = self.db_mngr.get_item(db_map, "alternative", id_)
            name = item.get("name")
        elif index_id == "index":
            _, index = header_id
            item = {}
            name = str(index)
        elif index_id == "database":
            item = {}
            name = header_id.codename
        else:
            db_map, id_ = header_id
            item = self.db_mngr.get_item(db_map, "object", id_)
            name = item.get("name")
        if role == Qt.ItemDataRole.DisplayRole:
            return name
        description = item.get("description")
        if description in (None, ""):
            description = name
        return description

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return None
        return super().headerData(section, orientation, role=role)

    @property
    def headers(self):
        return self._headers
