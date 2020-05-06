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
Contains project item specification class.

:authors: M. Marin (KTH)
:date:    7.5.2020
"""
from .metaobject import MetaObject


class ProjectItemSpecification(MetaObject):
    """
    Class to hold a project item specification.

    Attributes:
        item_type (str): type of the project item the specification is compatible with
        definition_file_path (str): specification's JSON file path
    """

    def __init__(self, name, description=None, item_type=""):
        """
        Args:
            name (str): specification name
            description (str): description
            item_type (str): Project item type
        """
        super().__init__(name, description)
        self.item_type = item_type
        self.definition_file_path = ""
