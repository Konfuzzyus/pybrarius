"""
    Hebi no Shisho - A small scale pythonic library management tool
    Copyright (C) 2013 Christian Meyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4 import QtGui
from hebi_no_shisho.filemaker import importer, conversion, xmlloader

class AdminWindow(QtGui.QDialog):

    def __init__(self, database):
        super(AdminWindow, self).__init__()
        self.__database = database

        self.__tabwidget = QtGui.QTabWidget(self)
        self.__tabwidget.addTab(LibraryReporter(database), "Library")
        self.__tabwidget.addTab(UserBrowser(database), "Users")
        self.__tabwidget.addTab(MediaBrowser(database), "Media")
        self.__tabwidget.addTab(DatabaseAdmin(database), "Database")
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.__tabwidget)
        
        self.setLayout(mainLayout)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Hebi-no-Shisho Administration")
        self.setMinimumSize(160, 160)
        self.resize(480, 320)

    def createActions(self):
        pass

    def createMenus(self):
        pass

class LibraryReporter(QtGui.QWidget):
    def __init__(self, database):
        super(LibraryReporter, self).__init__()
        self.__database = database

class UserBrowser(QtGui.QWidget):
    def __init__(self, database):
        super(UserBrowser, self).__init__()
        self.__database = database
        
        self.importButton = QtGui.QPushButton('Import')
        self.importButton.clicked.connect(self.importUsers)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.importButton)
        self.setLayout(layout)
    
    def importUsers(self):
        filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Select file to Import',
                                                     filter='FileMaker export (*.xml)')
        if filename:
            try:
                loader = xmlloader.FileMakerXMLData(str(filename))
                userimporter = importer.UserDataImporter(self.__database)
                converted = conversion.extract_users(loader.get_data())
                userimporter.import_data(converted)
            except xmlloader.LoadException as e:
                QtGui.QMessageBox.information(self,
                                              'Loading Error',
                                              e,
                                              QtGui.QMessageBox.Ok)


class MediaBrowser(QtGui.QWidget):
    def __init__(self, database):
        super(MediaBrowser, self).__init__()
        self.__database = database
        
        self.importButton = QtGui.QPushButton('Import')
        self.importButton.clicked.connect(self.importMedia)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.importButton)
        self.setLayout(layout)
    
    def importMedia(self):
        filename = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                     caption='Select file to Import',
                                                     filter='FileMaker export (*.xml)')
        if filename:
            try:
                loader = xmlloader.FileMakerXMLData(str(filename))
                mediaimporter = importer.MediaDataImporter(self.__database)
                converted = conversion.extract_media(loader.get_data())
                mediaimporter.import_data(converted)
            except xmlloader.LoadException as e:
                QtGui.QMessageBox.information(self,
                                              'Loading Error',
                                              e,
                                              QtGui.QMessageBox.Ok)
        
class DatabaseAdmin(QtGui.QWidget):
    def __init__(self, database):
        super(DatabaseAdmin, self).__init__()
        self.__database = database
        
        self.importButton = QtGui.QPushButton('Erase Database')
        self.importButton.clicked.connect(self.eraseDatabase)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.importButton)
        self.setLayout(layout)
    
    def eraseDatabase(self):
        answer = QtGui.QMessageBox.question(self,
                                            "Erase Database",
                                            "Clicking Yes will erase the current database.\n"
                                            "This can not be undone, are you sure you want to continue?",
                                            buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            self.__database.erase_database()
            self.topLevelWidget().close()
