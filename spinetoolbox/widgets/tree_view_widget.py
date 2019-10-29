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
Contains the TreeViewForm class.

:author: M. Marin (KTH)
:date:   26.11.2018
"""

import os
import time  # just to measure loading time and sqlalchemy ORM performance
from PySide2.QtWidgets import QFileDialog, QDockWidget, QInputDialog, QTreeView, QTableView, QMessageBox, QDialog
from PySide2.QtCore import Qt, Signal, Slot
from spinedb_api import copy_database
from .data_store_widget import DataStoreForm
from .custom_menus import (
    EditableParameterValueContextMenu,
    ObjectTreeContextMenu,
    RelationshipTreeContextMenu,
    ParameterContextMenu,
    ParameterValueListContextMenu,
)
from .import_widget import ImportDialog
from .report_plotting_failure import report_plotting_failure
from .edit_db_items_dialogs import RemoveEntitiesDialog
from ..mvcmodels.entity_tree_models import ObjectTreeModel, RelationshipTreeModel
from ..excel_import_export import export_spine_database_to_xlsx
from ..helpers import busy_effect
from ..plotting import plot_selection, PlottingError, GraphAndTreeViewPlottingHints


class TreeViewForm(DataStoreForm):
    """
    A widget to show and edit Spine objects in a data store.

    Attributes:
        project (SpineToolboxProject): The project instance that owns this form
        db_maps (iter): DiffDatabaseMapping instances
    """

    object_class_selection_available = Signal("bool")
    object_selection_available = Signal("bool")
    relationship_class_selection_available = Signal("bool")
    relationship_selection_available = Signal("bool")
    object_tree_selection_available = Signal("bool")
    relationship_tree_selection_available = Signal("bool")
    obj_parameter_definition_selection_available = Signal("bool")
    obj_parameter_value_selection_available = Signal("bool")
    rel_parameter_definition_selection_available = Signal("bool")
    rel_parameter_value_selection_available = Signal("bool")
    parameter_value_list_selection_available = Signal("bool")

    def __init__(self, project, *db_maps):
        """Initialize class."""
        from ..ui.tree_view_form import Ui_MainWindow

        tic = time.process_time()
        super().__init__(project, Ui_MainWindow(), *db_maps)
        self.takeCentralWidget()
        # Object tree model
        self.object_tree_model = ObjectTreeModel(self, self.db_mngr, *db_maps)
        self.relationship_tree_model = RelationshipTreeModel(self, self.db_mngr, *db_maps)
        self.ui.treeView_object.setModel(self.object_tree_model)
        self.ui.treeView_relationship.setModel(self.relationship_tree_model)
        # Others
        self.widget_with_selection = None
        self.paste_to_widget = None
        self.settings_group = 'treeViewWidget'
        self._selection_being_accepted = False
        self.restore_dock_widgets()
        self.restore_ui()
        # init models
        self.init_models()
        self.setup_delegates()
        self.add_toggle_view_actions()
        self.connect_signals()
        self.setWindowTitle("Data store tree view    -- {} --".format(", ".join([x.codename for x in db_maps])))
        toc = time.process_time()
        self.msg.emit("Tree view form created in {} seconds".format(toc - tic))

    def add_toggle_view_actions(self):
        """Add toggle view actions to View menu."""
        self.ui.menuDock_Widgets.addAction(self.ui.dockWidget_relationship_tree.toggleViewAction())
        super().add_toggle_view_actions()

    def connect_signals(self):
        """Connect signals to slots."""
        super().connect_signals()
        qApp.focusChanged.connect(self.update_paste_action)  # pylint: disable=undefined-variable
        # Action availability
        self.object_class_selection_available.connect(self.ui.actionEdit_object_classes.setEnabled)
        self.object_selection_available.connect(self.ui.actionEdit_objects.setEnabled)
        self.relationship_class_selection_available.connect(self.ui.actionEdit_relationship_classes.setEnabled)
        self.relationship_selection_available.connect(self.ui.actionEdit_relationships.setEnabled)
        self.object_tree_selection_available.connect(self._handle_object_tree_selection_available)
        self.relationship_tree_selection_available.connect(self._handle_relationship_tree_selection_available)
        self.obj_parameter_definition_selection_available.connect(
            self._handle_obj_parameter_definition_selection_available
        )
        self.obj_parameter_value_selection_available.connect(self._handle_obj_parameter_value_selection_available)
        self.rel_parameter_definition_selection_available.connect(
            self._handle_rel_parameter_definition_selection_available
        )
        self.rel_parameter_value_selection_available.connect(self._handle_rel_parameter_value_selection_available)
        self.parameter_value_list_selection_available.connect(self._handle_parameter_value_list_selection_available)
        # Menu actions
        # Import export
        self.ui.actionImport.triggered.connect(self.show_import_file_dialog)
        self.ui.actionExport.triggered.connect(self.export_database)
        # Copy and paste
        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionPaste.triggered.connect(self.paste)
        # Add and edit object tree
        self.ui.actionAdd_object_classes.triggered.connect(self.show_add_object_classes_form)
        self.ui.actionAdd_objects.triggered.connect(self.show_add_objects_form)
        self.ui.actionAdd_relationship_classes.triggered.connect(self.show_add_relationship_classes_form)
        self.ui.actionAdd_relationships.triggered.connect(self.show_add_relationships_form)
        self.ui.actionEdit_object_classes.triggered.connect(self.show_edit_object_classes_form)
        self.ui.actionEdit_objects.triggered.connect(self.show_edit_objects_form)
        self.ui.actionEdit_relationship_classes.triggered.connect(self.show_edit_relationship_classes_form)
        self.ui.actionEdit_relationships.triggered.connect(self.show_edit_relationships_form)
        # Remove
        self.ui.actionRemove_selection.triggered.connect(self.remove_selection)
        self.object_tree_model.remove_selection_requested.connect(self.show_remove_object_tree_items_form)
        self.relationship_tree_model.remove_selection_requested.connect(self.show_remove_relationship_tree_items_form)
        self.object_parameter_definition_model.remove_selection_requested.connect(
            self.remove_object_parameter_definitions
        )
        self.object_parameter_value_model.remove_selection_requested.connect(self.remove_object_parameter_values)
        self.relationship_parameter_definition_model.remove_selection_requested.connect(
            self.remove_relationship_parameter_definitions
        )
        self.relationship_parameter_value_model.remove_selection_requested.connect(
            self.remove_relationship_parameter_values
        )
        self.parameter_value_list_model.remove_selection_requested.connect(self.remove_parameter_value_lists)
        # Dock Widgets
        self.ui.actionRestore_Dock_Widgets.triggered.connect(self.restore_dock_widgets)
        # Object tree misc
        self.ui.treeView_object.edit_key_pressed.connect(self.edit_object_tree_items)
        self.ui.treeView_object.customContextMenuRequested.connect(self.show_object_tree_context_menu)
        self.ui.treeView_object.doubleClicked.connect(self.find_next_relationship)
        # Relationship tree
        self.ui.treeView_relationship.selectionModel().selectionChanged.connect(
            self._handle_relationship_tree_selection_changed
        )
        self.ui.treeView_relationship.edit_key_pressed.connect(self.edit_relationship_tree_items)
        self.ui.treeView_relationship.customContextMenuRequested.connect(self.show_relationship_tree_context_menu)
        # Parameter tables selection changes
        self.ui.tableView_object_parameter_definition.selectionModel().selectionChanged.connect(
            self._handle_object_parameter_definition_selection_changed
        )
        self.ui.tableView_object_parameter_value.selectionModel().selectionChanged.connect(
            self._handle_object_parameter_value_selection_changed
        )
        self.ui.tableView_relationship_parameter_definition.selectionModel().selectionChanged.connect(
            self._handle_relationship_parameter_definition_selection_changed
        )
        self.ui.tableView_relationship_parameter_value.selectionModel().selectionChanged.connect(
            self._handle_relationship_parameter_value_selection_changed
        )
        # Parameter value_list tree selection changed
        self.ui.treeView_parameter_value_list.selectionModel().selectionChanged.connect(
            self._handle_parameter_value_list_selection_changed
        )
        # Parameter tables context menu requested
        self.ui.tableView_object_parameter_definition.customContextMenuRequested.connect(
            self.show_object_parameter_definition_context_menu
        )
        self.ui.tableView_object_parameter_value.customContextMenuRequested.connect(
            self.show_object_parameter_value_context_menu
        )
        self.ui.tableView_relationship_parameter_definition.customContextMenuRequested.connect(
            self.show_relationship_parameter_definition_context_menu
        )
        self.ui.tableView_relationship_parameter_value.customContextMenuRequested.connect(
            self.show_relationship_parameter_value_context_menu
        )
        # Parameter value_list context menu requested
        self.ui.treeView_parameter_value_list.customContextMenuRequested.connect(
            self.show_parameter_value_list_context_menu
        )

    @Slot("bool")
    def restore_dock_widgets(self, checked=False):
        """Dock all floating and or hidden QDockWidgets back to the window at 'factory' positions."""
        # Place docks
        for dock in self.findChildren(QDockWidget):
            dock.setVisible(True)
            dock.setFloating(False)
            self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.splitDockWidget(self.ui.dockWidget_object_tree, self.ui.dockWidget_object_parameter_value, Qt.Horizontal)
        # Split and tabify
        self.splitDockWidget(self.ui.dockWidget_object_tree, self.ui.dockWidget_relationship_tree, Qt.Vertical)
        self.splitDockWidget(
            self.ui.dockWidget_object_parameter_value, self.ui.dockWidget_parameter_value_list, Qt.Horizontal
        )
        self.splitDockWidget(
            self.ui.dockWidget_object_parameter_value, self.ui.dockWidget_relationship_parameter_value, Qt.Vertical
        )
        self.tabifyDockWidget(self.ui.dockWidget_object_parameter_value, self.ui.dockWidget_object_parameter_definition)
        self.tabifyDockWidget(
            self.ui.dockWidget_relationship_parameter_value, self.ui.dockWidget_relationship_parameter_definition
        )
        self.ui.dockWidget_object_parameter_value.raise_()
        self.ui.dockWidget_relationship_parameter_value.raise_()

    def update_copy_and_remove_actions(self):
        """Update copy and remove actions according to selections across the widgets."""
        if not self.widget_with_selection:
            self.ui.actionCopy.setEnabled(False)
            self.ui.actionRemove_selection.setEnabled(False)
        else:
            self.ui.actionCopy.setEnabled(True)
            self.ui.actionRemove_selection.setEnabled(True)
            self.ui.actionRemove_selection.setIcon(self.widget_with_selection.model().remove_icon)

    @Slot("bool")
    def _handle_object_tree_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.treeView_object
        elif self.ui.treeView_object == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_relationship_tree_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.treeView_relationship
        elif self.ui.treeView_relationship == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_obj_parameter_definition_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.tableView_object_parameter_definition
        elif self.ui.tableView_object_parameter_definition == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_obj_parameter_value_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.tableView_object_parameter_value
        elif self.ui.tableView_object_parameter_value == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_rel_parameter_definition_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.tableView_relationship_parameter_definition
        elif self.ui.tableView_relationship_parameter_definition == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_rel_parameter_value_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.tableView_relationship_parameter_value
        elif self.ui.tableView_relationship_parameter_value == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("bool")
    def _handle_parameter_value_list_selection_available(self, on):
        if on:
            self.widget_with_selection = self.ui.treeView_parameter_value_list
        elif self.ui.treeView_parameter_value_list == self.widget_with_selection:
            self.widget_with_selection = None
        self.update_copy_and_remove_actions()

    @Slot("QWidget", "QWidget")
    def update_paste_action(self, old, new):
        self.paste_to_widget = None
        self.ui.actionPaste.setEnabled(False)
        try:
            if new.canPaste():
                self.paste_to_widget = new
                self.ui.actionPaste.setEnabled(True)
        except AttributeError:
            pass

    @Slot("bool")
    def copy(self, checked=False):
        """Copy data to clipboard."""
        if not self.widget_with_selection:
            return
        self.widget_with_selection.copy()

    @Slot("bool")
    def paste(self, checked=False):
        """Paste data from clipboard."""
        if not self.paste_to_widget:
            return
        self.paste_to_widget.paste()

    @Slot("bool")
    def remove_selection(self, checked=False):
        """Remove selection of items."""
        if not self.widget_with_selection:
            return
        self.widget_with_selection.model().remove_selection_requested.emit()

    @Slot("QItemSelection", "QItemSelection")
    def _handle_object_parameter_definition_selection_changed(self, selected, deselected):
        """Enable/disable the option to remove rows."""
        model = self.ui.tableView_object_parameter_definition.selectionModel()
        self.obj_parameter_definition_selection_available.emit(model.hasSelection())
        self._accept_selection(self.ui.tableView_object_parameter_definition)

    @Slot("QItemSelection", "QItemSelection")
    def _handle_object_parameter_value_selection_changed(self, selected, deselected):
        """Enable/disable the option to remove rows."""
        model = self.ui.tableView_object_parameter_value.selectionModel()
        self.obj_parameter_value_selection_available.emit(model.hasSelection())
        self._accept_selection(self.ui.tableView_object_parameter_value)

    @Slot("QItemSelection", "QItemSelection")
    def _handle_relationship_parameter_definition_selection_changed(self, selected, deselected):
        """Enable/disable the option to remove rows."""
        model = self.ui.tableView_relationship_parameter_definition.selectionModel()
        self.rel_parameter_definition_selection_available.emit(model.hasSelection())
        self._accept_selection(self.ui.tableView_relationship_parameter_definition)

    @Slot("QItemSelection", "QItemSelection")
    def _handle_relationship_parameter_value_selection_changed(self, selected, deselected):
        """Enable/disable the option to remove rows."""
        model = self.ui.tableView_relationship_parameter_value.selectionModel()
        self.rel_parameter_value_selection_available.emit(model.hasSelection())
        self._accept_selection(self.ui.tableView_relationship_parameter_value)

    @Slot("QItemSelection", "QItemSelection")
    def _handle_parameter_value_list_selection_changed(self, selected, deselected):
        """Enable/disable the option to remove rows."""
        model = self.ui.treeView_parameter_value_list.selectionModel()
        self.parameter_value_list_selection_available.emit(model.hasSelection())
        self._accept_selection(self.ui.treeView_parameter_value_list)

    # TODO: nothing connected to these two below

    @Slot("int")
    def _handle_object_parameter_tab_changed(self, index):
        """Update filter."""
        if index == 0:
            self.object_parameter_value_model.update_filter()
        else:
            self.object_parameter_definition_model.update_filter()

    @Slot("int")
    def _handle_relationship_parameter_tab_changed(self, index):
        """Update filter."""
        if index == 0:
            self.relationship_parameter_value_model.update_filter()
        else:
            self.relationship_parameter_definition_model.update_filter()

    @Slot("bool")
    def show_import_file_dialog(self, checked=False):
        """Show dialog to allow user to select a file to import."""
        db_map = next(iter(self.db_maps))
        if db_map.has_pending_changes():
            commit_warning = QMessageBox(parent=self)
            commit_warning.setText("Please commit or rollback before importing data")
            commit_warning.setStandardButtons(QMessageBox.Ok)
            commit_warning.exec()
            return
        dialog = ImportDialog(parent=self)
        # assume that dialog is modal, if not use accepted, rejected signals
        if dialog.exec() == QDialog.Accepted:
            if db_map.has_pending_changes():
                self.msg.emit("Import was successful")
                self.commit_available.emit(True)
                self.init_models()

    @Slot("bool")
    def export_database(self, checked=False):
        """Exports a database to a file."""
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        db_map = self._select_database()
        if db_map is None:  # Database selection cancelled
            return
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export to file", self._project.project_dir, "Excel file (*.xlsx);;SQlite database (*.sqlite *.db)"
        )
        if not file_path:  # File selection cancelled
            return
        if selected_filter.startswith("SQlite"):
            self.export_to_sqlite(db_map, file_path)
        elif selected_filter.startswith("Excel"):
            self.export_to_excel(db_map, file_path)

    def _select_database(self):
        """
        Lets user select a database from available databases.

        Shows a dialog from which user can select a single database.
        If there is only a single database it is selected automatically and no dialog is shown.

        Returns:
             the database map of the database or None if no database was selected
        """
        if len(self.db_maps) == 1:
            return next(iter(self.db_maps))
        db_names = [x.codename for x in self.db_maps]
        selected_database, ok = QInputDialog.getItem(
            self, "Select database", "Select database to export", db_names, editable=False
        )
        if not ok:
            return None
        return self.db_maps[db_names.index(selected_database)]

    @busy_effect
    def export_to_excel(self, db_map, file_path):
        """Export data from database into Excel file."""
        filename = os.path.split(file_path)[1]
        try:
            export_spine_database_to_xlsx(db_map, file_path)
            self.msg.emit("Excel file successfully exported.")
        except PermissionError:
            self.msg_error.emit(
                "Unable to export to file <b>{0}</b>.<br/>" "Close the file in Excel and try again.".format(filename)
            )
        except OSError:
            self.msg_error.emit("[OSError] Unable to export to file <b>{0}</b>".format(filename))

    @busy_effect
    def export_to_sqlite(self, db_map, file_path):
        """Export data from database into SQlite file."""
        dst_url = 'sqlite:///{0}'.format(file_path)
        copy_database(dst_url, db_map, overwrite=True)
        self.msg.emit("SQlite file successfully exported.")

    def init_models(self):
        """Initialize models."""
        super().init_models()
        self.init_relationship_tree_model()

    def init_object_tree_model(self):
        """Initialize object tree model."""
        super().init_object_tree_model()
        self.ui.actionExport.setEnabled(self.object_tree_model.root_item.has_children())

    def init_relationship_tree_model(self):
        """Initialize relationship tree model."""
        self.relationship_tree_model.build_tree()
        self.ui.treeView_relationship.expand(self.relationship_tree_model.root_index)
        self.ui.treeView_relationship.resizeColumnToContents(0)

    @Slot("QModelIndex")
    def find_next_relationship(self, index):
        """Expand next occurrence of a relationship in object tree."""
        next_index = self.object_tree_model.find_next_relationship_index(index)
        if not next_index:
            return
        self.ui.treeView_object.setCurrentIndex(next_index)
        self.ui.treeView_object.scrollTo(next_index)
        self.ui.treeView_object.expand(next_index)

    def _accept_selection(self, widget):
        """Accept the selection from given widget, which means clearing all others."""
        if not self._selection_being_accepted:
            self._selection_being_accepted = True
            for w in self.findChildren(QTreeView) + self.findChildren(QTableView):
                if w != widget:
                    w.selectionModel().clearSelection()
            self._selection_being_accepted = False
            return True
        return False

    @Slot("QItemSelection", "QItemSelection")
    def _handle_object_tree_selection_changed(self, selected, deselected):
        """Called when the object tree selection changes.
        Set default rows and apply filters on parameter models."""
        super()._handle_object_tree_selection_changed(selected, deselected)
        if not self._accept_selection(self.ui.treeView_object):
            return
        self.object_tree_selection_available.emit(any(v for v in self.object_tree_model.selected_indexes.values()))
        self.object_class_selection_available.emit(bool(self.object_tree_model.selected_object_class_indexes))
        self.object_selection_available.emit(bool(self.object_tree_model.selected_object_indexes))
        self.relationship_class_selection_available.emit(
            bool(self.object_tree_model.selected_relationship_class_indexes)
        )
        self.relationship_selection_available.emit(bool(self.object_tree_model.selected_relationship_indexes))
        self.set_default_parameter_data(self.ui.treeView_object.currentIndex())
        self._update_object_filter()

    @Slot("QItemSelection", "QItemSelection")
    def _handle_relationship_tree_selection_changed(self, selected, deselected):
        """Called when the relationship tree selection changes.
        Set default rows and apply filters on parameter models."""
        for index in deselected.indexes():
            self.relationship_tree_model.deselect_index(index)
        for index in selected.indexes():
            self.relationship_tree_model.select_index(index)
        if not self._accept_selection(self.ui.treeView_relationship):
            return
        self.object_class_selection_available.emit(False)
        self.object_selection_available.emit(False)
        self.relationship_tree_selection_available.emit(
            any(v for v in self.relationship_tree_model.selected_indexes.values())
        )
        self.relationship_class_selection_available.emit(
            bool(self.relationship_tree_model.selected_relationship_class_indexes)
        )
        self.relationship_selection_available.emit(bool(self.relationship_tree_model.selected_relationship_indexes))
        self.set_default_parameter_data(self.ui.treeView_relationship.currentIndex())
        self._update_relationship_filter()

    @staticmethod
    def _db_map_items(indexes):
        d = dict()
        for index in indexes:
            item = index.model().item_from_index(index)
            for db_map in item.db_maps:
                d.setdefault(db_map, []).append(item.db_map_data(db_map))
        return d

    @staticmethod
    def _db_map_class_ids(db_map_data):
        d = dict()
        for db_map, items in db_map_data.items():
            for item in items:
                d.setdefault((db_map, item["class_id"]), set()).add(item["id"])
        return d

    @staticmethod
    def _merge_db_map_data(left, right):
        result = left.copy()
        for db_map, data in right.items():
            result.setdefault(db_map, []).extend(data)
        return result

    def _update_object_filter(self):
        """Update filters on parameter models according to object tree selection."""
        selected_object_classes = self._db_map_items(self.object_tree_model.selected_object_class_indexes)
        self.selected_ent_cls_ids["object class"] = self.db_mngr._to_ids(selected_object_classes)
        selected_relationship_classes = self._db_map_items(self.object_tree_model.selected_relationship_class_indexes)
        cascading_relationship_classes = self.db_mngr.find_cascading_relationship_classes(
            self.selected_ent_cls_ids["object class"]
        )
        selected_relationship_classes = self._merge_db_map_data(
            selected_relationship_classes, cascading_relationship_classes
        )
        self.selected_ent_cls_ids["relationship class"] = self.db_mngr._to_ids(selected_relationship_classes)
        selected_objects = self._db_map_items(self.object_tree_model.selected_object_indexes)
        selected_relationships = self._db_map_items(self.object_tree_model.selected_relationship_indexes)
        cascading_relationships = self.db_mngr.find_cascading_relationships(self.db_mngr._to_ids(selected_objects))
        selected_relationships = self._merge_db_map_data(selected_relationships, cascading_relationships)
        for db_map, items in selected_objects.items():
            self.selected_ent_cls_ids["object class"].setdefault(db_map, set()).update({x["class_id"] for x in items})
        for db_map, items in selected_relationships.items():
            self.selected_ent_cls_ids["relationship class"].setdefault(db_map, set()).update(
                {x["class_id"] for x in items}
            )
        self.selected_ent_ids["object"] = self._db_map_class_ids(selected_objects)
        self.selected_ent_ids["relationship"] = self._db_map_class_ids(selected_relationships)
        self.update_filter()

    def _update_relationship_filter(self):
        """Update filters on parameter models according to relationship tree selection."""
        selected_relationship_classes = self._db_map_items(
            self.relationship_tree_model.selected_relationship_class_indexes
        )
        self.selected_ent_cls_ids["relationship class"] = self.db_mngr._to_ids(selected_relationship_classes)
        selected_relationships = self._db_map_items(self.relationship_tree_model.selected_relationship_indexes)
        for db_map, items in selected_relationships.items():
            self.selected_ent_cls_ids["relationship class"].setdefault(db_map, set()).update(
                {x["class_id"] for x in items}
            )
        self.selected_ent_ids["relationship"] = self._db_map_class_ids(selected_relationships)
        self.update_filter()

    @Slot("QPoint")
    def show_object_tree_context_menu(self, pos):
        """Context menu for object tree.

        Args:
            pos (QPoint): Mouse position
        """
        index = self.ui.treeView_object.indexAt(pos)
        global_pos = self.ui.treeView_object.viewport().mapToGlobal(pos)
        object_tree_context_menu = ObjectTreeContextMenu(self, global_pos, index)
        option = object_tree_context_menu.get_action()
        if option == "Copy text":
            self.ui.treeView_object.copy()
        elif option == "Add object classes":
            self.show_add_object_classes_form()
        elif option == "Add objects":
            self.call_show_add_objects_form(index)
        elif option == "Add relationship classes":
            self.call_show_add_relationship_classes_form(index)
        elif option == "Add relationships":
            self.call_show_add_relationships_form(index)
        elif option == "Edit object classes":
            self.show_edit_object_classes_form()
        elif option == "Edit objects":
            self.show_edit_objects_form()
        elif option == "Edit relationship classes":
            self.show_edit_relationship_classes_form()
        elif option == "Edit relationships":
            self.show_edit_relationships_form()
        elif option == "Find next":
            self.find_next_relationship(index)
        elif option == "Remove selection":
            self.show_remove_object_tree_items_form()
        elif option == "Fully expand":
            self.fully_expand_selection()
        elif option == "Fully collapse":
            self.fully_collapse_selection()
        else:  # No option selected
            pass
        object_tree_context_menu.deleteLater()

    @Slot("QPoint")
    def show_relationship_tree_context_menu(self, pos):
        """Context menu for relationship tree.

        Args:
            pos (QPoint): Mouse position
        """
        index = self.ui.treeView_relationship.indexAt(pos)
        global_pos = self.ui.treeView_relationship.viewport().mapToGlobal(pos)
        relationship_tree_context_menu = RelationshipTreeContextMenu(self, global_pos, index)
        option = relationship_tree_context_menu.get_action()
        if option == "Copy text":
            self.ui.treeView_relationship.copy()
        elif option == "Add relationship classes":
            self.show_add_relationship_classes_form()
        elif option == "Add relationships":
            self.call_show_add_relationships_form(index)
        elif option == "Edit relationship classes":
            self.show_edit_relationship_classes_form()
        elif option == "Edit relationships":
            self.show_edit_relationships_form()
        elif option == "Remove selection":
            self.show_remove_relationship_tree_items_form()
        else:  # No option selected
            pass
        relationship_tree_context_menu.deleteLater()

    @busy_effect
    def fully_expand_selection(self):
        for index in self.ui.treeView_object.selectionModel().selectedIndexes():
            if index.column() != 0:
                continue
            for item in self.object_tree_model.visit_all(index):
                self.ui.treeView_object.expand(self.object_tree_model.index_from_item(item))

    @busy_effect
    def fully_collapse_selection(self):
        for index in self.ui.treeView_object.selectionModel().selectedIndexes():
            if index.column() != 0:
                continue
            for item in self.object_tree_model.visit_all(index):
                self.ui.treeView_object.collapse(self.object_tree_model.index_from_item(item))

    def call_show_add_objects_form(self, index):
        class_name = index.internalPointer().display_name
        self.show_add_objects_form(class_name=class_name)

    def call_show_add_relationship_classes_form(self, index):
        object_class_one_name = index.internalPointer().display_name
        self.show_add_relationship_classes_form(object_class_one_name=object_class_one_name)

    def call_show_add_relationships_form(self, index):
        item = index.internalPointer()
        relationship_class_key = item.display_id
        try:
            object_name = item._parent.display_name
            object_class_name = item._parent._parent.display_name
        except AttributeError:
            object_name = object_class_name = None
        self.show_add_relationships_form(
            relationship_class_key=relationship_class_key, object_class_name=object_class_name, object_name=object_name
        )

    @Slot("QModelIndex")
    def edit_object_tree_items(self, current):
        """Called when F2 is pressed while the object tree has focus.
        Call the appropriate method to show the edit form,
        depending on the current index."""
        current = self.ui.treeView_object.currentIndex()
        current_type = self.object_tree_model.item_from_index(current).item_type
        if current_type == 'object class':
            self.show_edit_object_classes_form()
        elif current_type == 'object':
            self.show_edit_objects_form()
        elif current_type == 'relationship class':
            self.show_edit_relationship_classes_form()
        elif current_type == 'relationship':
            self.show_edit_relationships_form()

    @Slot("QModelIndex")
    def edit_relationship_tree_items(self, current):
        """Called when F2 is pressed while the relationship tree has focus.
        Call the appropriate method to show the edit form,
        depending on the current index."""
        current = self.ui.treeView_relationship.currentIndex()
        current_type = self.relationship_tree_model.item_from_index(current).item_type
        if current_type == 'relationship class':
            self.show_edit_relationship_classes_form()
        elif current_type == 'relationship':
            self.show_edit_relationships_form()

    @Slot()
    def show_remove_object_tree_items_form(self):
        """Show form to remove items from object treeview."""
        selected = {
            item_type: [ind.model().item_from_index(ind) for ind in indexes]
            for item_type, indexes in self.object_tree_model.selected_indexes.items()
        }
        dialog = RemoveEntitiesDialog(self, self.db_mngr, selected)
        dialog.show()

    @Slot()
    def show_remove_relationship_tree_items_form(self):
        """Show form to remove items from relationship treeview."""
        selected = {
            item_type: [ind.model().item_from_index(ind) for ind in indexes]
            for item_type, indexes in self.relationship_tree_model.selected_indexes.items()
        }
        dialog = RemoveEntitiesDialog(self, self.db_mngr, selected)
        dialog.show()

    def notify_items_changed(self, action, item_type, db_map_data):
        """Enables or disables actions and informs the user about what just happened."""
        super().notify_items_changed(action, item_type, db_map_data)
        # NOTE: Make sure this slot is called after removing the items, so the next line works
        self.ui.actionExport.setEnabled(self.object_tree_model.root_item.has_children())
        if action == "removed":
            self.object_tree_selection_available.emit(any(v for v in self.object_tree_model.selected_indexes.values()))
            self.object_class_selection_available.emit(bool(self.object_tree_model.selected_object_class_indexes))
            self.object_selection_available.emit(bool(self.object_tree_model.selected_object_indexes))
            self.relationship_class_selection_available.emit(
                bool(self.object_tree_model.selected_relationship_class_indexes)
            )
            self.relationship_selection_available.emit(bool(self.object_tree_model.selected_relationship_indexes))

    @Slot("QPoint")
    def show_object_parameter_value_context_menu(self, pos):
        """Context menu for object parameter value table view.

        Args:
            pos (QPoint): Mouse position
        """
        self._show_parameter_context_menu(pos, self.ui.tableView_object_parameter_value, "value")

    @Slot("QPoint")
    def show_relationship_parameter_value_context_menu(self, pos):
        """Context menu for relationship parameter value table view.

        Args:
            pos (QPoint): Mouse position
        """
        self._show_parameter_context_menu(pos, self.ui.tableView_relationship_parameter_value, "value")

    @Slot("QPoint")
    def show_object_parameter_definition_context_menu(self, pos):
        """Context menu for object parameter table view.

        Args:
            pos (QPoint): Mouse position
        """
        self._show_parameter_context_menu(pos, self.ui.tableView_object_parameter_definition, "default_value")

    @Slot("QPoint")
    def show_relationship_parameter_definition_context_menu(self, pos):
        """Context menu for relationship parameter table view.

        Args:
            pos (QPoint): Mouse position
        """
        self._show_parameter_context_menu(pos, self.ui.tableView_relationship_parameter_definition, "default_value")

    def _show_parameter_context_menu(self, position, table_view, value_column_header):
        """
        Show a context menu for parameter tables.

        Args:
            position (QPoint): local mouse position in the table view
            table_view (QTableView): the table view where the context menu was triggered
            value_column_header (str): column header for editable/plottable values
        """
        index = table_view.indexAt(position)
        global_pos = table_view.mapToGlobal(position)
        model = table_view.model()
        flags = model.flags(index)
        editable = (flags & Qt.ItemIsEditable) == Qt.ItemIsEditable
        is_value = model.headerData(index.column(), Qt.Horizontal) == value_column_header
        if editable and is_value:
            menu = EditableParameterValueContextMenu(self, global_pos, index)
        else:
            menu = ParameterContextMenu(self, global_pos, index)
        option = menu.get_action()
        if option == "Open in editor...":
            self.show_parameter_value_editor(index, table_view)
        elif option == "Plot":
            selection = table_view.selectedIndexes()
            try:
                hints = GraphAndTreeViewPlottingHints(table_view)
                plot_widget = plot_selection(model, selection, hints)
            except PlottingError as error:
                report_plotting_failure(error, self)
                return
            if (
                table_view is self.ui.tableView_object_parameter_value
                or table_view is self.ui.tableView_object_parameter_definition
            ):
                plot_window_title = "Object parameter plot -- {} --".format(value_column_header)
            elif (
                table_view is self.ui.tableView_relationship_parameter_value
                or table_view is self.ui.tableView_relationship_parameter_definition
            ):
                plot_window_title = "Relationship parameter plot    -- {} --".format(value_column_header)
            else:
                plot_window_title = "Plot"
            plot_widget.setWindowTitle(plot_window_title)
            plot_widget.show()
        elif option == "Remove selection":
            table_view.model().remove_selection_requested.emit()
        elif option == "Copy":
            table_view.copy()
        elif option == "Paste":
            table_view.paste()
        menu.deleteLater()

    @Slot("QPoint")
    def show_parameter_value_list_context_menu(self, pos):
        """
        Context menu for relationship parameter table view.

        Args:
            pos (QPoint): Mouse position
        """
        index = self.ui.treeView_parameter_value_list.indexAt(pos)
        global_pos = self.ui.treeView_parameter_value_list.viewport().mapToGlobal(pos)
        parameter_value_list_context_menu = ParameterValueListContextMenu(self, global_pos, index)
        parameter_value_list_context_menu.deleteLater()
        option = parameter_value_list_context_menu.get_action()
        if option == "Copy":
            self.ui.treeView_parameter_value_list.copy()
        elif option == "Remove selection":
            self.remove_parameter_value_lists()
        parameter_value_list_context_menu.deleteLater()

    @Slot()
    def remove_object_parameter_values(self):
        """Remove selected rows from object parameter value table."""
        self._remove_parameter_data(self.ui.tableView_object_parameter_value, "parameter value")

    @Slot()
    def remove_relationship_parameter_values(self):
        """Remove selected rows from relationship parameter value table."""
        self._remove_parameter_data(self.ui.tableView_relationship_parameter_value, "parameter value")

    @Slot()
    def remove_object_parameter_definitions(self):
        """Remove selected rows from object parameter definition table."""
        self._remove_parameter_data(self.ui.tableView_object_parameter_definition, "parameter definition")

    @Slot()
    def remove_relationship_parameter_definitions(self):
        """Remove selected rows from relationship parameter definition table."""
        self._remove_parameter_data(self.ui.tableView_relationship_parameter_definition, "parameter definition")

    @busy_effect
    def _remove_parameter_data(self, table_view, item_type):
        """
        Remove selected rows from parameter table.

        Args:
            table_view (QTableView): remove selection from this view
            item_type (str)
        """
        selection = table_view.selectionModel().selection()
        rows = list()
        while not selection.isEmpty():
            current = selection.takeFirst()
            top = current.top()
            bottom = current.bottom()
            rows += range(top, bottom + 1)
        # Get parameter data grouped by db_map
        db_map_typed_data = dict()
        model = table_view.model()
        for row in sorted(rows, reverse=True):
            try:
                db_map = model.sub_model_at_row(row).db_map
            except AttributeError:
                # It's an empty model, just remove the row
                _, sub_row = model._row_map[row]
                model.empty_model.removeRow(sub_row)
            else:
                id_ = model.item_at_row(row)
                item = model.db_mngr.get_item(db_map, item_type, id_)
                db_map_typed_data.setdefault(db_map, {}).setdefault(item_type, []).append(item)
        self.db_mngr.remove_items(db_map_typed_data)
        table_view.selectionModel().clearSelection()

    @Slot()
    def remove_parameter_value_lists(self):
        """Remove selection of parameter value_lists.
        """
        db_map_typed_data_to_rm = {}
        db_map_data_to_upd = {}
        selected = [
            self.parameter_value_list_model.item_from_index(index)
            for index in self.ui.treeView_parameter_value_list.selectionModel().selectedIndexes()
        ]
        for db_item in self.parameter_value_list_model._invisible_root_item.children:
            db_map_typed_data_to_rm[db_item.db_map] = {"parameter value list": []}
            db_map_data_to_upd[db_item.db_map] = []
            for list_item in reversed(db_item.children[:-1]):
                if list_item.id:
                    if list_item in selected:
                        db_map_typed_data_to_rm[db_item.db_map]["parameter value list"].append(
                            {"id": list_item.id, "name": list_item.name}
                        )
                        continue
                    curr_value_list = list_item.compile_value_list()
                    value_list = [
                        value
                        for value_item, value in zip(list_item.children, curr_value_list)
                        if value_item not in selected
                    ]
                    if not value_list:
                        db_map_typed_data_to_rm[db_item.db_map]["parameter value list"].append(
                            {"id": list_item.id, "name": list_item.name}
                        )
                        continue
                    if value_list != curr_value_list:
                        item = {"id": list_item.id, "value_list": value_list}
                        db_map_data_to_upd[db_item.db_map].append(item)
                else:
                    # WIP lists, just remove everything selected
                    if list_item in selected:
                        db_item.remove_children(list_item.child_number(), list_item.child_number())
                        continue
                    for value_item in reversed(list_item.children[:-1]):
                        if value_item in selected:
                            list_item.remove_children(value_item.child_number(), value_item.child_number())
        self.db_mngr.update_parameter_value_lists(db_map_data_to_upd)
        self.db_mngr.remove_items(db_map_typed_data_to_rm)
        self.ui.treeView_parameter_value_list.selectionModel().clearSelection()
