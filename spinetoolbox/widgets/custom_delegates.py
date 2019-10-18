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
Custom item delegates.

:author: M. Marin (KTH)
:date:   1.9.2018
"""

from PySide2.QtCore import Qt, Signal, QEvent, QPoint, QRect
from PySide2.QtWidgets import QComboBox, QItemDelegate, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox
from PySide2.QtGui import QIcon
from spinedb_api import from_database, DateTime, Duration, ParameterValueFormatError, TimePattern, TimeSeries
from .custom_editors import (
    CustomComboEditor,
    CustomLineEditor,
    SearchBarEditor,
    MultiSearchBarEditor,
    CheckListEditor,
    NumberParameterInlineEditor,
)


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent, choices):
        super().__init__(parent)
        self.editor = None
        self.items = choices

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.addItems(self.items)
        # self.editor.currentIndexChanged.connect(self.currentItemChanged)
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        style = QApplication.style()
        opt = QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
        QItemDelegate.paint(self, painter, option, index)

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def currentItemChanged(self):
        self.commitData.emit(self.sender())


class LineEditDelegate(QItemDelegate):
    """A delegate that places a fully functioning QLineEdit.

    Attributes:
        parent (QMainWindow): either data store or spine datapackage widget
    """

    data_committed = Signal("QModelIndex", "QVariant", name="data_committed")

    def createEditor(self, parent, option, index):
        """Return CustomLineEditor. Set up a validator depending on datatype."""
        return CustomLineEditor(parent)

    def setEditorData(self, editor, index):
        """Init the line editor with previous data from the index."""
        editor.set_data(index.data(Qt.EditRole))

    def setModelData(self, editor, model, index):
        """Send signal."""
        self.data_committed.emit(index, editor.data())


class CheckBoxDelegate(QItemDelegate):
    """A delegate that places a fully functioning QCheckBox.

    Attributes:
        parent (QMainWindow): either toolbox or spine datapackage widget
        centered (bool): whether or not the checkbox should be center-aligned in the widget
    """

    data_committed = Signal("QModelIndex", name="data_committed")

    def __init__(self, parent, centered=True):
        super().__init__(parent)
        self._centered = centered
        self.mouse_press_point = QPoint()

    def createEditor(self, parent, option, index):
        """Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model."""
        return None

    def paint(self, painter, option, index):
        """Paint a checkbox without the label."""
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        checkbox_style_option = QStyleOptionButton()
        if (index.flags() & Qt.ItemIsEditable) > 0:
            checkbox_style_option.state |= QStyle.State_Enabled
        else:
            checkbox_style_option.state |= QStyle.State_ReadOnly
        checked = index.data()
        if checked is None:
            checkbox_style_option.state |= QStyle.State_NoChange
        elif checked:
            checkbox_style_option.state |= QStyle.State_On
        else:
            checkbox_style_option.state |= QStyle.State_Off
        checkbox_style_option.rect = self.get_checkbox_rect(option)
        # noinspection PyArgumentList
        QApplication.style().drawControl(QStyle.CE_CheckBox, checkbox_style_option, painter)

    def editorEvent(self, event, model, option, index):
        """Change the data in the model and the state of the checkbox
        when user presses left mouse button and this cell is editable.
        Otherwise do nothing."""
        if not (index.flags() & Qt.ItemIsEditable) > 0:
            return False
        # Do nothing on double-click
        if event.type() == QEvent.MouseButtonDblClick:
            return True
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton and self.get_checkbox_rect(option).contains(event.pos()):
                self.mouse_press_point = event.pos()
                return True
        if event.type() == QEvent.MouseButtonRelease:
            checkbox_rect = self.get_checkbox_rect(option)
            if checkbox_rect.contains(self.mouse_press_point) and checkbox_rect.contains(event.pos()):
                # Change the checkbox-state
                self.data_committed.emit(index)
                self.mouse_press_point = QPoint()
                return True
            self.mouse_press_point = QPoint()
        return False

    def setModelData(self, editor, model, index):
        """Do nothing. Model data is updated by handling the `data_committed` signal."""

    def get_checkbox_rect(self, option):
        checkbox_style_option = QStyleOptionButton()
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, checkbox_style_option, None)
        if self._centered:
            checkbox_anchor = QPoint(
                option.rect.x() + option.rect.width() / 2 - checkbox_rect.width() / 2,
                option.rect.y() + option.rect.height() / 2 - checkbox_rect.height() / 2,
            )
        else:
            checkbox_anchor = QPoint(
                option.rect.x() + checkbox_rect.width() / 2, option.rect.y() + checkbox_rect.height() / 2
            )
        return QRect(checkbox_anchor, checkbox_rect.size())


class ParameterDelegate(QItemDelegate):
    """Base class for all custom parameter delegates.

    Attributes:
        parent (DataStoreForm): tree or graph view form
    """

    data_committed = Signal("QModelIndex", "QVariant", name="data_committed")
    parameter_value_editor_requested = Signal("QModelIndex", "QVariant", name="parameter_value_editor_requested")

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

    def setModelData(self, editor, model, index):
        """Send signal."""
        self.data_committed.emit(index, editor.data())

    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)
        if isinstance(editor, (SearchBarEditor, CheckListEditor, MultiSearchBarEditor)):
            size = option.rect.size()
            if index.data(Qt.DecorationRole):
                size.setWidth(size.width() - 22)  # FIXME
            editor.set_base_size(size)
            editor.update_geometry()

    def _connect_editor_signals(self, editor, index):
        """Connect editor signals if necessary.
        """
        if isinstance(editor, SearchBarEditor):
            model = index.model()
            editor.data_committed.connect(lambda e=editor, i=index, m=model: self._close_editor(e, i, m))

    def _close_editor(self, editor, index, model):
        self.closeEditor.emit(editor)
        self.setModelData(editor, model, index)

    def _create_database_editor(self, parent, option, index, db_mngr):
        editor = SearchBarEditor(self._parent, parent)
        editor.set_data(index.data(Qt.DisplayRole), [x.codename for x in db_mngr.db_maps])
        return editor

    def _create_line_editor(self, parent, option, index):
        editor = CustomLineEditor(parent)
        editor.set_data(index.data(Qt.EditRole))
        return editor

    def _create_parameter_value_editor(self, parent, option, index, db_mngr, db_map):
        """Returns a SearchBarEditor if the parameter has associated a value list.
        Otherwise returns the normal parameter value editor.
        """
        # TODO: get the parameter definition id in empty models
        id_ = model.item_at_row(index.row())
        parameter_id = db_mngr.get_item(db_map, "parameter value", id_).get("parameter_id")
        value_list_id = db_mngr.get_item(db_map, "parameter definition", parameter_id).get("value_list_id")
        value_list = db_mngr.get_item(db_map, "parameter value list", value_list_id).get("value_list")
        if value_list:
            editor = SearchBarEditor(self._parent, parent, is_json=True)
            value_list = value_list.split(",")
            editor.set_data(index.data(Qt.DisplayRole), value_list)
        else:
            editor = self._create_normal_parameter_value_editor(parent, option, index, db_mngr, db_map)
        return editor

    def _create_normal_parameter_value_editor(self, parent, option, index, db_mngr, db_map):
        """Returns a CustomLineEditor or NumberParameterInlineEditor if the data from index is not of special type.
        Otherwise, emit the signal to request a standalone `ParameterValueEditor`
        from parent widget.
        """
        try:
            value = from_database(index.data(role=Qt.EditRole))
        except ParameterValueFormatError:
            value = None
        if isinstance(value, (DateTime, Duration, TimePattern, TimeSeries)):
            self.parameter_value_editor_requested.emit(index, value)
            return None
        if isinstance(value, (float, int)):
            editor = NumberParameterInlineEditor(parent)
        else:
            editor = CustomLineEditor(parent)
        editor.set_data(index.data(Qt.EditRole))
        return editor

    def _create_entity_class_name_editor(self, parent, option, index, db_mngr, db_map):
        editor = SearchBarEditor(self._parent, parent)
        entity_classes = self._get_entity_classes(db_mngr, db_map)
        editor.set_data(index.data(Qt.EditRole), [x["name"] for x in entity_classes])
        return editor

    def _entity_class_query(self, db_map):
        raise NotImplementedError()

    def createEditor(self, parent, option, index):
        """Return editor."""
        model = index.model()
        header = model.horizontal_header_labels()
        db_mngr = model.db_mngr
        field = header[index.column()]
        if field == 'database':
            editor = self._create_database_editor(parent, option, index, db_mngr)
        else:
            database = index.sibling(index.row(), header.index("database")).data()
            db_map = next(iter(x for x in db_mngr.db_maps if x.codename == database), None)
            if not db_map:
                self._parent.msg.emit("Please select database first.")
                return None
            create_editor_func = self._create_editor_func_map.get(field)
            if create_editor_func:
                editor = create_editor_func(parent, option, index, db_mngr, db_map)
            else:
                editor = self._create_line_editor(parent, option, index)
        self._connect_editor_signals(editor, index)
        return editor


class ParameterDefinitionDelegateMixin:
    def _create_parameter_tag_list_editor(self, parent, option, index, db_mngr, db_map):
        editor = CheckListEditor(self._parent, parent)
        all_parameter_tag_list = [x["tag"] for x in db_mngr.get_parameter_tags(db_map)]
        try:
            parameter_tag_list = index.data(Qt.EditRole).split(",")
        except AttributeError:
            # Gibberish in the cell
            parameter_tag_list = []
        editor.set_data(all_parameter_tag_list, parameter_tag_list)
        return editor

    def _create_value_list_name_editor(self, parent, option, index, db_mngr, db_map):
        editor = SearchBarEditor(self._parent, parent)
        name_list = [x["name"] for x in db_mngr.get_parameter_value_lists(db_map)]
        editor.set_data(index.data(Qt.EditRole), name_list)
        return editor


class ParameterValueDelegateMixin:
    def _create_parameter_name_editor(self, parent, option, index, db_mngr, db_map):
        editor = SearchBarEditor(self._parent, parent)
        parameter_definition_list = self._parameter_definition_query(db_map, item.entity_class.id)
        name_list = [x.parameter_name for x in parameter_definition_list]
        editor.set_data(index.data(Qt.EditRole), name_list)
        return editor

    def _parameter_definition_query(self, db_map, entity_class_id):
        raise NotImplementedError()


class ObjectParameterDefinitionDelegate(ParameterDefinitionDelegateMixin, ParameterDelegate):
    """An object parameter definition delegate."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_editor_func_map = {
            "database": self._create_database_editor,
            "object_class_name": self._create_entity_class_name_editor,
            "parameter_tag_list": self._create_parameter_tag_list_editor,
            "value_list_name": self._create_value_list_name_editor,
            "default_value": self._create_normal_parameter_value_editor,
        }

    @staticmethod
    def _get_entity_classes(db_mngr, db_map):
        return db_mngr.get_object_classes(db_map)


