#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import platform
from pathlib import Path, PurePath
from PyQt5 import QtWidgets, QtGui, QtCore
from encryptor import Encryptor


class Encryptor_GUI(QtWidgets.QWidget):
    """Simple encryption / decryption program
    Made with QT GUI and cryptography Fernet lib
    """ 

    def __init__(self):
        super().__init__()
        self.init_UI()
        # create encryptor object for crypt/decrypt operations
        self.encryptor = Encryptor()
        
        
    def init_UI(self):
        """Initialize GUI
        """               
        self.resize(600, 400)
        self.center()
        
        self.setWindowTitle('Simple Encryptor')  
        self.setWindowIcon(QtGui.QIcon('icon.png')) 

        # global layout for the whole window
        self.layout_global = QtWidgets.QVBoxLayout()

        # generate sub layouts
        self.init_key_section()
        self.init_file_explorer()
        self.init_buttons()
    
        # add the layouts to the window
        self.layout_global.addLayout(self.layout_key)
        self.layout_global.addLayout(self.layout_file_explorer)
        self.layout_global.addLayout(self.layout_buttons)
        self.setLayout(self.layout_global)

        # show window
        self.show()
        

    def init_key_section(self):
        """Initiates the key section
        This contains the password typing field, key file load and generation
        """
        # password section
        self.label_pwd = QtWidgets.QLabel("Password")

        self.field_pwd = QtWidgets.QLineEdit()
        self.field_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.field_pwd.returnPressed.connect(self.change_pwd)

        self.btn_pwd = QtWidgets.QPushButton("Change password")
        self.btn_pwd.clicked.connect(self.change_pwd)

        self.label_chg_pwd = QtWidgets.QLabel("No password typed")
        self.label_chg_pwd.setStyleSheet("color:#FA5858")

        # key file section
        self.label_key = QtWidgets.QLabel("Key file")

        self.field_key = QtWidgets.QLineEdit()
        self.field_key.setReadOnly(True)

        self.btn_gen = QtWidgets.QPushButton("Create key file")
        self.btn_gen.clicked.connect(self.create_key)

        self.btn_key = QtWidgets.QPushButton("Load key")
        self.btn_key.clicked.connect(self.change_key)

        self.label_chg_key = QtWidgets.QLabel("No key loaded")
        self.label_chg_key.setStyleSheet("color:#FA5858")

        # creating layout
        self.layout_key = QtWidgets.QGridLayout()
        self.layout_key.addWidget(self.label_pwd,0,0)
        self.layout_key.addWidget(self.field_pwd,1,0)
        self.layout_key.addWidget(self.btn_pwd,1,1)
        self.layout_key.addWidget(self.label_chg_pwd,2,0)
        self.layout_key.addWidget(self.label_key,0,3)
        self.layout_key.addWidget(self.field_key,1,3)
        self.layout_key.addWidget(self.btn_gen,0,4)
        self.layout_key.addWidget(self.btn_key,1,4)
        self.layout_key.addWidget(self.label_chg_key,2,3)
        self.layout_key.setColumnMinimumWidth(1,110)
        self.layout_key.setColumnMinimumWidth(2,50)
        self.layout_key.setColumnMinimumWidth(4,110)
        self.layout_key.setRowMinimumHeight(3,20)
    

    def init_file_explorer(self):
        """Initiate the file explorer, which contains
        - an explorer button and current path field
        - a file tree for the current path
        """
        # initiate both sub layouts
        self.init_explorer_buttons()
        self.init_file_tree()

        # add them to the file explorer layout
        self.layout_file_explorer = QtWidgets.QGridLayout()
        self.layout_file_explorer.addLayout(self.layout_explorer_btn,0,0)
        self.layout_file_explorer.addLayout(self.layout_explorer_tree,1,0)


    def init_explorer_buttons(self):
        """Initiate the file explorer buttons
        """
        self.btn_prev_dir = QtWidgets.QPushButton()
        self.btn_prev_dir.setIcon(QtGui.QIcon("./previous.png"))
        self.btn_prev_dir.clicked.connect(self.previous_directory)

        self.path_viewer = QtWidgets.QLineEdit()
        self.path_viewer.setReadOnly(True)

        self.btn_change_dir = QtWidgets.QPushButton("Change Directory")
        self.btn_change_dir.clicked.connect(self.change_directory)

        self.layout_explorer_btn = QtWidgets.QGridLayout()
        # adding the tree to the layout
        self.layout_explorer_btn.addWidget(self.btn_prev_dir,0,0)
        self.layout_explorer_btn.addWidget(self.path_viewer,0,1)
        self.layout_explorer_btn.addWidget(self.btn_change_dir,0,2)

        self.layout_explorer_btn.setColumnMinimumWidth(2,110)


    def init_file_tree(self):
        """Initiate the file tree itself
        """
        # layout for the file explorer
        path=QtCore.QDir.currentPath()
        path="C:/valette/files/dev/cypherTests"
        # file system model init
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)
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

        # set path
        self.set_new_path(path)

        # event mappers
        self.tree.selectionModel().selectionChanged.connect(self.select_change)
        self.tree.doubleClicked.connect(self.open_file_directory)     
        self.tree.activated.connect(self.open_file_directory)

        # adding the tree to the layout
        self.layout_explorer_tree = QtWidgets.QGridLayout()
        self.layout_explorer_tree.addWidget(self.tree)


    def init_buttons(self):
        """Initiate the encrypt/decrypt buttons layout
        """
        self.btn_encrypt = QtWidgets.QPushButton('Encrypt')
        self.btn_encrypt.clicked.connect(self.encrypt)
        self.btn_encrypt.setEnabled(False)

        self.btn_decrypt = QtWidgets.QPushButton('Decrypt')
        self.btn_decrypt.clicked.connect(self.decrypt)
        self.btn_decrypt.setEnabled(False)            

        self.layout_buttons = QtWidgets.QGridLayout()

        self.layout_buttons.addWidget(self.btn_encrypt,0,0)
        self.layout_buttons.addWidget(self.btn_decrypt,0,1)


    def center(self):
        """Center the main window in the screen based off the window size
        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def change_pwd(self):
        """Changes Encryptor key, with a new Fernet key based on password
        """
        self.encryptor.set_key_from_password(self.field_pwd.text())
        self.label_chg_pwd.setText("Password typed")
        self.label_chg_pwd.setStyleSheet("color:#01DF3A")
        self.label_chg_key.clear()
        self.field_key.clear()
        QtWidgets.QMessageBox.information(self, "Password Change", 
            ("Your password has been successfully changed.\n\n"
             "You can now encrypt / decrypt files."))


    def create_key(self):
        """Create key file using Encryptor function
        This key file can be used later for encrypt/decrypt
        """
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("Any files (*.key)")
        if dialog.exec_():
            key_file = dialog.selectedFiles()[0]
            self.encryptor.generate_key_file("{}.key".format(key_file))
            QtWidgets.QMessageBox.information(self, "Key File Generation", 
                    ("Your key file has been successfully generated.\n\n"
                     "You can load it to encrypt / decrypt."))


    def change_key(self):
        """Changes Encryptor key, with a new Fernet key from the file 
        """    
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        if dialog.exec_():
            key_file = dialog.selectedFiles()[0]
            
            # load key file and create new Encryptor object
            try:
                self.encryptor.set_key_from_keyfile(key_file)
                # set field content
                self.field_key.setText(Path(key_file).name)
                self.label_chg_key.setText("Key loaded")
                self.label_chg_key.setStyleSheet("color:#01DF3A")
                self.field_pwd.clear()
                self.label_chg_pwd.clear()
                QtWidgets.QMessageBox.information(self, "Key File Change", 
                    ("Your key file has been successfully loaded.\n\n"
                     "You can now encrypt / decrypt files."))
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "File Loading Error", 
                "An error has occured during file loading:\n\n{}".format(repr(e)))  

   
    def previous_directory(self):
        """Is launched when the 'previous' button is clicked
        Change the current path to the previous directory
        """
        prev_dir = Path(self.path_viewer.text()).parent
        self.set_new_path(str(prev_dir))
        

    def change_directory(self):
        """Is launched when the 'change dir' button is clicked
        Change the current path to the one selected
        """
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        if dialog.exec_():
            folder = dialog.selectedFiles()[0]
            self.tree.setRootIndex(self.model.index(folder))
            self.path_viewer.setText(folder)
    

    def select_change(self, selected, deselected):
        """Is fired every time a new item in the tree is selected
        Enable/Disable 'encrypt' and 'decrypt' buttons and change their colors
        """
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        # check file extension
        file_ext = os.path.splitext(file_path)[1]
        if file_ext in [self.encryptor.ext_dir, self.encryptor.ext_file]:
            # activate encrypt button and disable decrypt + style change
            self.btn_encrypt.setEnabled(False)
            self.btn_encrypt.setStyleSheet("background-color:#353535;")
            self.btn_decrypt.setEnabled(True)
            self.btn_decrypt.setStyleSheet("background-color:#339900;")
        else:
            # activate decrypt button and disable encrypt + style change
            self.btn_encrypt.setEnabled(True)
            self.btn_encrypt.setStyleSheet("background-color:#2a82da;")
            self.btn_decrypt.setEnabled(False)
            self.btn_decrypt.setStyleSheet("background-color:#353535;")


    def open_file_directory(self):
        """Opens file or directory depending on current selection
        If the selection is a directory, it changes the working path
        If the selection is a file, it tries to open it with the system default
        """
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)
        if Path(file_path).is_dir():
            self.set_new_path(file_path)
        else:
            try:
                os.startfile(file_path)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "File Error", 
                "The system cannot open this file:\n\n{}".format(repr(e)))


    def set_new_path(self, path):
        """Changes the current path used, and set the field accordingly
        """
        path = Path(path)
        self.tree.setRootIndex(self.model.index(str(path)))
        # to display correcly / on windows and \ everywhere else
        if platform.system() == "windows":
            self.path_viewer.setText(path.as_posix())
        else:
            self.path_viewer.setText(str(path))


    def encrypt(self):
        """Uses the encryptor object to encrypt selected file or folder
        If the selection is a folder, its content is first added to a tar,
        and then encrypted
        """
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        try:
            if Path(file_path).is_dir():
                self.encryptor.encrypt_directory(file_path)
            elif Path(file_path).is_file():
                self.encryptor.encrypt_file(file_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Encryption Error", 
            "An error has occured during the encryption:\n\n{}".format(repr(e)))


    def decrypt(self):
        """Uses the encryptor object to decrypt selected file
        If the file is a tar archive, its content is unpacked after decryption
        """
        index = self.tree.currentIndex()
        file_path = self.model.filePath(index)

        try:
            if Path(file_path).suffix == self.encryptor.ext_file:
                self.encryptor.decrypt_file(file_path)
            elif Path(file_path).suffix == self.encryptor.ext_dir:
                self.encryptor.decrypt_directory(file_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Decryption Error", 
            "An error has occured during the decryption:\n\n{}".format(repr(e)))
    

# MAIN  
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    # DARK THEME
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
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; } QPushButton { padding: 5px; }")
    
    # 
    enc = Encryptor_GUI()
    sys.exit(app.exec_())