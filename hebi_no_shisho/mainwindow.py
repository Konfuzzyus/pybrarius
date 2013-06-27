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

class MainWindow(QtGui.QMainWindow):

    def __init__(self, database):
        super(MainWindow, self).__init__()
        self.__database = database

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Hebi-no-Shisho")
        self.setMinimumSize(160, 160)
        self.resize(480, 320)

    def createActions(self):
        self.actAdmin = QtGui.QAction("Administration",
                                      self,
                                      statusTip="Enter database administration mode",
                                      triggered=self.startAdministration)

        self.actExit = QtGui.QAction("&Quit",
                                     self,
                                     shortcut="Ctrl+Q",
                                     statusTip="Quit the application",
                                     triggered=self.close)

        self.actAbout = QtGui.QAction("About",
                                      self,
                                      statusTip="About Hebi-no-Shisho",
                                      triggered=self.showAbout)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.actAdmin)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

    def startAdministration(self):
        diag = QtGui.QInputDialog()
        
        if self.__database.is_valid():
            prompt = "Enter password for existing database:"
            action = self.useExistingDatabase
        else:
            prompt = "No valid database found, enter a password to create a new database:"
            action = self.createNewDatabase
        entered_password, ok = diag.getText(self,
                                 "Administration Mode",
                                 prompt,
                                 mode=QtGui.QLineEdit.Password)
        if ok:
            action(entered_password)
    
    def useExistingDatabase(self, password):
        if self.__database.check_password(str(password)):
            print "Password accepted"
        else:
            QtGui.QMessageBox.information(self,
                                          "Access denied",
                                          "Invalid password entered",
                                          QtGui.QMessageBox.Ok)
        
    def createNewDatabase(self, new_password):
        diag = QtGui.QInputDialog()
        entered_password, ok = diag.getText(self,
                                 "Administration Mode",
                                 "Please re-enter your password to confirm creation of the database:",
                                 mode=QtGui.QLineEdit.Password)
        if ok:
            if new_password == entered_password:
                self.__database.reset_database(str(new_password))
                print "Database reset"
            else:
                QtGui.QMessageBox.information(self,
                                          "Database creation failure",
                                          "The passwords you entered did not match.",
                                          QtGui.QMessageBox.Ok)

    def showAbout(self):
        QtGui.QMessageBox.about(self,
                                "About Shisho-no-Hebi")