class ObjectParameterValueDelegate(ParameterValueDelegateMixin, ParameterDelegate):
    """An object parameter value delegate."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_editor_func_map = {
            "database": self._create_database_editor,
            "object_class_name": self._create_entity_class_name_editor,
            "object_name": self._create_object_name_editor,
            "parameter_name": self._create_parameter_name_editor,
            "value": self._create_parameter_value_editor,
        }

    def _create_object_name_editor(self, parent, option, index, db_mngr, db_map):
        editor = SearchBarEditor(self._parent, parent)
        object_class_id = item.object_class_id
        name_list = [x.name for x in db_map.object_list(class_id=object_class_id)]
        editor.set_data(index.data(Qt.EditRole), name_list)
        return editor

    @staticmethod
    def _get_entity_classes(db_mngr, db_map):
        return db_mngr.get_object_classes(db_map)

    def _parameter_definition_query(self, db_map, entity_class_id):
        return db_map.object_parameter_definition_list(object_class_id=entity_class_id)


class RelationshipParameterDefinitionDelegate(ParameterDefinitionDelegateMixin, ParameterDelegate):
    """A relationship parameter definition delegate."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_editor_func_map = {
            "database": self._create_database_editor,
            "relationship_class_name": self._create_entity_class_name_editor,
            "object_class_name_list": lambda *args: None,
            "parameter_tag_list": self._create_parameter_tag_list_editor,
            "value_list_name": self._create_value_list_name_editor,
            "default_value": self._create_normal_parameter_value_editor,
        }

    @staticmethod
    def _get_entity_classes(db_mngr, db_map):
        return db_mngr.get_relationship_classes(db_map)


