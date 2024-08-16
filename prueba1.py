# ---------- Libraries ---------- #
import sys
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
import cv2
import numpy as np
import imutils
import sqlite3 as sql
from msgboxes import msg_boxes
import time
import datetime
import pyqrcode
import png
from pyqrcode import QRCode
from pyzbar.pyzbar import decode
import pyqtgraph as pg
from PIL import Image
import opcua
import opcuawebclient
import re
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

# ----- Global variables ----- #
data1 = np.array([0])
data2 = np.array([0])
data3 = np.array([0])
data4 = np.array([0])

# --- Connection to database (users) --- #
try:
    con = sql.connect("Database.db")
    con.commit()
    con.close()
except:
    msg_boxes.incorrect_msgbox('ERROR', 'Cannot access database.')

# ----- Email conection ----- #
load_dotenv()
email_sender = "rluciof042003@gmail.com"
email_password = os.getenv("PASSWORD")
email_receiver = ""

# ------------------------------------------------------------------------------------------------------------- #

class Login_Screen(QMainWindow):
    def __init__(self):
        super(Login_Screen, self).__init__()
        loadUi('Login_Interface.ui', self)
        self.GUI_Form = User_Form()
        self.GUI_Form.create_user_table()
        self.Database_Screen = Database_Interface()
        self.Database_Screen.create_information_table()
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_login.clicked.connect(self.Login)
        self.bt_register.clicked.connect(self.newUser_access)
        self.bt_recover.clicked.connect(self.access_to_recover_account)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window
        self.frame_title.mouseMoveEvent = self.move_window
        
        icon_user = QIcon("C:/Python38/Estadias/imagenes/user.svg")
        icon_password = QIcon("C:/Python38/Estadias/imagenes/lock.svg")
        self.in_username.addAction(icon_user, QLineEdit.LeadingPosition)
        self.in_password.addAction(icon_password, QLineEdit.LeadingPosition)
        
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
        if event.globalPos().y() <=5 or event.globalPos().x() <=5 :
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()
    
    def Login(self):
        username = self.in_username.text()
        password = self.in_password.text()
        
        if len(str(username))==0 or len(str(password))==0:
            self.label_message.setText("Enter all necessary data.")
        else:
            try:
                con = sql.connect("Database.db")
                cursor = con.cursor()
                cursor.execute('SELECT Username, Password FROM Users WHERE Username = ? AND Password = ?',(username, password))
                if cursor.fetchall():
                    self.access_to_HMI()
                    self.in_username.clear()
                    self.in_password.clear()
                    self.label_message.clear()
                else:
                    msg_boxes.incorrect_msgbox('ERROR', 'The username and/or password are incorrect. Try again.')
            except sql.Error as error:
                print("Error....", error)
    
    def access_to_HMI(self):
        self.go_to_HMI = HMI()
        self.go_to_HMI.show()
        self.close()
    
    def access_to_recover_account(self):
        self.go_to_recover_account = Forgotten_Account()
        self.go_to_recover_account.show()
        self.close()
    
    def newUser_access(self):
        self.go_to_permission_screen = Permission_Screen()
        self.go_to_permission_screen.show()
        self.close()


class Forgotten_Account(QMainWindow):
    def __init__(self):
        super(Forgotten_Account, self).__init__()
        loadUi('Recover_account_Interface.ui', self)
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_confirm.clicked.connect(self.recover_password)
        self.bt_return.clicked.connect(self.return_to_login)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window
        self.frame_title.mouseMoveEvent = self.move_window
        
        icon_employee_code = QIcon("C:/Python38/Estadias/imagenes/search.svg")
        self.in_employee_code.addAction(icon_employee_code, QLineEdit.LeadingPosition)
        
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
        if event.globalPos().y() <=5 or event.globalPos().x() <=5 :
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()
    
    def recover_password(self):
        global email_sender, email_receiver, email_password
        employee_code_to_search = self.in_employee_code.text()
        con = sql.connect("Database.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Users WHERE Employee_code = '{}' ".format(employee_code_to_search))
        user_x = cursor.fetchall()
        con.commit()
        con.close()
        if user_x:
            email_receiver = f'{user_x[0][7]}'
            subject = "ACCOUNT RECOVERY"
            body = f'Username: {user_x[0][3]} \nPassword: {user_x[0][9]}'
            
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_receiver
            em["Subject"] = subject
            em.set_content(body)
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                msg_boxes.correct_msgbox('SUCCESS', 'The email was sent.')
                self.in_employee_code.clear()
        else:
            msg_boxes.incorrect_msgbox('ERROR', 'The data entered is incorrect.')
    
    def return_to_login(self):
        self.go_to_login = Login_Screen()
        self.go_to_login.show()
        self.close()


