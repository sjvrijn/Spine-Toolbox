#############################################################################
# Copyright (C) 2017 - 2018 VTT Technical Research Centre of Finland
#
# This file is part of Spine Toolbox.
#
# Spine Toolbox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/subwindow_data_connection.ui'
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(220, 305)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Form.setToolTip("")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QtCore.QSize(0, 18))
        self.label_name.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_name.setFont(font)
        self.label_name.setStyleSheet("background-color: rgb(0, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.label_name.setAlignment(QtCore.Qt.AlignCenter)
        self.label_name.setWordWrap(True)
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.treeView_references = QtWidgets.QTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_references.sizePolicy().hasHeightForWidth())
        self.treeView_references.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.treeView_references.setFont(font)
        self.treeView_references.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_references.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_references.setIndentation(5)
        self.treeView_references.setUniformRowHeights(True)
        self.treeView_references.setObjectName("treeView_references")
        self.treeView_references.header().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.treeView_references)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton_plus = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_plus.sizePolicy().hasHeightForWidth())
        self.toolButton_plus.setSizePolicy(sizePolicy)
        self.toolButton_plus.setMinimumSize(QtCore.QSize(20, 20))
        self.toolButton_plus.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_plus.setFont(font)
        self.toolButton_plus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_plus.setIcon(icon)
        self.toolButton_plus.setObjectName("toolButton_plus")
        self.horizontalLayout_2.addWidget(self.toolButton_plus)
        self.toolButton_minus = QtWidgets.QToolButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_minus.sizePolicy().hasHeightForWidth())
        self.toolButton_minus.setSizePolicy(sizePolicy)
        self.toolButton_minus.setMinimumSize(QtCore.QSize(20, 20))
        self.toolButton_minus.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.toolButton_minus.setFont(font)
        self.toolButton_minus.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_minus.setIcon(icon1)
        self.toolButton_minus.setObjectName("toolButton_minus")
        self.horizontalLayout_2.addWidget(self.toolButton_minus)
        self.toolButton_add = QtWidgets.QToolButton(Form)
        self.toolButton_add.setMaximumSize(QtCore.QSize(20, 20))
        self.toolButton_add.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/dc_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_add.setIcon(icon2)
        self.toolButton_add.setObjectName("toolButton_add")
        self.horizontalLayout_2.addWidget(self.toolButton_add)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.toolButton_datapkg = QtWidgets.QToolButton(Form)
        self.toolButton_datapkg.setEnabled(True)
        self.toolButton_datapkg.setMaximumSize(QtCore.QSize(20, 20))
        self.toolButton_datapkg.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/datapkg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_datapkg.setIcon(icon3)
        self.toolButton_datapkg.setObjectName("toolButton_datapkg")
        self.horizontalLayout_2.addWidget(self.toolButton_datapkg)
        self.toolButton_datapkg_keys = QtWidgets.QToolButton(Form)
        self.toolButton_datapkg_keys.setEnabled(True)
        self.toolButton_datapkg_keys.setMaximumSize(QtCore.QSize(20, 20))
        self.toolButton_datapkg_keys.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/keys.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_datapkg_keys.setIcon(icon4)
        self.toolButton_datapkg_keys.setObjectName("toolButton_datapkg_keys")
        self.horizontalLayout_2.addWidget(self.toolButton_datapkg_keys)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.treeView_data = QtWidgets.QTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_data.sizePolicy().hasHeightForWidth())
        self.treeView_data.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.treeView_data.setFont(font)
        self.treeView_data.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView_data.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.treeView_data.setIndentation(5)
        self.treeView_data.setUniformRowHeights(True)
        self.treeView_data.setObjectName("treeView_data")
        self.treeView_data.header().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.treeView_data)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_open = QtWidgets.QPushButton(Form)
        self.pushButton_open.setMaximumSize(QtCore.QSize(75, 23))
        self.pushButton_open.setObjectName("pushButton_open")
        self.horizontalLayout.addWidget(self.pushButton_open)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.treeView_references, self.toolButton_plus)
        Form.setTabOrder(self.toolButton_plus, self.toolButton_minus)
        Form.setTabOrder(self.toolButton_minus, self.toolButton_add)
        Form.setTabOrder(self.toolButton_add, self.treeView_data)
        Form.setTabOrder(self.treeView_data, self.pushButton_open)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Data Connection", None, -1))
        self.label_name.setText(QtWidgets.QApplication.translate("Form", "Name", None, -1))
        self.toolButton_plus.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add references</p></body></html>", None, -1))
        self.toolButton_minus.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Remove selected references or all if nothing is selected</p></body></html>", None, -1))
        self.toolButton_add.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Add references to project. Copies files to Data connection\'s directory.</p></body></html>", None, -1))
        self.toolButton_datapkg.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Generate datapackage.json file.</p></body></html>", None, -1))
        self.toolButton_datapkg_keys.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Edit datapackage\'s keys.</p></body></html>", None, -1))
        self.pushButton_open.setToolTip(QtWidgets.QApplication.translate("Form", "<html><head/><body><p>Open Data Connection directory in File Explorer</p></body></html>", None, -1))
        self.pushButton_open.setText(QtWidgets.QApplication.translate("Form", "Open", None, -1))

import resources_icons_rc
