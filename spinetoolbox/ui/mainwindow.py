# -*- coding: utf-8 -*-
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

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide2.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QIcon,
    QKeySequence,
    QLinearGradient,
    QPalette,
    QPainter,
    QPixmap,
    QRadialGradient,
)
from PySide2.QtWidgets import *

from spinetoolbox.widgets.custom_qtextbrowser import CustomQTextBrowser
from spinetoolbox.widgets.custom_qgraphicsviews import DesignQGraphicsView

from spinetoolbox import resources_icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1322, 700)
        MainWindow.setDockNestingEnabled(True)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon = QIcon()
        icon.addFile(u":/icons/menu_icons/window-close.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionQuit.setIcon(icon)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon1 = QIcon()
        icon1.addFile(u":/icons/menu_icons/info-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon1)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon()
        icon2.addFile(u":/icons/menu_icons/save_solid.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        icon3 = QIcon()
        icon3.addFile(u":/icons/menu_icons/save_regular.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_As.setIcon(icon3)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon4 = QIcon()
        icon4.addFile(u":/icons/menu_icons/folder-open-solid.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon4)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon5 = QIcon()
        icon5.addFile(u":/icons/menu_icons/file.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew.setIcon(icon5)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        icon6 = QIcon()
        icon6.addFile(u":/icons/menu_icons/cog.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon6)
        self.actionItem_Toolbar = QAction(MainWindow)
        self.actionItem_Toolbar.setObjectName(u"actionItem_Toolbar")
        self.actionAdd_Item_Toolbar = QAction(MainWindow)
        self.actionAdd_Item_Toolbar.setObjectName(u"actionAdd_Item_Toolbar")
        self.actionEvent_Log = QAction(MainWindow)
        self.actionEvent_Log.setObjectName(u"actionEvent_Log")
        self.actionEvent_Log.setCheckable(False)
        self.actionEvent_Log.setChecked(False)
        self.actionSubprocess_Output = QAction(MainWindow)
        self.actionSubprocess_Output.setObjectName(u"actionSubprocess_Output")
        self.actionSelected_Item = QAction(MainWindow)
        self.actionSelected_Item.setObjectName(u"actionSelected_Item")
        self.actionJulia_REPL = QAction(MainWindow)
        self.actionJulia_REPL.setObjectName(u"actionJulia_REPL")
        self.actionUser_Guide = QAction(MainWindow)
        self.actionUser_Guide.setObjectName(u"actionUser_Guide")
        icon7 = QIcon()
        icon7.addFile(u":/icons/menu_icons/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionUser_Guide.setIcon(icon7)
        self.actionRestore_Dock_Widgets = QAction(MainWindow)
        self.actionRestore_Dock_Widgets.setObjectName(u"actionRestore_Dock_Widgets")
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(u"actionAbout_Qt")
        icon8 = QIcon()
        icon8.addFile(u":/icons/qt_extended_48x48.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout_Qt.setIcon(icon8)
        self.actionRemove_all = QAction(MainWindow)
        self.actionRemove_all.setObjectName(u"actionRemove_all")
        icon9 = QIcon()
        icon9.addFile(u":/icons/menu_icons/trash-alt.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRemove_all.setIcon(icon9)
        self.actionGetting_started = QAction(MainWindow)
        self.actionGetting_started.setObjectName(u"actionGetting_started")
        self.actionGetting_started.setIcon(icon7)
        self.actionOpen_recent = QAction(MainWindow)
        self.actionOpen_recent.setObjectName(u"actionOpen_recent")
        icon10 = QIcon()
        icon10.addFile(u":/icons/menu_icons/history.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_recent.setIcon(icon10)
        self.actionCopy = QAction(MainWindow)
        self.actionCopy.setObjectName(u"actionCopy")
        self.actionPaste = QAction(MainWindow)
        self.actionPaste.setObjectName(u"actionPaste")
        self.actionDuplicate = QAction(MainWindow)
        self.actionDuplicate.setObjectName(u"actionDuplicate")
        self.actionLive_tutorial = QAction(MainWindow)
        self.actionLive_tutorial.setObjectName(u"actionLive_tutorial")
        self.actionLive_tutorial.setIcon(icon7)
        self.actionUpgrade_project = QAction(MainWindow)
        self.actionUpgrade_project.setObjectName(u"actionUpgrade_project")
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        self.actionOpen_project_directory = QAction(MainWindow)
        self.actionOpen_project_directory.setObjectName(u"actionOpen_project_directory")
        self.actionOpen_item_directory = QAction(MainWindow)
        self.actionOpen_item_directory.setObjectName(u"actionOpen_item_directory")
        self.actionRename_item = QAction(MainWindow)
        self.actionRename_item.setObjectName(u"actionRename_item")
        self.actionNew_DB_editor = QAction(MainWindow)
        self.actionNew_DB_editor.setObjectName(u"actionNew_DB_editor")
        icon11 = QIcon()
        icon11.addFile(u":/icons/database-edit.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew_DB_editor.setIcon(icon11)
        self.actionPasteAndDuplicateFiles = QAction(MainWindow)
        self.actionPasteAndDuplicateFiles.setObjectName(u"actionPasteAndDuplicateFiles")
        self.actionDuplicateAndDuplicateFiles = QAction(MainWindow)
        self.actionDuplicateAndDuplicateFiles.setObjectName(u"actionDuplicateAndDuplicateFiles")
        self.actionInstall_plugin = QAction(MainWindow)
        self.actionInstall_plugin.setObjectName(u"actionInstall_plugin")
        self.actionManage_plugins = QAction(MainWindow)
        self.actionManage_plugins.setObjectName(u"actionManage_plugins")
        self.actionCreate_plugin = QAction(MainWindow)
        self.actionCreate_plugin.setObjectName(u"actionCreate_plugin")
        self.actionCreate_plugin.setEnabled(False)
        self.actionCreate_plugin.setVisible(False)
        self.actionStartJuliaConsole = QAction(MainWindow)
        self.actionStartJuliaConsole.setObjectName(u"actionStartJuliaConsole")
        icon12 = QIcon()
        icon12.addFile(u":/icons/julia-dots.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStartJuliaConsole.setIcon(icon12)
        self.actionStartPythonConsole = QAction(MainWindow)
        self.actionStartPythonConsole.setObjectName(u"actionStartPythonConsole")
        icon13 = QIcon()
        icon13.addFile(u":/icons/python.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStartPythonConsole.setIcon(icon13)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        icon14 = QIcon()
        icon14.addFile(u":/icons/menu_icons/door-closed.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClose.setIcon(icon14)
        self.actionRename_project = QAction(MainWindow)
        self.actionRename_project.setObjectName(u"actionRename_project")
        icon15 = QIcon()
        icon15.addFile(u":/icons/menu_icons/exchange-alt.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRename_project.setIcon(icon15)
        self.actionExecute_project = QAction(MainWindow)
        self.actionExecute_project.setObjectName(u"actionExecute_project")
        icon16 = QIcon()
        icon16.addFile(u":/icons/menu_icons/play-circle-solid.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExecute_project.setIcon(icon16)
        self.actionExecute_selection = QAction(MainWindow)
        self.actionExecute_selection.setObjectName(u"actionExecute_selection")
        icon17 = QIcon()
        icon17.addFile(u":/icons/menu_icons/play-circle-regular.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExecute_selection.setIcon(icon17)
        self.actionStop_execution = QAction(MainWindow)
        self.actionStop_execution.setObjectName(u"actionStop_execution")
        icon18 = QIcon()
        icon18.addFile(u":/icons/menu_icons/stop-circle-regular.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStop_execution.setIcon(icon18)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_10 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1322, 27))
        self.menubar.setNativeMenuBar(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setToolTipsVisible(True)
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuToolbars = QMenu(self.menuView)
        self.menuToolbars.setObjectName(u"menuToolbars")
        self.menuDock_Widgets = QMenu(self.menuView)
        self.menuDock_Widgets.setObjectName(u"menuDock_Widgets")
        self.menuPlugins = QMenu(self.menubar)
        self.menuPlugins.setObjectName(u"menuPlugins")
        self.menuConsoles = QMenu(self.menubar)
        self.menuConsoles.setObjectName(u"menuConsoles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_eventlog = QDockWidget(MainWindow)
        self.dockWidget_eventlog.setObjectName(u"dockWidget_eventlog")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_eventlog.sizePolicy().hasHeightForWidth())
        self.dockWidget_eventlog.setSizePolicy(sizePolicy)
        self.dockWidget_eventlog.setMinimumSize(QSize(174, 184))
        self.dockWidget_eventlog.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textBrowser_eventlog = CustomQTextBrowser(self.dockWidgetContents)
        self.textBrowser_eventlog.setObjectName(u"textBrowser_eventlog")
        sizePolicy.setHeightForWidth(self.textBrowser_eventlog.sizePolicy().hasHeightForWidth())
        self.textBrowser_eventlog.setSizePolicy(sizePolicy)
        self.textBrowser_eventlog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.textBrowser_eventlog.setOpenLinks(False)

        self.verticalLayout_5.addWidget(self.textBrowser_eventlog)

        self.dockWidget_eventlog.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_eventlog)
        self.dockWidget_itemlog = QDockWidget(MainWindow)
        self.dockWidget_itemlog.setObjectName(u"dockWidget_itemlog")
        sizePolicy.setHeightForWidth(self.dockWidget_itemlog.sizePolicy().hasHeightForWidth())
        self.dockWidget_itemlog.setSizePolicy(sizePolicy)
        self.dockWidget_itemlog.setMinimumSize(QSize(382, 178))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        sizePolicy1.setHeightForWidth(self.dockWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_no_itemlog = QLabel(self.dockWidgetContents_2)
        self.label_no_itemlog.setObjectName(u"label_no_itemlog")
        self.label_no_itemlog.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_no_itemlog)

        self.textBrowser_itemlog = CustomQTextBrowser(self.dockWidgetContents_2)
        self.textBrowser_itemlog.setObjectName(u"textBrowser_itemlog")
        sizePolicy.setHeightForWidth(self.textBrowser_itemlog.sizePolicy().hasHeightForWidth())
        self.textBrowser_itemlog.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Segoe UI")
        self.textBrowser_itemlog.setFont(font)
        self.textBrowser_itemlog.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.textBrowser_itemlog.setOpenLinks(False)

        self.verticalLayout_3.addWidget(self.textBrowser_itemlog)

        self.dockWidget_itemlog.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_itemlog)
        self.dockWidget_item = QDockWidget(MainWindow)
        self.dockWidget_item.setObjectName(u"dockWidget_item")
        self.dockWidget_item.setMinimumSize(QSize(356, 293))
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_item_properties = QTabWidget(self.dockWidgetContents_3)
        self.tabWidget_item_properties.setObjectName(u"tabWidget_item_properties")
        self.tabWidget_item_properties.setStyleSheet(u"")
        self.tab_no_selection = QWidget()
        self.tab_no_selection.setObjectName(u"tab_no_selection")
        self.verticalLayout_14 = QVBoxLayout(self.tab_no_selection)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(6, 6, 6, 6)
        self.label_no_selection = QLabel(self.tab_no_selection)
        self.label_no_selection.setObjectName(u"label_no_selection")
        self.label_no_selection.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_no_selection)

        self.listView_executions = QTreeView(self.tab_no_selection)
        self.listView_executions.setObjectName(u"listView_executions")
        sizePolicy1.setHeightForWidth(self.listView_executions.sizePolicy().hasHeightForWidth())
        self.listView_executions.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setPointSize(11)
        self.listView_executions.setFont(font1)

        self.verticalLayout_14.addWidget(self.listView_executions)

        self.tabWidget_item_properties.addTab(self.tab_no_selection, "")

        self.verticalLayout.addWidget(self.tabWidget_item_properties)

        self.dockWidget_item.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_item)
        self.dockWidget_project = QDockWidget(MainWindow)
        self.dockWidget_project.setObjectName(u"dockWidget_project")
        self.dockWidget_project.setMinimumSize(QSize(136, 344))
        self.dockWidget_project.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.treeView_project = QTreeView(self.dockWidgetContents_4)
        self.treeView_project.setObjectName(u"treeView_project")
        sizePolicy1.setHeightForWidth(self.treeView_project.sizePolicy().hasHeightForWidth())
        self.treeView_project.setSizePolicy(sizePolicy1)
        self.treeView_project.setMaximumSize(QSize(16777215, 16777215))
        self.treeView_project.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView_project.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView_project.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView_project.setUniformRowHeights(True)
        self.treeView_project.setAnimated(True)
        self.treeView_project.header().setVisible(False)

        self.verticalLayout_4.addWidget(self.treeView_project)

        self.dockWidget_project.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_project)
        self.dockWidget_console = QDockWidget(MainWindow)
        self.dockWidget_console.setObjectName(u"dockWidget_console")
        self.dockWidget_console.setFloating(False)
        self.dockWidget_console.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.dockWidgetContents_console = QWidget()
        self.dockWidgetContents_console.setObjectName(u"dockWidgetContents_console")
        self.verticalLayout_20 = QVBoxLayout(self.dockWidgetContents_console)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.label_no_console = QLabel(self.dockWidgetContents_console)
        self.label_no_console.setObjectName(u"label_no_console")
        self.label_no_console.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.label_no_console.setAlignment(Qt.AlignCenter)

        self.verticalLayout_20.addWidget(self.label_no_console)

        self.dockWidget_console.setWidget(self.dockWidgetContents_console)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_console)
        self.dockWidget_design_view = QDockWidget(MainWindow)
        self.dockWidget_design_view.setObjectName(u"dockWidget_design_view")
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents_5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = DesignQGraphicsView(self.dockWidgetContents_5)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy1.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy1)
        self.graphicsView.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setFrameShadow(QFrame.Raised)
        self.graphicsView.setMidLineWidth(0)
        self.graphicsView.setAlignment(Qt.AlignCenter)
        self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.graphicsView.setRubberBandSelectionMode(Qt.ContainsItemBoundingRect)

        self.verticalLayout_2.addWidget(self.graphicsView)

        self.dockWidget_design_view.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget_design_view)
        QWidget.setTabOrder(self.textBrowser_eventlog, self.textBrowser_itemlog)
        QWidget.setTabOrder(self.textBrowser_itemlog, self.tabWidget_item_properties)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuPlugins.menuAction())
        self.menubar.addAction(self.menuConsoles.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_recent)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionRename_project)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew_DB_editor)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionUser_Guide)
        self.menuHelp.addAction(self.actionGetting_started)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionPasteAndDuplicateFiles)
        self.menuEdit.addAction(self.actionDuplicate)
        self.menuEdit.addAction(self.actionDuplicateAndDuplicateFiles)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionRemove)
        self.menuEdit.addAction(self.actionRemove_all)
        self.menuView.addAction(self.menuToolbars.menuAction())
        self.menuView.addAction(self.menuDock_Widgets.menuAction())
        self.menuDock_Widgets.addAction(self.actionRestore_Dock_Widgets)
        self.menuDock_Widgets.addSeparator()
        self.menuPlugins.addAction(self.actionInstall_plugin)
        self.menuPlugins.addAction(self.actionManage_plugins)
        self.menuPlugins.addSeparator()
        self.menuPlugins.addAction(self.actionCreate_plugin)
        self.menuConsoles.addAction(self.actionStartPythonConsole)
        self.menuConsoles.addAction(self.actionStartJuliaConsole)

        self.retranslateUi(MainWindow)

        self.tabWidget_item_properties.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Spine Toolbox", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        # if QT_CONFIG(tooltip)
        self.actionQuit.setToolTip(
            QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Quit</p></body></html>", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
        # endif // QT_CONFIG(shortcut)
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        # if QT_CONFIG(shortcut)
        self.actionAbout.setShortcut(QCoreApplication.translate("MainWindow", u"F12", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save project", None))
        # if QT_CONFIG(tooltip)
        self.actionSave.setToolTip(
            QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Save project</p></body></html>", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save project as...", None))
        # if QT_CONFIG(tooltip)
        self.actionSave_As.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Save project in another directory</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
        # endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open project...", None))
        # if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open existing project</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
        # endif // QT_CONFIG(shortcut)
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New project...", None))
        # if QT_CONFIG(tooltip)
        self.actionNew.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Create new project</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings...", None))
        # if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open application and project settings</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionSettings.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+,", None))
        # endif // QT_CONFIG(shortcut)
        self.actionItem_Toolbar.setText(QCoreApplication.translate("MainWindow", u"Item Toolbar", None))
        self.actionAdd_Item_Toolbar.setText(QCoreApplication.translate("MainWindow", u"Add Item Toolbar", None))
        # if QT_CONFIG(tooltip)
        self.actionAdd_Item_Toolbar.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Make Add Item Toolbar visible</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionEvent_Log.setText(QCoreApplication.translate("MainWindow", u"Event Log", None))
        # if QT_CONFIG(tooltip)
        self.actionEvent_Log.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Make Event Log widget visible</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSubprocess_Output.setText(QCoreApplication.translate("MainWindow", u"Subprocess Output", None))
        # if QT_CONFIG(tooltip)
        self.actionSubprocess_Output.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Make Subprocess Output widget visible</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSelected_Item.setText(QCoreApplication.translate("MainWindow", u"Selected Item", None))
        # if QT_CONFIG(tooltip)
        self.actionSelected_Item.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Make Selected Item widget visible</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionJulia_REPL.setText(QCoreApplication.translate("MainWindow", u"Julia REPL", None))
        # if QT_CONFIG(tooltip)
        self.actionJulia_REPL.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Make Julia REPL widget visible</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionUser_Guide.setText(QCoreApplication.translate("MainWindow", u"User guide", None))
        # if QT_CONFIG(shortcut)
        self.actionUser_Guide.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
        # endif // QT_CONFIG(shortcut)
        self.actionRestore_Dock_Widgets.setText(QCoreApplication.translate("MainWindow", u"Restore Dock Widgets", None))
        # if QT_CONFIG(tooltip)
        self.actionRestore_Dock_Widgets.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                u"<html><head/><body><p>Dock all floating and/or hidden dock widgets back to main window.</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionAbout_Qt.setText(QCoreApplication.translate("MainWindow", u"About Qt...", None))
        # if QT_CONFIG(shortcut)
        self.actionAbout_Qt.setShortcut(QCoreApplication.translate("MainWindow", u"F11", None))
        # endif // QT_CONFIG(shortcut)
        self.actionRemove_all.setText(QCoreApplication.translate("MainWindow", u"Remove all", None))
        # if QT_CONFIG(tooltip)
        self.actionRemove_all.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Remove all project items</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionGetting_started.setText(QCoreApplication.translate("MainWindow", u"Getting started", None))
        # if QT_CONFIG(shortcut)
        self.actionGetting_started.setShortcut(QCoreApplication.translate("MainWindow", u"F3", None))
        # endif // QT_CONFIG(shortcut)
        self.actionOpen_recent.setText(QCoreApplication.translate("MainWindow", u"Open recent", None))
        # if QT_CONFIG(tooltip)
        self.actionOpen_recent.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open recent project</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionCopy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        # if QT_CONFIG(tooltip)
        self.actionCopy.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Copy project item(s)</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionCopy.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
        # endif // QT_CONFIG(shortcut)
        self.actionPaste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        # if QT_CONFIG(tooltip)
        self.actionPaste.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Paste project item(s)</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionPaste.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+V", None))
        # endif // QT_CONFIG(shortcut)
        self.actionDuplicate.setText(QCoreApplication.translate("MainWindow", u"Duplicate", None))
        # if QT_CONFIG(tooltip)
        self.actionDuplicate.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Duplicate project item(s)</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionDuplicate.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
        # endif // QT_CONFIG(shortcut)
        self.actionLive_tutorial.setText(QCoreApplication.translate("MainWindow", u"Live tutorial", None))
        # if QT_CONFIG(shortcut)
        self.actionLive_tutorial.setShortcut(QCoreApplication.translate("MainWindow", u"Shift+F2", None))
        # endif // QT_CONFIG(shortcut)
        self.actionUpgrade_project.setText(QCoreApplication.translate("MainWindow", u"Upgrade project", None))
        # if QT_CONFIG(tooltip)
        self.actionUpgrade_project.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                u"<html><head/><body><p>Upgrade old (.proj) Spine Toolbox project into a new style directory based project</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        # if QT_CONFIG(tooltip)
        self.actionRemove.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Remove project item(s)</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionRemove.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
        # endif // QT_CONFIG(shortcut)
        self.actionOpen_project_directory.setText(
            QCoreApplication.translate("MainWindow", u"Open project directory...", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionOpen_project_directory.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open project directory in file browser</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionOpen_item_directory.setText(
            QCoreApplication.translate("MainWindow", u"Open item directory...", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionOpen_item_directory.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open item directory in file browser</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionRename_item.setText(QCoreApplication.translate("MainWindow", u"Rename...", None))
        # if QT_CONFIG(tooltip)
        self.actionRename_item.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Rename project item</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionNew_DB_editor.setText(QCoreApplication.translate("MainWindow", u"New DB editor", None))
        # if QT_CONFIG(tooltip)
        self.actionNew_DB_editor.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Open Spine Db Editor</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionPasteAndDuplicateFiles.setText(
            QCoreApplication.translate("MainWindow", u"Paste and duplicate files", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionPasteAndDuplicateFiles.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Paste project item(s) and duplicate files</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionPasteAndDuplicateFiles.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+V", None))
        # endif // QT_CONFIG(shortcut)
        self.actionDuplicateAndDuplicateFiles.setText(
            QCoreApplication.translate("MainWindow", u"Duplicate and duplicate files", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionDuplicateAndDuplicateFiles.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                u"<html><head/><body><p>Duplicate project item(s) and duplicate files</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionDuplicateAndDuplicateFiles.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Shift+D", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionInstall_plugin.setText(QCoreApplication.translate("MainWindow", u"Install plugin...", None))
        self.actionManage_plugins.setText(QCoreApplication.translate("MainWindow", u"Manage plugins...", None))
        self.actionCreate_plugin.setText(QCoreApplication.translate("MainWindow", u"Create plugin...", None))
        self.actionStartJuliaConsole.setText(QCoreApplication.translate("MainWindow", u"Start Julia Console", None))
        # if QT_CONFIG(tooltip)
        self.actionStartJuliaConsole.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                u"<html><head/><body><p>Start Julia Console using the kernel selected in Settings-&gt;Tools</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionStartJuliaConsole.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+2", None))
        # endif // QT_CONFIG(shortcut)
        self.actionStartPythonConsole.setText(QCoreApplication.translate("MainWindow", u"Start Python Console", None))
        # if QT_CONFIG(tooltip)
        self.actionStartPythonConsole.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                u"<html><head/><body><p>Start Python Console using the kernel selected in Settings-&gt;Tools</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionStartPythonConsole.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+1", None))
        # endif // QT_CONFIG(shortcut)
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close project", None))
        # if QT_CONFIG(tooltip)
        self.actionClose.setToolTip(
            QCoreApplication.translate(
                "MainWindow", u"<html><head/><body><p>Close current project</p></body></html>", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionRename_project.setText(QCoreApplication.translate("MainWindow", u"Rename project...", None))
        # if QT_CONFIG(tooltip)
        self.actionRename_project.setToolTip(QCoreApplication.translate("MainWindow", u"Rename project", None))
        # endif // QT_CONFIG(tooltip)
        self.actionExecute_project.setText(QCoreApplication.translate("MainWindow", u"Execute project", None))
        # if QT_CONFIG(shortcut)
        self.actionExecute_project.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
        # endif // QT_CONFIG(shortcut)
        self.actionExecute_selection.setText(QCoreApplication.translate("MainWindow", u"Execute selection", None))
        # if QT_CONFIG(shortcut)
        self.actionExecute_selection.setShortcut(QCoreApplication.translate("MainWindow", u"F6", None))
        # endif // QT_CONFIG(shortcut)
        self.actionStop_execution.setText(QCoreApplication.translate("MainWindow", u"Stop execution", None))
        # if QT_CONFIG(shortcut)
        self.actionStop_execution.setShortcut(QCoreApplication.translate("MainWindow", u"F7", None))
        # endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuToolbars.setTitle(QCoreApplication.translate("MainWindow", u"Toolbars", None))
        self.menuDock_Widgets.setTitle(QCoreApplication.translate("MainWindow", u"Dock widgets", None))
        self.menuPlugins.setTitle(QCoreApplication.translate("MainWindow", u"Plugins", None))
        self.menuConsoles.setTitle(QCoreApplication.translate("MainWindow", u"Consoles", None))
        self.dockWidget_eventlog.setWindowTitle(QCoreApplication.translate("MainWindow", u"Event Log", None))
        self.dockWidget_itemlog.setWindowTitle(QCoreApplication.translate("MainWindow", u"Item Execution Log", None))
        self.label_no_itemlog.setText(
            QCoreApplication.translate(
                "MainWindow", u"Select and execute a project item to view its execution log", None
            )
        )
        self.dockWidget_item.setWindowTitle(QCoreApplication.translate("MainWindow", u"Properties", None))
        self.label_no_selection.setText(
            QCoreApplication.translate("MainWindow", u"Select a project item to view its properties", None)
        )
        self.tabWidget_item_properties.setTabText(
            self.tabWidget_item_properties.indexOf(self.tab_no_selection),
            QCoreApplication.translate("MainWindow", u"No Selection", None),
        )
        self.dockWidget_project.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project", None))
        self.dockWidget_console.setWindowTitle(QCoreApplication.translate("MainWindow", u"Console", None))
        self.label_no_console.setText(
            QCoreApplication.translate("MainWindow", u"Select and execute a Tool to see its console", None)
        )
        self.dockWidget_design_view.setWindowTitle(QCoreApplication.translate("MainWindow", u"Design View", None))

    # retranslateUi