class Permission_Screen(QMainWindow):
    def __init__(self):
        super(Permission_Screen, self).__init__()
        loadUi('Permission_Interface.ui', self)
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_on.clicked.connect(self.start_video)
        self.bt_off.clicked.connect(self.stop_video)
        self.bt_return.clicked.connect(self.return_window)
        self.bt_confirm.clicked.connect(self.confirm_access)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window 
        self.frame_title.mouseMoveEvent = self.move_window
        
        # --- QR Code --- #
        self.qr_thread = QRReaderThread()
        self.qr_thread.qrDetected.connect(self.update_info_label)
    
    def start_video(self):
        self.qr_thread.start()
        self.qr_thread.Imageupd.connect(self.Imageupd_slot)
    
    def update_info_label(self, data):
        masked_data = '*' * len(data)
        self.label_code.setText(masked_data)
        self.qr_data = data
    
    def Imageupd_slot(self, Image):
        self.label_camera.setPixmap(QPixmap.fromImage(Image))
    
    def stop_video(self):
        self.qr_thread.stop_video()
        self.label_camera.clear()
    
    def confirm_access(self):
        pattern = re.compile(r'^A-\d{4}$')
        if pattern.match(self.qr_data):
            self.qr_thread.stop_video()
            self.go_to_registration = User_Form()
            self.go_to_registration.show()
            self.label_code.setText("")
            self.close()
        
        else:
            pass
    
    def return_window(self):
        self.qr_thread.stop_video()
        self.return_to_login = Login_Screen()
        self.return_to_login.show()
        self.close()
  
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
        if event.globalPos().y() <=5 or event.globalPos().x() <=5 :
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()


