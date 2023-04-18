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
Miscelaneous mixins for parameter models

:authors: M. Marin (KTH)
:date:   4.10.2019
"""

from spinedb_api.parameter_value import split_value_and_type


class ConvertToDBMixin:
    """Base class for all mixins that convert model items (name-based) into database items (id-based)."""

    def build_lookup_dictionary(self, db_map_data):
        """Begins an operation to convert items."""

    # pylint: disable=no-self-use
    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item = item.copy()
        value_field, type_field = {
            "parameter_value": ("value", "type"),
            "parameter_definition": ("default_value", "default_type"),
        }[self.item_type]
        if value_field in item:
            value, value_type = split_value_and_type(item[value_field])
            item[value_field] = value
            item[type_field] = value_type
        return item, []


class FillInAlternativeIdMixin(ConvertToDBMixin):
    """Fills in alternative names."""

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_alt_lookup = {}

    def build_lookup_dictionary(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping
        """
        super().build_lookup_dictionary(db_map_data)
        # Group data by name
        db_map_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                name = item.get("alternative_name")
                db_map_names.setdefault(db_map, set()).add(name)
        # Build lookup dict
        self._db_map_alt_lookup.clear()
        for db_map, names in db_map_names.items():
            for name in names:
                if item := self.db_mngr.get_item_by_field(
                    db_map, "alternative", "name", name, only_visible=False
                ):
                    self._db_map_alt_lookup.setdefault(db_map, {})[name] = item

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err = super()._convert_to_db(item, db_map)
        alt_name = item.pop("alternative_name", None)
        alt = self._db_map_alt_lookup.get(db_map, {}).get(alt_name)
        if not alt:
            return item, err + [f"Unknown alternative name {alt_name}"] if alt_name else err
        item["alternative_id"] = alt["id"]
        return item, err


class FillInParameterNameMixin(ConvertToDBMixin):
    """Fills in parameter names."""

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err = super()._convert_to_db(item, db_map)
        if name := item.pop("parameter_name", None):
            item["name"] = name
        return item, err


