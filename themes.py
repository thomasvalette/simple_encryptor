#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore


def set_dark_theme(app):
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
    dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
    dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
    dark_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)

    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; } QPushButton { padding: 5px; }")


def set_light_theme(app):
    app.setStyle("Fusion")


def set_ubuntu_theme(app):
    app.setStyle("Fusion")
    
    ubuntu_palette = QtGui.QPalette()
    ubuntu_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 0,50))
    ubuntu_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    ubuntu_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(30, 0, 30))
    ubuntu_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(40, 0, 40))
    ubuntu_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    ubuntu_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    ubuntu_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    ubuntu_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(55, 0, 55))
    ubuntu_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    ubuntu_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    ubuntu_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(230, 230, 230))
    ubuntu_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(150, 150, 150))
    ubuntu_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    ubuntu_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
    ubuntu_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtCore.Qt.darkGray)
    ubuntu_palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtCore.Qt.darkGray)

    app.setPalette(ubuntu_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; } QPushButton { padding: 5px; }")