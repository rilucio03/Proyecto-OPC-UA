import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from msgboxes import msg_boxes
import sqlite3 as sql
import re


class Database_Interface(QMainWindow):
    def __init__(self):
        super(Database_Interface, self).__init__()
        loadUi('Database_Interface.ui', self)
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_list.clicked.connect(self.move_list)
        self.bt_database.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_database))
        self.bt_profile.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_profile))
        self.bt_return.clicked.connect(self.return_to_HMI)
        self.bt_settings.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_settings))
        self.bt_update_database.clicked.connect(self.show_information)
        self.bt_search_profile.clicked.connect(self.search_profile_information)
        self.bt_update_profile.clicked.connect(self.update_profile)
        
        self.table_information.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window
        self.frame_top.mouseMoveEvent = self.move_window
        
        icon_username = QIcon("C:/Python38/Estadias/imagenes/user.svg")
        icon_phone_number = QIcon("C:/Python38/Estadias/imagenes/phone.svg")
        icon_email = QIcon("C:/Python38/Estadias/imagenes/mail.svg")
        icon_password = QIcon("C:/Python38/Estadias/imagenes/lock.svg")
        self.in_username.addAction(icon_username, QLineEdit.LeadingPosition)
        self.in_phone_number.addAction(icon_phone_number, QLineEdit.LeadingPosition)
        self.in_email.addAction(icon_email, QLineEdit.LeadingPosition)
        self.in_new_password.addAction(icon_password, QLineEdit.LeadingPosition)
        self.in_confirm_password.addAction(icon_password, QLineEdit.LeadingPosition)
        
    def control_bt_normal(self):
        self.showNormal()
        self.bt_normal.hide()
        self.bt_maximize.show()
        
    def control_bt_maximize(self):
        self.showMaximized()
        self.bt_maximize.hide()
        self.bt_normal.show()
    
    # SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        
    # Move window
    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()
        
    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()
        if event.globalPos().y() <=10:
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()
    
    def move_list(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animation = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animation.setDuration(500)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extender)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    
    def create_information_table(self):
        conn = sql.connect("Database.db")
        cursor2 = conn.cursor()
        cursor2.execute("""CREATE TABLE IF NOT EXISTS Information (
                        Date_Time integer, 
                        Username text,
                        Employee_code text, 
                        Value_input_1 integer, 
                        Value_input_2 integer, 
                        Value_input_3 integer,
                        Value_input_4 integer, 
                        Observations text)""")
        conn.commit()
        conn.close()
    
    def capture_information(self, date_time, username, employee_code, input_1, input_2, input_3, input_4, observations):
        conn = sql.connect("Database.db")
        cursor2 = conn.cursor()
        capture = f"INSERT INTO Information VALUES ('{date_time}', '{username}', '{employee_code}', '{input_1}', " \
                    f"'{input_2}', '{input_3}', '{input_4}', '{observations}')"
        cursor2.execute(capture)
        conn.commit()
        conn.close()
    
    def show(self):
        conn = sql.connect("Database.db")
        cursor2 = conn.cursor()
        cursor2.execute("SELECT * FROM Information")
        data = cursor2.fetchall()
        return data
    
    def show_information(self):
        info = self.show()
        i = len(info)
        self.table_information.setRowCount(i)
        tablerow = 0
        for row in info:
            self.date_time = row[0]
            self.table_information.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
            self.table_information.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
            self.table_information.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
            self.table_information.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
            self.table_information.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[5]))
            self.table_information.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[6]))
            self.table_information.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[7]))
            self.table_information.setItem(tablerow,7,QtWidgets.QTableWidgetItem(row[8]))
            tablerow += 1
    
    def search_profile_information(self):
        search_password = self.in_password.text()
        
        conn = sql.connect("Database.db")
        cursor2 = conn.cursor()
        cursor2.execute("SELECT * FROM Users WHERE Password = '{}' ".format(search_password))
        codeX = cursor2.fetchall()
        conn.commit()
        conn.close()
        if codeX:
            self.label_name.setText(f'Name: {codeX[0][0]} {codeX[0][1]} {codeX[0][2]}')
            self.label_age.setText(f'Age: {codeX[0][4]} years old')
            self.label_gender.setText(f'Gender: {codeX[0][5]}')
            self.in_username.setText(codeX[0],[3])
            self.in_phone_number.setText(codeX[0],[6])
            self.in_email.setText(codeX[0],[7])
            self.in_new_password.setText(codeX[0],[9])
            self.in_confirm_password.setText(codeX[0],[9])
        else:
            msg_boxes.incorrect_msgbox("ERROR", "The password entered is incorrect.")
    
    def clear_profile_fields(self):
        self.in_username.clear()
        self.in_phone_number.clear()
        self.in_email.clear()
        self.label_name.clear()
        self.label_age.clear()
        self.label_gender.clear()
        self.in_new_password.clear()
        self.confirm_password.clear()
        self.in_password.setText("")
    
    def update_profile(self):
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail\.com$")
        
        search_password = self.in_employee_code.text()
        new_username = self.in_username.text()
        new_phone_number = self.in_phone_number.text()
        new_email = self.in_email.text()
        new_password = self.in_new_password.text()
        confirm_password = self.in_confirm_password.text()
        if len(str(new_username)) == 0:
                msg_boxes.incorrect_msgbox("ERROR", "Please enter a new username.")
        elif len(str(new_phone_number)) != 10:
            msg_boxes.incorrect_msgbox("ERROR", "The phone number entered is incorrect.")
        elif len(str(new_email)) >= 0:
            if email_regex.match(new_email):
                if len(str(new_password)) == 0:
                    msg_boxes.incorrect_msgbox('ERROR', 'For your security, enter a strong password.')
                elif new_password != confirm_password:
                    msg_boxes.incorrect_msgbox('ERROR', 'Please confirm the new password correctly.')
                elif new_password == confirm_password:
                    resp = msg_boxes.warning_msgbox('WARNING', 'Are you sure you want to update your profile information?')
                    if resp == QMessageBox.Yes:
                        self.update(new_username, new_phone_number, new_email, new_password, search_password)
                        msg_boxes.correct_msgbox('SUCCESS', 'Your profile information has been changed successfully.')
                        self.clear_profile_fields()
                    else:
                        msg_boxes.incorrect_msgbox('ERROR', 'Your profile information has not been changed. Try again.')
                else:
                    msg_boxes.incorrect_msgbox('ERROR', 'Something got wrong. Try again.')
            else:
                msg_boxes.incorrect_msgbox('ERROR', 'Invalid email format.')
    
    def update(self, new_username, new_phone_number, new_email, new_password, search_password):
        conn = sql.connect("Database.db")
        cursor2 = conn.cursor()
        cursor2.execute("""UPDATE Users SET Username = '{}', Phone_number = '{}', Email = '{}', Password = '{}'
                        WHERE Password = '{}' """.format(new_username, new_phone_number, new_email, new_password, search_password))
        a = cursor2.rowcount
        conn.commit()
        conn.close()
        return a
    
    def return_to_HMI(self):
        #self.go_to_HMI = HMI()
        #self.go_to_HMI.show()
        self.close()
        

# ------------ Main ------------ #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Database_Interface()
    my_app.show()
    sys.exit(app.exec_())