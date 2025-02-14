# -*- coding: utf-8 -*-
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

################################################################################
## Form generated from reading UI file 'spine_datapackage_form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QHeaderView,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QVBoxLayout, QWidget)

from spinetoolbox.widgets.custom_qtableview import CopyPasteTableView
from spinetoolbox import resources_icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(558, 752)
        MainWindow.setDockNestingEnabled(True)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        icon = QIcon()
        icon.addFile(u":/icons/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClose.setIcon(icon)
        self.actionRemove_foreign_keys = QAction(MainWindow)
        self.actionRemove_foreign_keys.setObjectName(u"actionRemove_foreign_keys")
        icon1 = QIcon()
        icon1.addFile(u":/icons/minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRemove_foreign_keys.setIcon(icon1)
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        icon2 = QIcon()
        icon2.addFile(u":/icons/copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionCopy.setIcon(icon2)
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        icon3 = QIcon()
        icon3.addFile(u":/icons/paste.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPaste.setIcon(icon3)
        self.actionSave_All = QAction(MainWindow)
        self.actionSave_All.setObjectName(u"actionSave_All")
        self.actionSave_All.setEnabled(False)
        self.actionSave_datapackage = QAction(MainWindow)
        self.actionSave_datapackage.setObjectName(u"actionSave_datapackage")
        self.actionSave_datapackage.setEnabled(False)
        self.actionInfer_datapackage = QAction(MainWindow)
        self.actionInfer_datapackage.setObjectName(u"actionInfer_datapackage")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 558, 27))
        self.menubar.setNativeMenuBar(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setToolTipsVisible(True)
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuDock_Widgets = QMenu(self.menuView)
        self.menuDock_Widgets.setObjectName(u"menuDock_Widgets")
        MainWindow.setMenuBar(self.menubar)
        self.dockWidget_fields = QDockWidget(MainWindow)
        self.dockWidget_fields.setObjectName(u"dockWidget_fields")
        self.dockWidget_fields.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.verticalLayout_8 = QVBoxLayout(self.dockWidgetContents_5)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.tableView_fields = CopyPasteTableView(self.dockWidgetContents_5)
        self.tableView_fields.setObjectName(u"tableView_fields")
        self.tableView_fields.setLayoutDirection(Qt.LeftToRight)
        self.tableView_fields.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableView_fields.setShowGrid(True)
        self.tableView_fields.horizontalHeader().setHighlightSections(False)
        self.tableView_fields.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableView_fields.horizontalHeader().setStretchLastSection(True)
        self.tableView_fields.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.tableView_fields)

        self.dockWidget_fields.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_fields)
        self.dockWidget_foreign_keys = QDockWidget(MainWindow)
        self.dockWidget_foreign_keys.setObjectName(u"dockWidget_foreign_keys")
        self.dockWidgetContents_6 = QWidget()
        self.dockWidgetContents_6.setObjectName(u"dockWidgetContents_6")
        self.verticalLayout_9 = QVBoxLayout(self.dockWidgetContents_6)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.tableView_foreign_keys = CopyPasteTableView(self.dockWidgetContents_6)
        self.tableView_foreign_keys.setObjectName(u"tableView_foreign_keys")
        self.tableView_foreign_keys.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView_foreign_keys.setLayoutDirection(Qt.LeftToRight)
        self.tableView_foreign_keys.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableView_foreign_keys.setShowGrid(True)
        self.tableView_foreign_keys.setGridStyle(Qt.SolidLine)
        self.tableView_foreign_keys.horizontalHeader().setHighlightSections(False)
        self.tableView_foreign_keys.horizontalHeader().setStretchLastSection(True)
        self.tableView_foreign_keys.verticalHeader().setVisible(True)

        self.verticalLayout_9.addWidget(self.tableView_foreign_keys)

        self.dockWidget_foreign_keys.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_foreign_keys)
        self.dockWidget_resources = QDockWidget(MainWindow)
        self.dockWidget_resources.setObjectName(u"dockWidget_resources")
        self.dockWidget_resources.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_resources.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableView_resources = CopyPasteTableView(self.dockWidgetContents)
        self.tableView_resources.setObjectName(u"tableView_resources")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_resources.sizePolicy().hasHeightForWidth())
        self.tableView_resources.setSizePolicy(sizePolicy)
        self.tableView_resources.setLayoutDirection(Qt.LeftToRight)
        self.tableView_resources.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView_resources.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableView_resources.setShowGrid(False)
        self.tableView_resources.horizontalHeader().setHighlightSections(False)
        self.tableView_resources.horizontalHeader().setStretchLastSection(True)
        self.tableView_resources.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.tableView_resources)

        self.dockWidget_resources.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_resources)
        self.dockWidget_data = QDockWidget(MainWindow)
        self.dockWidget_data.setObjectName(u"dockWidget_data")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tableView_resource_data = CopyPasteTableView(self.dockWidgetContents_2)
        self.tableView_resource_data.setObjectName(u"tableView_resource_data")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableView_resource_data.sizePolicy().hasHeightForWidth())
        self.tableView_resource_data.setSizePolicy(sizePolicy1)
        self.tableView_resource_data.setLayoutDirection(Qt.LeftToRight)
        self.tableView_resource_data.setTabKeyNavigation(False)
        self.tableView_resource_data.horizontalHeader().setVisible(True)
        self.tableView_resource_data.horizontalHeader().setHighlightSections(False)
        self.tableView_resource_data.horizontalHeader().setStretchLastSection(True)
        self.tableView_resource_data.verticalHeader().setVisible(False)
        self.tableView_resource_data.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.tableView_resource_data)

        self.dockWidget_data.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_data)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionSave_datapackage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_All)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuView.addAction(self.menuDock_Widgets.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Spine datapackage editor", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
#if QT_CONFIG(shortcut)
        self.actionClose.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionRemove_foreign_keys.setText(QCoreApplication.translate("MainWindow", u"Remove foreign keys", None))
#if QT_CONFIG(tooltip)
        self.actionRemove_foreign_keys.setToolTip(QCoreApplication.translate("MainWindow", u"Remove selected foreign keys.", None))
#endif // QT_CONFIG(tooltip)
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
#if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
#if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_All.setText(QCoreApplication.translate("MainWindow", u"Save All", None))
#if QT_CONFIG(shortcut)
        self.actionSave_All.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_datapackage.setText(QCoreApplication.translate("MainWindow", u"Save datapackage.json", None))
        self.actionInfer_datapackage.setText(QCoreApplication.translate("MainWindow", u"Infer datapackage", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuDock_Widgets.setTitle(QCoreApplication.translate("MainWindow", u"Dock Widgets", None))
        self.dockWidget_fields.setWindowTitle(QCoreApplication.translate("MainWindow", u"Fields", None))
        self.dockWidget_foreign_keys.setWindowTitle(QCoreApplication.translate("MainWindow", u"Foreign keys", None))
        self.dockWidget_resources.setWindowTitle(QCoreApplication.translate("MainWindow", u"Resources", None))
        self.dockWidget_data.setWindowTitle(QCoreApplication.translate("MainWindow", u"Data", None))
    # retranslateUi

