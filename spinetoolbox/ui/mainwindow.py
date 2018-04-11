#############################################################################\
# Copyright (C) 2017 - 2018 VTT Technical Research Centre of Finland\
#\
# This file is part of Spine Toolbox.\
#\
# Spine Toolbox is free software: you can redistribute it and\/or modify\
# it under the terms of the GNU Lesser General Public License as published by\
# the Free Software Foundation, either version 3 of the License, or\
# (at your option) any later version.\
#\
# This program is distributed in the hope that it will be useful,\
# but WITHOUT ANY WARRANTY; without even the implied warranty of\
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\
# GNU Lesser General Public License for more details.\
#\
# You should have received a copy of the GNU Lesser General Public License\
# along with this program.  If not, see <http:\/\/www.gnu.org\/licenses\/>.\
#############################################################################\

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/mainwindow.ui'
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(709, 557)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setObjectName("splitter")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_project = QtWidgets.QWidget()
        self.tab_project.setObjectName("tab_project")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_project)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeView_project = QtWidgets.QTreeView(self.tab_project)
        self.treeView_project.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView_project.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.treeView_project.setObjectName("treeView_project")
        self.verticalLayout_2.addWidget(self.treeView_project)
        self.groupBox = QtWidgets.QGroupBox(self.tab_project)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_type = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_type.sizePolicy().hasHeightForWidth())
        self.lineEdit_type.setSizePolicy(sizePolicy)
        self.lineEdit_type.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_type.setReadOnly(True)
        self.lineEdit_type.setObjectName("lineEdit_type")
        self.verticalLayout.addWidget(self.lineEdit_type)
        self.lineEdit_name = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_name.sizePolicy().hasHeightForWidth())
        self.lineEdit_name.setSizePolicy(sizePolicy)
        self.lineEdit_name.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_name.setReadOnly(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.verticalLayout.addWidget(self.lineEdit_name)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_project, "")
        self.tab_tool_templates = QtWidgets.QWidget()
        self.tab_tool_templates.setObjectName("tab_tool_templates")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_tool_templates)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.listView_tool_templates = QtWidgets.QListView(self.tab_tool_templates)
        self.listView_tool_templates.setObjectName("listView_tool_templates")
        self.verticalLayout_5.addWidget(self.listView_tool_templates)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add_tool_template = QtWidgets.QPushButton(self.tab_tool_templates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add_tool_template.sizePolicy().hasHeightForWidth())
        self.pushButton_add_tool_template.setSizePolicy(sizePolicy)
        self.pushButton_add_tool_template.setMinimumSize(QtCore.QSize(26, 26))
        self.pushButton_add_tool_template.setMaximumSize(QtCore.QSize(26, 26))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/add_tool.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add_tool_template.setIcon(icon)
        self.pushButton_add_tool_template.setIconSize(QtCore.QSize(22, 22))
        self.pushButton_add_tool_template.setObjectName("pushButton_add_tool_template")
        self.horizontalLayout.addWidget(self.pushButton_add_tool_template)
        self.pushButton_refresh_tool_templates = QtWidgets.QPushButton(self.tab_tool_templates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_refresh_tool_templates.sizePolicy().hasHeightForWidth())
        self.pushButton_refresh_tool_templates.setSizePolicy(sizePolicy)
        self.pushButton_refresh_tool_templates.setMinimumSize(QtCore.QSize(26, 26))
        self.pushButton_refresh_tool_templates.setMaximumSize(QtCore.QSize(26, 26))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/refresh_tools.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_refresh_tool_templates.setIcon(icon1)
        self.pushButton_refresh_tool_templates.setIconSize(QtCore.QSize(22, 22))
        self.pushButton_refresh_tool_templates.setObjectName("pushButton_refresh_tool_templates")
        self.horizontalLayout.addWidget(self.pushButton_refresh_tool_templates)
        self.pushButton_remove_tool_template = QtWidgets.QPushButton(self.tab_tool_templates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_remove_tool_template.sizePolicy().hasHeightForWidth())
        self.pushButton_remove_tool_template.setSizePolicy(sizePolicy)
        self.pushButton_remove_tool_template.setMinimumSize(QtCore.QSize(26, 26))
        self.pushButton_remove_tool_template.setMaximumSize(QtCore.QSize(26, 26))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/remove_tool.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_remove_tool_template.setIcon(icon2)
        self.pushButton_remove_tool_template.setIconSize(QtCore.QSize(22, 22))
        self.pushButton_remove_tool_template.setObjectName("pushButton_remove_tool_template")
        self.horizontalLayout.addWidget(self.pushButton_remove_tool_template)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_tool_templates, "")
        self.tab_connections = QtWidgets.QWidget()
        self.tab_connections.setObjectName("tab_connections")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_connections)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tableView_connections = QtWidgets.QTableView(self.tab_connections)
        self.tableView_connections.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView_connections.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView_connections.setObjectName("tableView_connections")
        self.tableView_connections.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_7.addWidget(self.tableView_connections)
        self.tabWidget.addTab(self.tab_connections, "")
        self.mdiArea_container = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea_container.sizePolicy().hasHeightForWidth())
        self.mdiArea_container.setSizePolicy(sizePolicy)
        self.mdiArea_container.setObjectName("mdiArea_container")
        self.verticalLayout_4.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 709, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuToolbars = QtWidgets.QMenu(self.menuView)
        self.menuToolbars.setObjectName("menuToolbars")
        self.menuDock_Widgets = QtWidgets.QMenu(self.menuView)
        self.menuDock_Widgets.setObjectName("menuDock_Widgets")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_eventlog = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_eventlog.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_eventlog.setObjectName("dockWidget_eventlog")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textBrowser_eventlog = CustomQTextBrowser(self.dockWidgetContents)
        self.textBrowser_eventlog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textBrowser_eventlog.setOpenLinks(False)
        self.textBrowser_eventlog.setObjectName("textBrowser_eventlog")
        self.verticalLayout_3.addWidget(self.textBrowser_eventlog)
        self.dockWidget_eventlog.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_eventlog)
        self.dockWidget_process_output = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_process_output.setObjectName("dockWidget_process_output")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.textBrowser_process_output = CustomQTextBrowser(self.dockWidgetContents_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.textBrowser_process_output.setFont(font)
        self.textBrowser_process_output.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textBrowser_process_output.setOpenLinks(False)
        self.textBrowser_process_output.setObjectName("textBrowser_process_output")
        self.verticalLayout_6.addWidget(self.textBrowser_process_output)
        self.dockWidget_process_output.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_process_output)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionData_Store = QtWidgets.QAction(MainWindow)
        self.actionData_Store.setObjectName("actionData_Store")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAdd_Data_Connection = QtWidgets.QAction(MainWindow)
        self.actionAdd_Data_Connection.setObjectName("actionAdd_Data_Connection")
        self.actionAdd_Data_Store = QtWidgets.QAction(MainWindow)
        self.actionAdd_Data_Store.setObjectName("actionAdd_Data_Store")
        self.actionAdd_Tool = QtWidgets.QAction(MainWindow)
        self.actionAdd_Tool.setObjectName("actionAdd_Tool")
        self.actionAdd_View = QtWidgets.QAction(MainWindow)
        self.actionAdd_View.setObjectName("actionAdd_View")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionItem_Toolbar = QtWidgets.QAction(MainWindow)
        self.actionItem_Toolbar.setObjectName("actionItem_Toolbar")
        self.actionAdd_Item_Toolbar = QtWidgets.QAction(MainWindow)
        self.actionAdd_Item_Toolbar.setObjectName("actionAdd_Item_Toolbar")
        self.actionEvent_Log = QtWidgets.QAction(MainWindow)
        self.actionEvent_Log.setObjectName("actionEvent_Log")
        self.actionSubprocess_Output = QtWidgets.QAction(MainWindow)
        self.actionSubprocess_Output.setObjectName("actionSubprocess_Output")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEdit.addAction(self.actionAdd_Data_Store)
        self.menuEdit.addAction(self.actionAdd_Data_Connection)
        self.menuEdit.addAction(self.actionAdd_Tool)
        self.menuEdit.addAction(self.actionAdd_View)
        self.menuToolbars.addAction(self.actionAdd_Item_Toolbar)
        self.menuDock_Widgets.addAction(self.actionEvent_Log)
        self.menuDock_Widgets.addAction(self.actionSubprocess_Output)
        self.menuView.addAction(self.menuToolbars.menuAction())
        self.menuView.addAction(self.menuDock_Widgets.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.treeView_project)
        MainWindow.setTabOrder(self.treeView_project, self.listView_tool_templates)
        MainWindow.setTabOrder(self.listView_tool_templates, self.pushButton_add_tool_template)
        MainWindow.setTabOrder(self.pushButton_add_tool_template, self.pushButton_refresh_tool_templates)
        MainWindow.setTabOrder(self.pushButton_refresh_tool_templates, self.pushButton_remove_tool_template)
        MainWindow.setTabOrder(self.pushButton_remove_tool_template, self.textBrowser_eventlog)
        MainWindow.setTabOrder(self.textBrowser_eventlog, self.textBrowser_process_output)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Spine Toolbox", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Selected Item", None, -1))
        self.lineEdit_type.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Type", None, -1))
        self.lineEdit_name.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "Name", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_project), QtWidgets.QApplication.translate("MainWindow", "Project", None, -1))
        self.listView_tool_templates.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Tool Templates available in this project</p></body></html>", None, -1))
        self.pushButton_add_tool_template.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Add Tool Template to project</p></body></html>", None, -1))
        self.pushButton_refresh_tool_templates.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Refresh Tool Templates. Press this button to refresh Tools that use this Template if the Template has changed.</p></body></html>", None, -1))
        self.pushButton_remove_tool_template.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Remove Tool Template from project</p></body></html>", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tool_templates), QtWidgets.QApplication.translate("MainWindow", "Templates", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_connections), QtWidgets.QApplication.translate("MainWindow", "Connections", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("MainWindow", "Help", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.menuView.setTitle(QtWidgets.QApplication.translate("MainWindow", "View", None, -1))
        self.menuToolbars.setTitle(QtWidgets.QApplication.translate("MainWindow", "Toolbars", None, -1))
        self.menuDock_Widgets.setTitle(QtWidgets.QApplication.translate("MainWindow", "Dock Widgets", None, -1))
        self.dockWidget_eventlog.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Event Log", None, -1))
        self.dockWidget_process_output.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Subprocess Output", None, -1))
        self.actionQuit.setText(QtWidgets.QApplication.translate("MainWindow", "Quit", None, -1))
        self.actionQuit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Q", None, -1))
        self.actionData_Store.setText(QtWidgets.QApplication.translate("MainWindow", "Data Store", None, -1))
        self.actionDocumentation.setText(QtWidgets.QApplication.translate("MainWindow", "Documentation", None, -1))
        self.actionAbout.setText(QtWidgets.QApplication.translate("MainWindow", "About", None, -1))
        self.actionAbout.setShortcut(QtWidgets.QApplication.translate("MainWindow", "F12", None, -1))
        self.actionAdd_Data_Connection.setText(QtWidgets.QApplication.translate("MainWindow", "Add Data Connection", None, -1))
        self.actionAdd_Data_Store.setText(QtWidgets.QApplication.translate("MainWindow", "Add Data Store", None, -1))
        self.actionAdd_Tool.setText(QtWidgets.QApplication.translate("MainWindow", "Add Tool", None, -1))
        self.actionAdd_View.setText(QtWidgets.QApplication.translate("MainWindow", "Add View", None, -1))
        self.actionSave.setText(QtWidgets.QApplication.translate("MainWindow", "Save", None, -1))
        self.actionSave.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+S", None, -1))
        self.actionSave_As.setText(QtWidgets.QApplication.translate("MainWindow", "Save As...", None, -1))
        self.actionSave_As.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, -1))
        self.actionOpen.setText(QtWidgets.QApplication.translate("MainWindow", "Open...", None, -1))
        self.actionOpen.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+O", None, -1))
        self.actionNew.setText(QtWidgets.QApplication.translate("MainWindow", "New...", None, -1))
        self.actionNew.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+N", None, -1))
        self.actionSettings.setText(QtWidgets.QApplication.translate("MainWindow", "Settings...", None, -1))
        self.actionSettings.setShortcut(QtWidgets.QApplication.translate("MainWindow", "F1", None, -1))
        self.actionItem_Toolbar.setText(QtWidgets.QApplication.translate("MainWindow", "Item Toolbar", None, -1))
        self.actionAdd_Item_Toolbar.setText(QtWidgets.QApplication.translate("MainWindow", "Add Item Toolbar", None, -1))
        self.actionAdd_Item_Toolbar.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Make Add Item Toolbar visible</p></body></html>", None, -1))
        self.actionEvent_Log.setText(QtWidgets.QApplication.translate("MainWindow", "Event Log", None, -1))
        self.actionEvent_Log.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Make Event Log widget visible</p></body></html>", None, -1))
        self.actionSubprocess_Output.setText(QtWidgets.QApplication.translate("MainWindow", "Subprocess Output", None, -1))
        self.actionSubprocess_Output.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Make Subprocess Output widget visible</p></body></html>", None, -1))

from widgets.custom_qtextbrowser import CustomQTextBrowser
import resources_icons_rc
