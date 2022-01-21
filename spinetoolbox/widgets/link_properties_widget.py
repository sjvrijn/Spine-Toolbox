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
Link properties widget.

:author: M. Marin (KTH)
:date:   27.11.2020
"""

from PySide2.QtCore import Slot
from .properties_widget import PropertiesWidgetBase
from ..project_commands import SetConnectionOptionsCommand


class LinkPropertiesWidget(PropertiesWidgetBase):
    """Widget for connection link properties."""

    def __init__(self, toolbox, base_color=None):
        """
        Args:
            toolbox (ToolboxUI): The toolbox instance where this widget should be embedded
        """
        from ..ui.link_properties import Ui_Form  # pylint: disable=import-outside-toplevel

        super().__init__(toolbox, base_color=base_color)
        self._connection = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.checkBox_use_datapackage.stateChanged.connect(self._handle_use_datapackage_state_changed)

    def set_link(self, connection):
        """Hooks the widget to given link, so that user actions are reflected in the link's filter configuration.

        Args:
            connection (LoggingConnection)
        """
        self._connection = connection
        self._connection.refresh_resource_filter_model()
        self.ui.treeView_filters.setModel(self._connection.resource_filter_model)
        self.ui.treeView_filters.expandAll()
        self._toolbox.label_item_name.setText(f"<b>Link {self._connection.link.name}</b>")
        self.load_connection_options()

    def unset_link(self):
        """Releases the widget from any links."""
        self.ui.treeView_filters.setModel(None)

    @Slot(int)
    def _handle_use_datapackage_state_changed(self, _state):
        checked = self.ui.checkBox_use_datapackage.isChecked()
        if self._connection.use_datapackage == checked:
            return
        options = {"use_datapackage": checked}
        self._toolbox.undo_stack.push(SetConnectionOptionsCommand(self._connection, options))

    def load_connection_options(self):
        self.ui.checkBox_use_datapackage.setChecked(self._connection.use_datapackage)
