# ---------- Libraries ---------- #

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

import sys
sys.path.insert(0, "..")
from opcua import Client
from opcua import ua


# ----- Global variables ----- #
data1 = np.array([0])
data2 = np.array([0])
data3 = np.array([0])
data4 = np.array([0])
client = Client("opc.tcp://192.168.0.1:4841")
# client = Client("opc.tcp://admin:clave@192.168.0.1:4841") #connect using a user


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
        
        #self.bt_logout.clicked.connect(self.Logout)
        #self.bt_go_to_database.clicked.connect(self.go_Database)
        self.bt_screenshot.clicked.connect(self.Screenshot)
        self.graph1.valueChanged.connect(self.update_plot1) # botones
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
    
 #   def Logout(self):
  #      self.logout = Login_Screen()
   #     self.logout.show()
    #    self.close()
    
    #def go_Database(self):
     #   self.go_to_database = Database()
      #  self.go_to_database.show()
        #self.close()
        
    def Screenshot(self):
        # Get the screen where the window is located
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        
        # Generate a filename with the current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"screenshot_{timestamp}.png"
        
        # Open a file dialog to save the screenshot
        file_dialog = QFileDialog(self)
        file_dialog.setWindowIcon(QIcon("C:/Python38/programasPython/imagenes/save.svg"))
        file_dialog.setDefaultSuffix("png")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save Screenshot",
            QDir.homePath() + '/' + default_filename,
            "PNG Files (.png);;All Files ()",
            options=options
        )
        
        if file_path:
            screenshot.save(file_path, "png")
    
    def update_plot1(self):
        global data1,client
        ##########
                
        try:
            client.connect()

           
            root = client.get_root_node()
            
            nodo_Sensor_1 = client.get_node('ns=3;s="Data_block_1"."Sensor_1"')
            
            Sensor_1 =nodo_Sensor_1.get_value()
            new_value1 = self.graph1.value()
            data1 = np.append(data1, new_value1)
            self.Num1.display(new_value1)
            self.plot_all()
            
            dv_1= ua.DataValue(ua.Variant(new_value1,ua.VariantType.Int16))
            
            nodo_Sensor_1.set_data_value(dv_1)
            
            
           

        finally:
            client.disconnect()
        
        
        ##########

    def update_plot2(self):
        
        global data2,client
        ##########
                
        try:
            client.connect()

           
            root = client.get_root_node()
            
            nodo_Sensor_2 = client.get_node('ns=3;s="Data_block_1"."Sensor_2"')
            
            Sensor_2 =nodo_Sensor_2.get_value()
            new_value2 = self.graph2.value()
            data2 = np.append(data2, new_value2)
            self.Num2.display(new_value2)
            self.plot_all()
            
            dv_2= ua.DataValue(ua.Variant(new_value2,ua.VariantType.Int16))
            
            nodo_Sensor_2.set_data_value(dv_2)
            
            
           

        finally:
            client.disconnect()
        
        

    def update_plot3(self):
        global data3,client
        try:
            client.connect()

         
            root = client.get_root_node()
            
            nodo_Sensor_3 = client.get_node('ns=3;s="Data_block_1"."Sensor_3"')
            
            Sensor_3 =nodo_Sensor_3.get_value()
            new_value3 = self.graph3.value()
            data3 = np.append(data3, new_value3)
            self.Num3.display(new_value3)
            self.plot_all()
            dv_3= ua.DataValue(ua.Variant(new_value3,ua.VariantType.Int16))
            
            nodo_Sensor_3.set_data_value(dv_3)
            
            
           

        finally:
            client.disconnect()
        
    def update_plot4(self):
        global data4,client
        try:
            client.connect()

          
            root = client.get_root_node()
            
            nodo_Sensor_4 = client.get_node('ns=3;s="Data_block_1"."Sensor_4"')
            
            Sensor_4 =nodo_Sensor_4.get_value()
            new_value4 = self.graph4.value()
            data4 = np.append(data4, new_value4)
            self.Num4.display(new_value4)
            self.plot_all()
            
            dv_4= ua.DataValue(ua.Variant(new_value4,ua.VariantType.Int16))
            
            nodo_Sensor_4.set_data_value(dv_4)
            
            
           

        finally:
            client.disconnect()

    def plot_all(self):
        self.graphWidget.plot(data1, pen='r')
        self.graphWidget.plot(data2, pen='g')
        self.graphWidget.plot(data3, pen='b')
        self.graphWidget.plot(data4, pen='y')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = HMI()
    my_app.show()
    sys.exit(app.exec_())