class FillInValueListIdMixin(ConvertToDBMixin):
    """Fills in value list ids."""

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_value_list_lookup = {}

    def build_lookup_dictionary(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping
        """
        super().build_lookup_dictionary(db_map_data)
        # Group data by name
        db_map_value_list_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                value_list_name = item.get("value_list_name")
                db_map_value_list_names.setdefault(db_map, set()).add(value_list_name)
        # Build lookup dict
        self._db_map_value_list_lookup.clear()
        for db_map, names in db_map_value_list_names.items():
            for name in names:
                if item := self.db_mngr.get_item_by_field(
                    db_map,
                    "parameter_value_list",
                    "name",
                    name,
                    only_visible=False,
                ):
                    self._db_map_value_list_lookup.setdefault(db_map, {})[name] = item

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._fill_in_value_list_id(item, db_map)
        return item, err1 + err2

    def _fill_in_value_list_id(self, item, db_map):
        """Fills in the value list id in the given db item.

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        if "value_list_name" not in item:
            return []
        if value_list_name := item.pop("value_list_name"):
            if value_list := self._db_map_value_list_lookup.get(db_map, {}).get(
                value_list_name
            ):
                item["parameter_value_list_id"] = value_list["id"]
            else:
                return [f"Unknown value list name {value_list_name}"] if value_list_name else []
        else:
            item["parameter_value_list_id"] = None
        return []


class FillInEntityClassIdMixin(ConvertToDBMixin):
    """Fills in entity_class ids."""

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_ent_cls_lookup = {}

    def build_lookup_dictionary(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping
        """
        super().build_lookup_dictionary(db_map_data)
        # Group data by name
        db_map_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                entity_class_name = item.get(self.entity_class_name_key)
                db_map_names.setdefault(db_map, set()).add(entity_class_name)
        # Build lookup dict
        self._db_map_ent_cls_lookup.clear()
        for db_map, names in db_map_names.items():
            for name in names:
                if item := self.db_mngr.get_item_by_field(
                    db_map,
                    self.entity_class_type,
                    "name",
                    name,
                    only_visible=False,
                ):
                    self._db_map_ent_cls_lookup.setdefault(db_map, {})[name] = item

    def _fill_in_entity_class_id(self, item, db_map):
        """Fills in the entity_class id in the given db item.

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        entity_class_name = item.pop(self.entity_class_name_key, None)
        entity_class = self._db_map_ent_cls_lookup.get(db_map, {}).get(entity_class_name)
        if not entity_class:
            return [f"Unknown entity_class {entity_class_name}"] if entity_class_name else []
        item[self.entity_class_id_key] = entity_class.get("id")
        return []

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._fill_in_entity_class_id(item, db_map)
        return item, err1 + err2


class FillInEntityIdsMixin(ConvertToDBMixin):
    """Fills in entity ids."""

    _add_entities_on_the_fly = False

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_ent_lookup = {}

    def build_lookup_dictionary(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping
        """
        super().build_lookup_dictionary(db_map_data)
        # Group data by name
        db_map_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                name = item.get(self.entity_name_key)
                db_map_names.setdefault(db_map, set()).add(name)
        # Build lookup dict
        self._db_map_ent_lookup.clear()
        for db_map, names in db_map_names.items():
            for name in names:
                if items := self.db_mngr.get_items_by_field(
                    db_map,
                    self.entity_type,
                    self.entity_name_key_in_cache,
                    name,
                    only_visible=False,
                ):
                    self._db_map_ent_lookup.setdefault(db_map, {})[name] = items

    def _fill_in_entity_ids(self, item, db_map):
        """Fills in all possible entity ids keyed by entity_class id in the given db item
        (as there can be more than one entity for the same name).

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        name = item.pop(self.entity_name_key, None)
        items = self._db_map_ent_lookup.get(db_map, {}).get(name)
        if not items:
            return [f"Unknown entity {name}"] if name and not self._add_entities_on_the_fly else []
        item["entity_ids"] = {x["class_id"]: x["id"] for x in items}
        return []

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._fill_in_entity_ids(item, db_map)
        return item, err1 + err2


class FillInParameterDefinitionIdsMixin(ConvertToDBMixin):
    """Fills in parameter_definition ids."""

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_param_lookup = {}

    def build_lookup_dictionary(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping
        """
        super().build_lookup_dictionary(db_map_data)
        # Group data by name
        db_map_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                name = item.get("parameter_name")
                db_map_names.setdefault(db_map, set()).add(name)
        # Build lookup dict
        self._db_map_param_lookup.clear()
        for db_map, names in db_map_names.items():
            for name in names:
                if items := [
                    x
                    for x in self.db_mngr.get_items_by_field(
                        db_map,
                        "parameter_definition",
                        "parameter_name",
                        name,
                        only_visible=False,
                    )
                    if self.entity_class_id_key in x
                ]:
                    self._db_map_param_lookup.setdefault(db_map, {})[name] = items

    def _fill_in_parameter_ids(self, item, db_map):
        """Fills in all possible parameter_definition ids keyed by entity_class id in the given db item
        (as there can be more than one parameter_definition for the same name).

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        name = item.pop("parameter_name", None)
        items = self._db_map_param_lookup.get(db_map, {}).get(name)
        if not items:
            return [f"Unknown parameter {name}"] if name else []
        item["parameter_ids"] = {x[self.entity_class_id_key]: x["id"] for x in items}
        return []

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._fill_in_parameter_ids(item, db_map)
        return item, err1 + err2


class InferEntityClassIdMixin(ConvertToDBMixin):
    """Infers entity class ids."""

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._infer_and_fill_in_entity_class_id(item, db_map)
        return item, err1 + err2

    def _infer_and_fill_in_entity_class_id(self, item, db_map):
        """Fills the entity_class id in the given db item, by intersecting entity ids and parameter ids.
        Then picks the correct entity id and parameter_definition id.
        Also sets the inferred entity_class name in the model.

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        row = item.pop("row")
        entity_ids = item.pop("entity_ids", {})
        parameter_ids = item.pop("parameter_ids", {})
        if self.entity_class_id_key not in item:
            if not entity_ids:
                entity_class_ids = set(parameter_ids.keys())
            elif not parameter_ids:
                entity_class_ids = set(entity_ids.keys())
            else:
                entity_class_ids = entity_ids.keys() & parameter_ids.keys()
            if len(entity_class_ids) != 1:
                # entity_class id not in the item and not inferrable, good bye
                return ["Unable to infer entity_class."]
            entity_class_id = entity_class_ids.pop()
            item[self.entity_class_id_key] = entity_class_id
            entity_class_name = self.db_mngr.get_item(
                db_map, self.entity_class_type, entity_class_id, only_visible=False
            )["name"]
            # TODO: Try to find a better place for this, and emit dataChanged
            self._main_data[row][self.header.index(self.entity_class_name_key)] = entity_class_name
        # At this point we're sure the entity_class_id is there
        entity_class_id = item[self.entity_class_id_key]
        entity_id = entity_ids.get(entity_class_id)
        parameter_definition_id = parameter_ids.get(entity_class_id)
        if entity_id:
            item[self.entity_id_key] = entity_id
        if parameter_definition_id:
            item["parameter_definition_id"] = parameter_definition_id
        return []


class ImposeEntityClassIdMixin(ConvertToDBMixin):
    """Imposes entity class ids."""

    def _convert_to_db(self, item, db_map):
        """Returns a db item (id-based) from the given model item (name-based).

        Args:
            item (dict): the model item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db item
            list: error log
        """
        item, err1 = super()._convert_to_db(item, db_map)
        err2 = self._impose_entity_class_id(item, db_map)
        return item, err1 + err2

    def _impose_entity_class_id(self, item, db_map):
        """Imposes the entity_class id from the model, to pick the correct entity id and parameter_definition id.

        Args:
            item (dict): the db item
            db_map (DiffDatabaseMapping): the database where the given item belongs

        Returns:
            list: error log
        """
        entity_ids = item.pop("entity_ids", {})
        parameter_ids = item.pop("parameter_ids", {})
        entity_id = entity_ids.get(self.entity_class_id)
        parameter_definition_id = parameter_ids.get(self.entity_class_id)
        if entity_id:
            item[self.entity_id_key] = entity_id
        if parameter_definition_id:
            item["parameter_definition_id"] = parameter_definition_id
        return []


class MakeRelationshipOnTheFlyMixin:
    """Makes relationships on the fly."""

    def __init__(self, *args, **kwargs):
        """Initializes lookup dicts."""
        super().__init__(*args, **kwargs)
        self._db_map_obj_lookup = {}
        self._db_map_rel_cls_lookup = {}
        self._db_map_existing_rels = {}

    @staticmethod
    def _make_unique_relationship_id(item):
        """Returns a unique name-based identifier for db relationships."""
        return (item["class_name"], item["object_name_list"])

    def build_lookup_dictionaries(self, db_map_data):
        """Builds a name lookup dictionary for the given data.

        Args:
            db_map_data (dict): lists of model items keyed by DiffDatabaseMapping.
        """
        # Group data by name
        db_map_object_names = {}
        db_map_rel_cls_names = {}
        for db_map, items in db_map_data.items():
            for item in items:
                if object_name_list := item.get("object_name_list"):
                    db_map_object_names.setdefault(db_map, set()).update(object_name_list)
                relationship_class_name = item.get("relationship_class_name")
                db_map_rel_cls_names.setdefault(db_map, set()).add(relationship_class_name)
        # Build lookup dicts
        self._db_map_obj_lookup.clear()
        for db_map, names in db_map_object_names.items():
            for name in names:
                if item := self.db_mngr.get_item_by_field(
                    db_map, "object", "name", name, only_visible=False
                ):
                    self._db_map_obj_lookup.setdefault(db_map, {})[name] = item
        self._db_map_rel_cls_lookup.clear()
        for db_map, names in db_map_rel_cls_names.items():
            for name in names:
                if item := self.db_mngr.get_item_by_field(
                    db_map, "relationship_class", "name", name, only_visible=False
                ):
                    self._db_map_rel_cls_lookup.setdefault(db_map, {})[name] = item
        self._db_map_existing_rels = {
            db_map: {
                self._make_unique_relationship_id(x)
                for x in self.db_mngr.get_items(db_map, "relationship", only_visible=False)
            }
            for db_map in self._db_map_obj_lookup.keys() | self._db_map_rel_cls_lookup.keys()
        }

    def _make_relationship_on_the_fly(self, item, db_map):
        """Returns a database relationship item (id-based) from the given model parameter_value item (name-based).

        Args:
            item (dict): the model parameter_value item
            db_map (DiffDatabaseMapping): the database where the resulting item belongs

        Returns:
            dict: the db relationship item
            list: error log
        """
        relationship_class_name = item.get("relationship_class_name")
        object_name_list = item.get("object_name_list")
        if not object_name_list:
            return None, []
        relationships = self._db_map_existing_rels.get(db_map, set())
        if (relationship_class_name, object_name_list) in relationships:
            return None, []
        relationship_class = self._db_map_rel_cls_lookup.get(db_map, {}).get(relationship_class_name)
        if not relationship_class:
            return None, [f"Unknown relationship_class {relationship_class_name}"] if relationship_class_name else []
        object_id_list = []
        for name in object_name_list:
            if object_ := self._db_map_obj_lookup.get(db_map, {}).get(name):
                object_id_list.append(object_["id"])
            else:
                return None, [f"Unknown object {name}"]
        relationship_name = f"{relationship_class_name}__" + "_".join(object_name_list)
        return {"class_id": relationship_class["id"], "object_id_list": object_id_list, "name": relationship_name}, []