class RelationshipParameterValueDelegate(ParameterValueDelegateMixin, ParameterDelegate):
    """A relationship parameter definition delegate."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_editor_func_map = {
            "database": self._create_database_editor,
            "relationship_class_name": self._create_entity_class_name_editor,
            "object_name_list": self._create_object_name_list_editor,
            "parameter_name": self._create_parameter_name_editor,
            "value": self._create_parameter_value_editor,
        }

    def _create_object_name_list_editor(self, parent, option, index, db_mngr, db_map, id_):
        object_class_id_list = item.object_class_id_list
        if not object_class_id_list:
            editor = CustomLineEditor(parent)
            editor.set_data(index.data(Qt.EditRole))
        else:
            editor = MultiSearchBarEditor(self._parent, parent)
            object_class_ids = [int(x) for x in object_class_id_list.split(',')]
            object_class_dict = {x.id: x.name for x in db_map.object_class_list(id_list=object_class_ids)}
            object_class_names = [object_class_dict[x] for x in object_class_ids]
            object_name_list = index.data(Qt.EditRole)
            current_object_names = object_name_list.split(",") if object_name_list else []
            all_object_names_list = list()
            for class_id in object_class_ids:
                all_object_names_list.append([x.name for x in db_map.object_list(class_id=class_id)])
            editor.set_data(object_class_names, current_object_names, all_object_names_list)
        return editor

    @staticmethod
    def _get_entity_classes(db_mngr, db_map):
        return db_mngr.get_relationship_classes(db_map)

    def _parameter_definition_query(self, db_map, entity_class_id):
        return db_map.relationship_parameter_definition_list(relationship_class_id=entity_class_id)


class ManageItemsDelegate(QItemDelegate):
    """A custom delegate for the model in {Add/Edit}ItemDialogs.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    data_committed = Signal("QModelIndex", "QVariant", name="data_committed")

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

    def setModelData(self, editor, model, index):
        """Send signal."""
        self.data_committed.emit(index, editor.data())

    def close_editor(self, editor, index, model):
        self.closeEditor.emit(editor)
        self.setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        super().updateEditorGeometry(editor, option, index)
        if isinstance(editor, (SearchBarEditor, CheckListEditor)):
            size = option.rect.size()
            if index.data(Qt.DecorationRole):
                size.setWidth(size.width() - 22)  # FIXME
            editor.set_base_size(size)
            editor.update_geometry()

    def connect_editor_signals(self, editor, index):
        """Connect editor signals if necessary.
        """
        if isinstance(editor, SearchBarEditor):
            model = index.model()
            editor.data_committed.connect(lambda e=editor, i=index, m=model: self.close_editor(e, i, m))

    def _create_database_editor(self, parent, option, index):
        editor = CheckListEditor(parent)
        all_databases = self._parent.all_databases(index.row())
        databases = index.data(Qt.DisplayRole).split(",")
        editor.set_data(all_databases, databases)
        return editor