class QRReaderThread(QThread):
    Imageupd = pyqtSignal(QImage)
    qrDetected = pyqtSignal(str)
    
    def run(self):
        self.running_thread = True
        cap = cv2.VideoCapture(0) 
        
        while self.running_thread:
            ret, self.frame = cap.read()
            # -- Read QR -- #
            for codes in decode(self.frame):
                #information = codes.data.decode('utf-$')    # decode
                #information = information[0:]
                #information = str(information)
                
                # --- Decode --- #
                information = codes.data.decode('utf-8')
                
                # --- Type of employee --- #
                type_employee = information[0:2]
                type_employee = int(type_employee)
                
                # - Extract coordinates - #
                pos = np.array([codes.polygon], np.int32)
                xi, yi = codes.rect.left, codes.rect.top
                
                # - Resize - #
                pos = pos.reshape((-1, 1, 2))
                
                if type_employee == 65:    # A -> 65 (Manager)
                    # --- Draw --- #
                    cv2.polylines(self.frame, [pos], True, (255, 0, 0), 5)
                    cv2.putText(self.frame, 'Manager', (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    time.sleep(0.2)
                    information = str(f"A-{information[2:]}")
                    self.qrDetected.emit(information)
                
                if type_employee == 66:    # B -> 66 (Production)
                    # --- Draw --- #
                    cv2.polylines(self.frame, [pos], True, (0, 255, 0), 5)
                    cv2.putText(self.frame, 'Production', (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    time.sleep(0.2)
                    information = str(f"B-{information[2:]}")
                    self.qrDetected.emit(information)
                
                if type_employee == 67:    # C -> 67 (Maintenance)
                    # --- Draw --- #
                    cv2.polylines(self.frame, [pos], True, (0, 0, 255), 5)
                    cv2.putText(self.frame, 'Maintenance', (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    time.sleep(0.2)
                    information = str(f"C-{information[2:]}")
                    self.qrDetected.emit(information)
                
                else:
                    pass

                # -- Draw -- #
                #cv2.polylines(self.frame, [pos], True, (255, 128, 0), 5)
                #time.sleep(0.2)
                #self.qrDetected.emit(information)
    
            if ret:
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                convertir_qt = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                pic = convertir_qt.scaled(700, 500, Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)
        cap.release()
        
    def stop_video(self):
        self.running_thread = False
        self.quit()


class User_Form(QMainWindow):
    def __init__(self):
        super(User_Form, self).__init__()
        loadUi('Users_Form.ui', self)
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_create.clicked.connect(self.data)
        self.bt_cancel.clicked.connect(self.cancel)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window
        self.frame_title.mouseMoveEvent = self.move_window
        icon_name = QIcon("C:/Python38/Estadias/imagenes/user.svg")
        icon_user = QIcon("C:/Python38/Estadias/imagenes/user-check.svg")
        icon_phone = QIcon("C:/Python38/Estadias/imagenes/phone.svg")
        icon_email = QIcon("C:/Python38/Estadias/imagenes/mail.svg")
        icon_ecode = QIcon("C:/Python38/Estadias/imagenes/hash.svg")
        icon_password = QIcon("C:/Python38/Estadias/imagenes/lock.svg")
        self.in_name.addAction(icon_name, QLineEdit.LeadingPosition)    #QLineEdit.TrailingPosition
        self.in_lastname.addAction(icon_name, QLineEdit.LeadingPosition)
        self.in_lastname2.addAction(icon_name, QLineEdit.LeadingPosition)
        self.in_user.addAction(icon_user, QLineEdit.LeadingPosition)
        self.in_phone.addAction(icon_phone, QLineEdit.LeadingPosition)
        self.in_email.addAction(icon_email, QLineEdit.LeadingPosition)
        self.in_employee_code.addAction(icon_ecode, QLineEdit.LeadingPosition)
        self.in_password.addAction(icon_password, QLineEdit.LeadingPosition)
        self.in_password2.addAction(icon_password, QLineEdit.LeadingPosition)
        
        int_validator = QIntValidator()
        self.in_phone.setValidator(int_validator)
        
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
        if event.globalPos().y() <=5 or event.globalPos().x() <=5 :
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()
    
    def create_user_table(self):
        con = sql.connect("Database.db")
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users (Name text, Middle_name text,
                    Last_name text, Username text, Age integer, Gender text, Phone_number integer, 
                    Email text, Employee_code text, Password text)""")
        con.commit()
        con.close()
    
    def register(self, name, mn, ln, username, age, gender, phone_number, email, employee_code, password):
        con = sql.connect("Database.db")
        cursor = con.cursor()
        instruction = f"INSERT INTO Users VALUES ('{name}', '{mn}', '{ln}', '{username}', " \
                    f"'{age}', '{gender}', '{phone_number}', '{email}', '{employee_code}', '{password}')"
        cursor.execute(instruction)
        con.commit()
        con.close()
    
    def clear_lineEdit(self):
        self.in_name.setText("")
        self.in_lastname.setText("")
        self.in_lastname2.setText("")
        self.in_user.setText("")
        self.in_age.setValue(0)
        self.in_gender.clear()
        self.in_phone.setText("")
        self.in_email.setText("")
        self.in_employee_code.setText("")
        self.in_password.setText("")
        self.in_password2.setText("")
    
    def data(self):
        # Define the regex pattern
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail\.com$")
        code_regex = re.compile(r"^[ABC]-\d{4}$")
        
        name = self.in_name.text()
        mn = self.in_lastname.text()
        ln = self.in_lastname2.text()
        username = self.in_user.text()
        age = self.in_age.value()
        gender = str(self.in_gender.currentText())
        phone_number = self.in_phone.text()
        email = self.in_email.text()
        employee_code = self.in_employee_code.text()
        password = self.in_password.text()
        confirm_password = self.in_password2.text()
        if len(str(name)) == 0:
            msg_boxes.incorrect_msgbox("ERROR", "Please enter your name.")
        elif len(str(mn)) == 0:
            msg_boxes.incorrect_msgbox("ERROR", "Please enter your middle name.")
        elif len(str(ln)) == 0:
            msg_boxes.incorrect_msgbox("ERROR", "Please enter your last name.")
        elif len(str(username)) == 0:
            msg_boxes.incorrect_msgbox("ERROR", "Please enter a username.")
        elif age < 18:
            msg_boxes.incorrect_msgbox("ERROR", "The user must be of legal age to have access to the controls.")
        elif str(gender) == "":
            msg_boxes.incorrect_msgbox("ERROR", "Please indicate your gender.")
        elif len(str(phone_number)) != 10:
            msg_boxes.incorrect_msgbox("ERROR", "The phone number entered is incorrect.")
        elif len(str(email)) >= 0:
            if email_regex.match(email):
                if len(str(employee_code)) >= 0:
                    if code_regex.match(employee_code):
                        if len(str(password)) == 0:
                            msg_boxes.incorrect_msgbox("ERROR", "Please enter a secure password.")
                        elif password != confirm_password:
                            msg_boxes.incorrect_msgbox("ERROR", "Password doesn't match.")
                        elif password == confirm_password:
                            self.register(name, mn, ln, username, age, gender, phone_number, email, employee_code, password)
                            msg_boxes.correct_msgbox("SUCCESS", "The new user has successfully registered.")
                            self.clear_lineEdit()
                        else:
                            resp = msg_boxes.warning_msgbox("WARNING", "Something went wrong. Do you want to try again?")
                            if resp == QMessageBox.No:
                                self.clear_lineEdit()
                                self.cancel()
                    else:
                        msg_boxes.incorrect_msgbox('ERROR', 'Invalid employee code format.')
            else:
                msg_boxes.incorrect_msgbox('ERROR', 'Invalid email format.')
    
    def cancel(self):
        self.clear_lineEdit()
        self.go_to_login = Login_Screen()
        self.go_to_login.show()
        self.close()


class HMI(QMainWindow):
    def __init__(self):
        super(HMI, self).__init__()
        loadUi('HMI.ui', self)
        
        self.bt_normal.hide()
        self.click_posicion = None
        self.bt_minimize.clicked.connect(lambda: self.showMinimized())
        self.bt_normal.clicked.connect(self.control_bt_normal)
        self.bt_maximize.clicked.connect(self.control_bt_maximize)
        self.bt_close.clicked.connect(lambda: self.close())
        
        self.bt_logout.clicked.connect(self.Logout)
        self.bt_go_to_database.clicked.connect(self.go_Database)
        self.bt_screenshot.clicked.connect(self.Screenshot)
        self.graph1.valueChanged.connect(self.update_plot1)
        self.graph2.valueChanged.connect(self.update_plot2)
        self.graph3.valueChanged.connect(self.update_plot3)
        self.graph4.valueChanged.connect(self.update_plot4)
        
        # Delete title bar and opacity
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # Move window
        self.frame_title.mouseMoveEvent = self.move_window
        
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
        if event.globalPos().y() <=5 or event.globalPos().x() <=5 :
            self.showMaximized()
            self.bt_maximize.hide()
            self.bt_normal.show()
        else:
            self.showNormal()
            self.bt_normal.hide()
            self.bt_maximize.show()
    
    def Logout(self):
        self.logout = Login_Screen()
        self.logout.show()
        self.close()
    
    def go_Database(self):
        self.go_to_database = Database_Interface()
        self.go_to_database.show()
        self.showMinimized()
        
    def Screenshot(self):
        # Get the screen where the window is located
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        
        # Generate a filename with the current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"screenshot_{timestamp}.png"
        
        # Open a file dialog to save the screenshot
        file_dialog = QFileDialog(self)
        file_dialog.setWindowIcon(QIcon("C:/Python38/Estadias/imagenes/save.svg"))
        file_dialog.setDefaultSuffix("png")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save Screenshot",
            QDir.homePath() + '/' + default_filename,
            "PNG Files (*.png);;All Files (*)",
            options=options
        )
        
        if file_path:
            screenshot.save(file_path, "png")
    
    def update_plot1(self):
        global data1
        new_value1 = self.graph1.value()
        data1 = np.append(data1, new_value1)
        self.Num1.display(new_value1)
        self.plot_all()

    def update_plot2(self):
        global data2
        new_value2 = self.graph2.value()
        data2 = np.append(data2, new_value2)
        self.Num2.display(new_value2)
        self.plot_all()

    def update_plot3(self):
        global data3
        new_value3 = self.graph3.value()
        data3 = np.append(data3, new_value3)
        self.Num3.display(new_value3)
        self.plot_all()
        
    def update_plot4(self):
        global data4
        new_value4 = self.graph4.value()
        data4 = np.append(data4, new_value4)
        self.Num4.display(new_value4)
        self.plot_all()

    def plot_all(self):
        self.graphWidget.plot(data1, pen='r')
        self.graphWidget.plot(data2, pen='g')
        self.graphWidget.plot(data3, pen='b')
        self.graphWidget.plot(data4, pen='y')


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
        #self.bt_update_database.clicked.connect(self.show_information)
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
        
        icon_search = QIcon("C:/Python38/Estadias/imagenes/search.svg")
        icon_username = QIcon("C:/Python38/Estadias/imagenes/user.svg")
        icon_phone_number = QIcon("C:/Python38/Estadias/imagenes/phone.svg")
        icon_email = QIcon("C:/Python38/Estadias/imagenes/mail.svg")
        icon_password = QIcon("C:/Python38/Estadias/imagenes/lock.svg")
        self.in_password.addAction(icon_search, QLineEdit.LeadingPosition)
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
            self.animation.setDuration(300)
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
    
    #def show(self):
        #conn = sql.connect("Database.db")
        #cursor2 = conn.cursor()
        #cursor2.execute("SELECT * FROM Information")
        #data = cursor2.fetchall()
        #return data
    
    #def show_information(self):
     #   info = self.show()
      #  i = len(info)
       # self.table_information.setRowCount(i)
        #tablerow = 0
        #for row in info:
         #   self.date_time = row[0]
          #  self.table_information.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[1]))
           # self.table_information.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[2]))
            #self.table_information.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[3]))
            #self.table_information.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row[4]))
            #self.table_information.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row[5]))
            #self.table_information.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row[6]))
            #self.table_information.setItem(tablerow,6,QtWidgets.QTableWidgetItem(row[7]))
            #self.table_information.setItem(tablerow,7,QtWidgets.QTableWidgetItem(row[8]))
            #tablerow += 1
    
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
            self.in_username.setText(f'{codeX[0][3]}')
            self.in_phone_number.setText(f'{codeX[0][6]}')
            self.in_email.setText(f'{codeX[0][7]}')
            self.in_new_password.setText(f'{codeX[0][9]}')
            self.in_confirm_password.setText(f'{codeX[0][9]}')
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
        self.in_confirm_password.clear()
        self.in_password.setText("")
    
    def update_profile(self):
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail\.com$")
        
        search_password = self.in_password.text()
        new_username = self.in_username.text()
        new_phone_number = self.in_phone_number.text()
        new_email = self.in_email.text()
        new_password = self.in_new_password.text()
        confirm_password = self.in_confirm_password.text()
        if len(str(search_password)) != 0:
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
                            msg_boxes.correct_msgbox('WARNING', 'Your profile information has not been changed.')
                            self.clear_profile_fields()
                    else:
                        msg_boxes.incorrect_msgbox('ERROR', 'Something got wrong. Try again.')
                else:
                    msg_boxes.incorrect_msgbox('ERROR', 'Invalid email format.')
        else:
            msg_boxes.incorrect_msgbox('ERROR', 'Search your profile information before editing it.')
    
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
    my_app = Login_Screen()
    my_app.show()
    sys.exit(app.exec_())