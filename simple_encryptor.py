#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import platform
import secrets
import string
import yaml
from pathlib import Path, PurePath
from PyQt5 import QtWidgets, QtGui, QtCore
from encryptor import Encryptor
from themes import *


class EncryptorGUI(QtWidgets.QMainWindow):
    """Simple encryption / decryption program
    Made with QT GUI and cryptography Fernet lib
    """ 

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # window properties
        self.resize(600, 400)
        self.center()
        self.setWindowTitle('Simple Encryptor')  
        self.setWindowIcon(QtGui.QIcon(resource_path('resource/icon.png')))

        # creating menu
        self.init_menu()

        # create the encryptor widget
        self.encryptor_widget = EncryptorWidget()    
        # set the main widget for the window    
        self.setCentralWidget(self.encryptor_widget)

        # displays the window
        self.show()


    def center(self):
        """Center the main window in the screen based off the window size
        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def init_menu(self):
        """Builds the application menu
        """
        # generate password
        gen_pwd_action = QtWidgets.QAction('Generate Password', self)        
        gen_pwd_action.triggered.connect(self.create_password)

        # generate key file
        gen_key_action = QtWidgets.QAction('Generate Key File', self)        
        gen_key_action.triggered.connect(self.create_key)

        # exit action, closes the program
        exit_action = QtWidgets.QAction('Exit', self)        
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(app.quit)

        # Theme menus
        light_theme_action = QtWidgets.QAction('Light theme', self)        
        light_theme_action.triggered.connect(self.light_theme)
        dark_theme_action = QtWidgets.QAction('Dark theme', self)        
        dark_theme_action.triggered.connect(self.dark_theme)
        ubuntu_theme_action = QtWidgets.QAction('Ubuntu theme', self)        
        ubuntu_theme_action.triggered.connect(self.ubuntu_theme)
        solaris_theme_action = QtWidgets.QAction('Solaris theme', self)        
        solaris_theme_action.triggered.connect(self.solaris_theme)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(gen_pwd_action)
        fileMenu.addAction(gen_key_action)
        fileMenu.addSeparator()
        fileMenu.addAction(exit_action)
        themeMenu = menuBar.addMenu('Theme')
        themeMenu.addAction(light_theme_action)
        themeMenu.addAction(dark_theme_action)
        themeMenu.addAction(ubuntu_theme_action)
        themeMenu.addAction(solaris_theme_action)

    def light_theme(self):
        set_light_theme(app)

    def dark_theme(self):
        set_dark_theme(app)

    def ubuntu_theme(self):
        set_ubuntu_theme(app)

    def solaris_theme(self):
        set_solaris_theme(app)

    def create_password(self):
        """Generates a 30 char long password
        """
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(30))

        QtWidgets.QMessageBox.information(self, "Password generated", 
                "{}".format(password)) 

    def create_key(self):
        self.encryptor_widget.create_key()


class EncryptorWidget(QtWidgets.QWidget):
    """Encryptor widget, contains all the needed widgets to encrypt/decrypt
    """ 

    def __init__(self):
        """Initializes widget
        """  
        super().__init__()
           
        # global layout for the whole widget 
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

        # create encryptor object for crypt/decrypt operations
        self.encryptor = Encryptor()

    def init_key_section(self):
        """Initiates the key section
        This contains the password typing field, key file load
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
        self.btn_prev_dir.setIcon(QtGui.QIcon(resource_path("resource/previous.png")))
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

    def change_pwd(self):
        """Changes Encryptor key, with a new Fernet key based on password
        """
        if self.field_pwd.text() == "":
            self.label_chg_pwd.setText("Password cannot be empty")
            return None
        self.encryptor.set_key_from_password(self.field_pwd.text())
        self.label_chg_pwd.setText("Password typed")
        self.label_chg_pwd.setStyleSheet("color:#01ac2d")
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
                self.label_chg_key.setStyleSheet("color:#01ac2d")
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
            # activate encrypt button and disable decrypt
            self.btn_encrypt.setEnabled(False)
            self.btn_decrypt.setEnabled(True)
        else:
            # activate decrypt button and disable encrypt
            self.btn_encrypt.setEnabled(True)
            self.btn_decrypt.setEnabled(False)

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
    

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller 
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# MAIN  
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    
    # theme
    app.setStyle("Fusion")
    config = yaml.safe_load(open("config.yml"))
    theme = config["default_theme"]

    if theme == "light":
        set_light_theme(app)
    elif theme == "dark":
        set_dark_theme(app)
    elif theme == "ubuntu":
        set_ubuntu_theme(app)
    elif theme == "solaris":
        set_solaris_theme(app)
    else:
        set_light_theme(app)
   
    # launch GUI
    enc = EncryptorGUI()
    sys.exit(app.exec_())