class ManageObjectClassesDelegate(ManageItemsDelegate):
    """A delegate for the model and view in {Add/Edit}ObjectClassesDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    icon_color_editor_requested = Signal("QModelIndex", name="icon_color_editor_requested")

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'display icon':
            self.icon_color_editor_requested.emit(index)
            editor = None
        elif header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
        else:
            editor = CustomLineEditor(parent)
            editor.set_data(index.data(Qt.EditRole))
        self.connect_editor_signals(editor, index)
        return editor

    def paint(self, painter, option, index):
        """Get a pixmap from the index data and paint it in the middle of the cell."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'display icon':
            pixmap = self._parent.icon_mngr.create_object_pixmap(index.data(Qt.DisplayRole))
            icon = QIcon(pixmap)
            icon.paint(painter, option.rect, Qt.AlignVCenter | Qt.AlignHCenter)
        else:
            super().paint(painter, option, index)


class ManageObjectsDelegate(ManageItemsDelegate):
    """A delegate for the model and view in {Add/Edit}ObjectsDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'object class name':
            editor = SearchBarEditor(parent)
            object_class_name_list = self._parent.object_class_name_list(index.row())
            editor.set_data(index.data(Qt.EditRole), object_class_name_list)
        elif header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
        else:
            editor = CustomLineEditor(parent)
            editor.set_data(index.data(Qt.EditRole))
        self.connect_editor_signals(editor, index)
        return editor


class ManageRelationshipClassesDelegate(ManageItemsDelegate):
    """A delegate for the model and view in {Add/Edit}RelationshipClassesDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'relationship class name':
            editor = CustomLineEditor(parent)
            editor.set_data(index.data(Qt.EditRole))
        elif header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
        else:
            editor = SearchBarEditor(parent)
            object_class_name_list = self._parent.object_class_name_list(index.row())
            editor.set_data(index.data(Qt.EditRole), object_class_name_list)
        self.connect_editor_signals(editor, index)
        return editor


