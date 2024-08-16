from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class MsgBox(QMessageBox):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(text)
        
    def set_custom_icon(self, q_icon):
        title_icon = QIcon(q_icon)
        self.setWindowIcon(title_icon)
    
    def set_yes_no_buttons(self):
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)


def correct_msgbox(title, text):
    #icon = 'C:/Python38/Estadias/imagenes/check-circle.svg'
    q_icon = 'C:/Python38/Estadias/imagenes/check.svg'
    msg_box = MsgBox(title, text)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.set_custom_icon(q_icon)
    msg_box.exec_()

def incorrect_msgbox(title, text):
    #icon = 'C:/Python38/Estadias/imagenes/x.svg'
    q_icon = 'C:/Python38/Estadias/imagenes/alert-circle.svg'
    msg_box = MsgBox(title, text)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.set_custom_icon(q_icon)
    msg_box.exec_()
    
def warning_msgbox(title, text):
    #icon = 'C:/Python38/Estadias/imagenes/database.svg'
    q_icon = 'C:/Python38/Estadias/imagenes/alert-circle.svg'
    msg_box = MsgBox(title, text)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.set_custom_icon(q_icon)
    msg_box.set_yes_no_buttons()
    resp = msg_box.exec_()
    return resp