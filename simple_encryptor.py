#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Useless program
"""

import sys
import os
import platform
from pathlib import Path, PurePath

from PyQt5 import QtWidgets, QtGui, QtCore

from encryptor import Encryptor


class Encryptor_GUI(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.encryptor = Encryptor("toto")
        
        
    def init_UI(self):               
        self.resize(600, 400)
        self.center()
        
        self.setWindowTitle('Simple Encryptor')  
        self.setWindowIcon(QtGui.QIcon('icon.png')) 

        # global layout for the whole window
        self.layout_global = QtWidgets.QVBoxLayout()

        self.init_key_section()
        self.init_file_explorer()
        self.init_buttons()

        
        self.layout_global.addLayout(self.layout_key)
        self.layout_global.addLayout(self.layout_file_explorer)
        self.layout_global.addLayout(self.layout_buttons)

        self.setLayout(self.layout_global)

        self.show()
        

    def center(self):
        """ Center the main window in the screen based off the window size
        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def init_key_section(self):
        self.label_pwd = QtWidgets.QLabel("Password")

        self.field_pwd = QtWidgets.QLineEdit()
        self.field_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.field_pwd.returnPressed.connect(self.change_pwd)

        self.btn_pwd = QtWidgets.QPushButton("Validate")
        self.btn_pwd.clicked.connect(self.change_pwd)

        self.layout_key = QtWidgets.QGridLayout()
        self.layout_key.addWidget(self.label_pwd,0,0)
        self.layout_key.addWidget(self.field_pwd,0,1)
        self.layout_key.addWidget(self.btn_pwd,0,2)

    
    def change_pwd(self):
        """ Create a new Encryptor object, with a new Fernet key based on password
        """
        self.encryptor = Encryptor(self.field_pwd.text())
        self.field_pwd.clear()


    def init_file_explorer(self):
        self.init_explorer_buttons()
        self.init_file_tree()

        self.layout_file_explorer = QtWidgets.QGridLayout()
        self.layout_file_explorer.addLayout(self.layout_explorer_btn,0,0)
        self.layout_file_explorer.addLayout(self.layout_explorer_tree,1,0)

    def init_explorer_buttons(self):

        self.btn_prev_dir = QtWidgets.QPushButton()
        self.btn_prev_dir.setIcon(QtGui.QIcon("./previous.png"))
        self.btn_prev_dir.clicked.connect(self.previous_directory)

        self.path_viewer = QtWidgets.QLineEdit()

        self.btn_change_dir = QtWidgets.QPushButton(" Change Directory ")
        self.btn_change_dir.clicked.connect(self.change_directory)

        self.layout_explorer_btn = QtWidgets.QGridLayout()
        # adding the tree to the layout
        self.layout_explorer_btn.addWidget(self.btn_prev_dir,0,0)
        self.layout_explorer_btn.addWidget(self.path_viewer,0,1)
        self.layout_explorer_btn.addWidget(self.btn_change_dir,0,2)

    
    def previous_directory(self):
        prev_dir = Path(self.path_viewer.text()).parent
        self.tree.setRootIndex(self.model.index(str(prev_dir)))
        if platform.system() == "windows":
            self.path_viewer.setText(prev_dir.as_posix())
        else:
            self.path_viewer.setText(str(prev_dir))
        


    def change_directory(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_():
            folder = dialog.selectedFiles()[0]
            self.tree.setRootIndex(self.model.index(folder))
            self.path_viewer.setText(folder)


    def init_file_tree(self):
        # layout for the file explorer
        path=QtCore.QDir.currentPath()
        # file system model init
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)
        self.path_viewer.setText(path)

        self.model.setNameFilterDisables(False)
        
        # tree view init and settings
        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(path))
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.tree.setColumnWidth(0,200)
        self.tree.setColumnWidth(1,100)
        self.tree.setColumnWidth(2,100)
        self.tree.setItemsExpandable(False)
        # self.tree.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # event mappers
        self.tree.selectionModel().selectionChanged.connect(self.select_change)
        self.tree.doubleClicked.connect(self.open_file_directory)     
        self.tree.activated.connect(self.open_file_directory)

        self.layout_explorer_tree = QtWidgets.QGridLayout()
        # adding the tree to the layout
        self.layout_explorer_tree.addWidget(self.tree)


    def open_file_directory(self):
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)
        if Path(file_path).is_dir():
            self.tree.setRootIndex(self.model.index(file_path))
            self.path_viewer.setText(file_path)
        else:
            os.startfile(file_path)


    def init_buttons(self):
        self.btn_encrypt = QtWidgets.QPushButton('Encrypt')
        self.btn_encrypt.clicked.connect(self.encrypt)

        self.btn_decrypt = QtWidgets.QPushButton('Decrypt')
        self.btn_decrypt.clicked.connect(self.decrypt)
        
        self.layout_buttons = QtWidgets.QGridLayout()

        self.layout_buttons.addWidget(self.btn_encrypt,0,0)
        self.layout_buttons.addWidget(self.btn_decrypt,0,1)

    
    def select_change(self, selected, deselected):
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        # check file extension
        file_ext = os.path.splitext(file_path)[1]
        if file_ext in [self.encryptor.ext_dir, self.encryptor.ext_file]:
            # activate encrypt button and disable decrypt + style change
            self.btn_encrypt.setEnabled(False)
            self.btn_encrypt.setStyleSheet("background-color:#6e6e6e;")
            self.btn_decrypt.setEnabled(True)
            self.btn_decrypt.setStyleSheet("background-color:#2a82da;")
        else:
            # activate decrypt button and disable encrypt + style change
            self.btn_encrypt.setEnabled(True)
            self.btn_encrypt.setStyleSheet("background-color:#339900;")
            self.btn_decrypt.setEnabled(False)
            self.btn_decrypt.setStyleSheet("background-color:#6e6e6e;")


    def encrypt(self):
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        try:
            if Path(file_path).is_dir():
                self.encryptor.encrypt_directory(file_path)
            elif Path(file_path).is_file():
                self.encryptor.encrypt_file(file_path)
        except:
            QtWidgets.QMessageBox.critical(self, 'Encryption Error', 
            "An error has occured during the encryption.")


    def decrypt(self):
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        try:
            if Path(file_path).suffix == self.encryptor.ext_file:
                self.encryptor.decrypt_file(file_path)
            elif Path(file_path).suffix == self.encryptor.ext_dir:
                self.encryptor.decrypt_directory(file_path)
        except:
            QtWidgets.QMessageBox.critical(self, 'Decryption Error', 
            "An error has occured during the decryption.")
        


        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(230, 230, 230))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(150, 150, 150))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    
    
    enc = Encryptor_GUI()
    sys.exit(app.exec_())