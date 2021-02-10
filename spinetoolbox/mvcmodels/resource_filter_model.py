######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Contains ResourceFilterModel.

:author: M. Marin (KTH)
:date:   26.11.2020
"""

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem
from spinedb_api.filters.scenario_filter import SCENARIO_FILTER_TYPE
from spinedb_api.filters.tool_filter import TOOL_FILTER_TYPE


class FilterValueItem(QStandardItem):
    _db_url = None
    _item_type = None
    _filter_type = None
    _id = None


class ResourceFilterModel(QStandardItemModel):

    tree_built = Signal()
    _SELECT_ALL = "Select all"

    def __init__(self, link):
        """
        Args:
            link (Link)
            parent (QObject)
        """
        super().__init__()
        self._link = link
        self._root_items = {}

    def _add_leaves(self, db_url, filter_item, items, filter_type, item_type):
        value_items = []
        if not filter_item.rowCount() and items:
            select_all_item = FilterValueItem(self._SELECT_ALL)
            select_all_item._db_url = db_url
            select_all_item._item_type = item_type
            select_all_item._filter_type = filter_type
            value_items.append(select_all_item)
        for item in items:
            value_item = FilterValueItem()
            value_item._db_url = db_url
            value_item._id = item["id"]
            value_item._item_type = item_type
            value_item._filter_type = filter_type
            value_items.append(value_item)
        filter_item.appendRows(value_items)

    def _remove_leaves(self, filter_item, items, resource_label, filter_type):
        ids = {x["id"] for x in items}
        invalid_rows = [row for row in range(filter_item.rowCount()) if filter_item.child(row)._id in ids]
        for row in reversed(invalid_rows):
            filter_item.removeRow(row)
        current_ids = self._link.resource_filters.get(resource_label, {}).get(filter_type, [])
        for id_ in ids:
            try:
                current_ids.remove(id_)
            except ValueError:
                pass

    def receive_scenarios_added(self, db_map_data):
        for db_map, data in db_map_data.items():
            root_item = self._root_items.get(db_map.db_url)
            if not root_item:
                continue
            filter_item = root_item.child(0)
            self._add_leaves(db_map.db_url, filter_item, data, SCENARIO_FILTER_TYPE, "scenario")

    def receive_tools_added(self, db_map_data):
        for db_map, data in db_map_data.items():
            root_item = self._root_items.get(db_map.db_url)
            if not root_item:
                continue
            filter_item = root_item.child(1)
            self._add_leaves(db_map.db_url, filter_item, data, TOOL_FILTER_TYPE, "tool")

    def receive_scenarios_removed(self, db_map_data):
        for db_map, data in db_map_data.items():
            root_item = self._root_items.get(db_map.db_url)
            if not root_item:
                continue
            filter_item = root_item.child(0)
            self._remove_leaves(filter_item, data, root_item.text(), SCENARIO_FILTER_TYPE)

    def receive_tools_removed(self, db_map_data):
        for db_map, data in db_map_data.items():
            root_item = self._root_items.get(db_map.db_url)
            if not root_item:
                continue
            filter_item = root_item.child(1)
            self._remove_leaves(filter_item, data, root_item.text(), TOOL_FILTER_TYPE)

    def init_resources(self, resources):
        for resource in resources:
            root_item = self._root_items.get(resource.url)
            if root_item is not None:
                for row in range(root_item.rowCount()):
                    filter_item = root_item.child(row)
                    filter_item.removeRows(0, filter_item.rowCount())
                continue
            root_item = self._root_items[resource.url] = QStandardItem(resource.label)
            filter_items = [QStandardItem("Scenario filter"), QStandardItem("Tool filter")]
            root_item.appendRows(filter_items)
            self.appendRow(root_item)

    def remove_resources(self, urls):
        invalid_rows = []
        for url in urls:
            resource_item = self._root_items.pop(url, None)
            if resource_item is not None:
                invalid_rows.append(self.indexFromItem(resource_item).row())
        for row in sorted(invalid_rows, reverse=True):
            self.removeRow(row)

    def flags(self, index):  # pylint: disable=no-self-use
        return Qt.ItemIsEnabled

    def data(self, index, role=Qt.DisplayRole):
        item = self.itemFromIndex(index)
        if not isinstance(item, FilterValueItem):
            return super().data(index, role=role)
        if role == Qt.DisplayRole:
            if super().data(index) == self._SELECT_ALL:
                return self._SELECT_ALL
            db_map = self._link.db_mngr.db_map(item._db_url)
            return self._link.db_mngr.get_item(db_map, item._item_type, item._id).get("name")
        if role == Qt.CheckStateRole:
            resource_label = self._root_items[item._db_url].text()
            filter_type = item._filter_type
            ids = self._link.resource_filters.get(resource_label, {}).get(filter_type, [])
            if super().data(index) == self._SELECT_ALL:
                db_map = self._link.db_mngr.db_map(item._db_url)
                all_ids = self._link.db_mngr.get_items(db_map, item._item_type)
                return Qt.Checked if len(ids) == len(all_ids) > 0 else Qt.Unchecked
            return Qt.Checked if item._id in ids else Qt.Unchecked
        return super().data(index, role=role)

    def toggle_checked_state(self, index):
        """Toggles the checked state of the index if it's a leaf.
        This calls a method in the underlying Link object which in turn pushes a command to the undo stack...

        Args:
            QModelIndex
        """
        item = self.itemFromIndex(index)
        if not isinstance(item, FilterValueItem):
            return
        resource_label = self._root_items[item._db_url].text()
        filter_type = item._filter_type
        if super().data(index) == self._SELECT_ALL:
            ids = self._link.resource_filters.get(resource_label, {}).get(filter_type, [])
            if index.data(Qt.CheckStateRole) == Qt.Unchecked:
                db_map = self._link.db_mngr.db_map(item._db_url)
                all_ids = [x["id"] for x in self._link.db_mngr.get_items(db_map, item._item_type)]
                self._link.toggle_filter_ids(resource_label, filter_type, *(set(all_ids) - set(ids)))
            else:
                self._link.toggle_filter_ids(resource_label, filter_type, *ids)
            return
        self._link.toggle_filter_ids(resource_label, filter_type, item._id)

    def refresh_model(self):
        """Notifies changes in the model. Called by the underlying Link once changes are successfully done."""
        self.layoutChanged.emit()