class ManageRelationshipsDelegate(ManageItemsDelegate):
    """A delegate for the model and view in {Add/Edit}RelationshipsDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'relationship name':
            editor = CustomLineEditor(parent)
            data = index.data(Qt.EditRole)
            editor.set_data(data)
        elif header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
        else:
            editor = SearchBarEditor(parent)
            object_name_list = self._parent.object_name_list(index.row(), index.column())
            editor.set_data(index.data(Qt.EditRole), object_name_list)
        self.connect_editor_signals(editor, index)
        return editor


class RemoveTreeItemsDelegate(ManageItemsDelegate):
    """A delegate for the model and view in RemoveTreeItemsDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
            self.connect_editor_signals(editor, index)
            return editor


class ManageParameterTagsDelegate(ManageItemsDelegate):
    """A delegate for the model and view in ManageParameterTagsDialog.

    Attributes:
        parent (ManageItemsDialog): parent dialog
    """

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'remove':
            return None
        if header[index.column()] == 'databases':
            editor = self._create_database_editor(parent, option, index)
        else:
            editor = CustomLineEditor(parent)
            editor.set_data(index.data(Qt.EditRole))
        self.connect_editor_signals(editor, index)
        return editor


class ForeignKeysDelegate(QItemDelegate):
    """A QComboBox delegate with checkboxes.

    Attributes:
        parent (SpineDatapackageWidget): spine datapackage widget
    """

    data_committed = Signal("QModelIndex", "QVariant", name="data_committed")

    def close_field_name_list_editor(self, editor, index, model):
        self.closeEditor.emit(editor)
        self.data_committed.emit(index, editor.data())

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.datapackage = None
        self.selected_resource_name = None

    def createEditor(self, parent, option, index):
        """Return editor."""
        header = index.model().horizontal_header_labels()
        if header[index.column()] == 'fields':
            editor = CheckListEditor(self._parent, parent)
            model = index.model()
            editor.data_committed.connect(lambda e=editor, i=index, m=model: self.close_field_name_list_editor(e, i, m))
            return editor
        if header[index.column()] == 'reference resource':
            return CustomComboEditor(parent)
        if header[index.column()] == 'reference fields':
            editor = CheckListEditor(self._parent, parent)
            model = index.model()
            editor.data_committed.connect(lambda e=editor, i=index, m=model: self.close_field_name_list_editor(e, i, m))
            return editor
        return None

    def setEditorData(self, editor, index):
        """Set editor data."""
        self.datapackage = self._parent.datapackage
        self.selected_resource_name = self._parent.selected_resource_name
        header = index.model().horizontal_header_labels()
        h = header.index
        if header[index.column()] == 'fields':
            current_field_names = index.data(Qt.DisplayRole).split(',') if index.data(Qt.DisplayRole) else []
            field_names = self.datapackage.get_resource(self.selected_resource_name).schema.field_names
            editor.set_data(field_names, current_field_names)
        elif header[index.column()] == 'reference resource':
            editor.set_data(index.data(Qt.EditRole), self.datapackage.resource_names)
        elif header[index.column()] == 'reference fields':
            current_field_names = index.data(Qt.DisplayRole).split(',') if index.data(Qt.DisplayRole) else []
            reference_resource_name = index.sibling(index.row(), h('reference resource')).data(Qt.DisplayRole)
            reference_resource = self.datapackage.get_resource(reference_resource_name)
            if not reference_resource:
                field_names = []
            else:
                field_names = reference_resource.schema.field_names
            editor.set_data(field_names, current_field_names)

    def setModelData(self, editor, model, index):
        """Send signal."""
        self.data_committed.emit(index, editor.data())
