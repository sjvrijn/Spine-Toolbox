######################################################################################################################
# Copyright (C) 2017-2020 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Classes for custom QGraphicsViews for the Entity graph view.

:authors: P. Savolainen (VTT), M. Marin (KTH)
:date:   6.2.2018
"""

from PySide2.QtCore import Qt, QTimeLine
from PySide2.QtWidgets import QMenu
from ...widgets.custom_qgraphicsviews import CustomQGraphicsView
from ..graphics_items import ObjectItem, RodObjectItem, RodArcItem


class EntityQGraphicsView(CustomQGraphicsView):
    """QGraphicsView for the Entity Graph View."""

    def __init__(self, parent):
        """

        Args:
            parent (QWidget): Graph View Form's (QMainWindow) central widget (self.centralwidget)
        """
        super().__init__(parent=parent)  # Parent is passed to QWidget's constructor
        self._data_store_form = None
        self._menu = QMenu(self)
        self._hovered_object_item = None
        self.link_item = None
        self.rod_items = []

    def set_rod_items(self, rod_items):
        self.rod_items = rod_items
        for item in rod_items:
            self.scene().addItem(item)
            item.apply_zoom(self.zoom_factor)
        rod_items[0].grabMouse()

    def clear_rod_items(self):
        for item in self.rod_items:
            item.hide()
            item.scene().removeItem(item)
        self.rod_items.clear()

    def connect_data_store_form(self, data_store_form):
        self._data_store_form = data_store_form
        self.create_context_menu()

    def create_context_menu(self):
        self._menu.addAction(self._data_store_form.ui.actionSave_positions)
        self._menu.addAction(self._data_store_form.ui.actionClear_positions)
        self._menu.addSeparator()
        self._menu.addAction(self._data_store_form.ui.actionHide_selected)
        self._menu.addAction(self._data_store_form.ui.actionShow_hidden)
        self._menu.addSeparator()
        self._menu.addAction(self._data_store_form.ui.actionPrune_selected_entities)
        self._menu.addAction(self._data_store_form.ui.actionPrune_selected_classes)
        self._menu.addMenu(self._data_store_form.ui.menuRestore_pruned)
        self._menu.addAction(self._data_store_form.ui.actionRestore_all_pruned)

    def edit_selected(self):
        """Edits selected items using the connected data store form."""
        self._data_store_form.edit_entity_graph_items()

    def remove_selected(self):
        """Removes selected items using the connected data store form."""
        self._data_store_form.remove_entity_graph_items()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.rod_items:
            return
        if not self._hovered_object_item:
            self.clear_rod_items()
            return
        if event.buttons() & Qt.RightButton:
            rod_rel_item = self.rod_items[1]
            rod_arc_item = RodArcItem(rod_rel_item, self._hovered_object_item, self._data_store_form._ARC_WIDTH)
            rod_rel_item.refresh_icon()
            self.scene().addItem(rod_arc_item)
            rod_arc_item.apply_zoom(self.zoom_factor)
            self.rod_items.append(rod_arc_item)
            self._data_store_form.msg.emit(
                "Successfuly added new member object '{0}'".format(self._hovered_object_item.entity_name)
            )
            return
        rod_obj_item, _, *rod_arc_items = self.rod_items
        obj_items = [arc_item.obj_item for arc_item in rod_arc_items]
        obj_items.remove(rod_obj_item)
        self.clear_rod_items()
        self._data_store_form.try_and_add_relationships(self._hovered_object_item, *obj_items)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self.rod_items:
            return
        obj_items = [
            x for x in self.items(event.pos()) if isinstance(x, ObjectItem) and not isinstance(x, RodObjectItem)
        ]
        self._hovered_object_item = next(iter(obj_items), None)
        if self._hovered_object_item is None:
            self.viewport().setCursor(Qt.ArrowCursor)
        else:
            self.viewport().setCursor(Qt.DragCopyCursor)

    def keyPressEvent(self, event):
        """Wipes this item out if user presses ESC."""
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape and self.rod_items:
            self.clear_rod_items()

    def contextMenuEvent(self, e):
        """Show context menu.

        Args:
            e (QContextMenuEvent): Context menu event
        """
        super().contextMenuEvent(e)
        if e.isAccepted():
            return
        e.accept()
        self._data_store_form._handle_menu_graph_about_to_show()
        self._menu.exec_(e.globalPos())

    def _zoom(self, factor):
        super()._zoom(factor)
        for item in self.items():
            if hasattr(item, "apply_zoom"):
                item.apply_zoom(self.zoom_factor)

    def wheelEvent(self, event):
        """Zooms in/out. If user has pressed the shift key, rotates instead.

        Args:
            event (QWheelEvent): Mouse wheel event
        """
        if event.modifiers() != Qt.ShiftModifier:
            super().wheelEvent(event)
            return
        if event.orientation() != Qt.Vertical:
            event.ignore()
            return
        event.accept()
        smooth_rotation = self._qsettings.value("appSettings/smoothRotation", defaultValue="false")
        if smooth_rotation == "true":
            num_degrees = event.delta() / 8
            num_steps = num_degrees / 15
            self._scheduled_transformations += num_steps
            if self._scheduled_transformations * num_steps < 0:
                self._scheduled_transformations = num_steps
            if self.time_line:
                self.time_line.deleteLater()
            self.time_line = QTimeLine(200, self)
            self.time_line.setUpdateInterval(20)
            self.time_line.valueChanged.connect(self._handle_rotation_time_line_advanced)
            self.time_line.finished.connect(self._handle_transformation_time_line_finished)
            self.time_line.start()
        else:
            angle = event.angleDelta().y() / 8
            self._rotate(angle)
            self._set_preferred_scene_rect()

    def _handle_rotation_time_line_advanced(self, pos):
        """Performs rotation whenever the smooth rotation time line advances."""
        angle = self._scheduled_transformations / 2.0
        self._rotate(angle)

    def _rotate(self, angle):
        center = self._get_viewport_scene_rect().center()
        for item in self.items():
            if hasattr(item, "apply_rotation"):
                item.apply_rotation(angle, center)

    def rotate_clockwise(self):
        """Performs a rotate clockwise with fixed angle."""
        self._rotate(-self._angle / 8)
        self._set_preferred_scene_rect()

    def rotate_anticlockwise(self):
        """Performs a rotate anticlockwise with fixed angle."""
        self._rotate(self._angle / 8)
        self._set_preferred_scene_rect()
