import cv2
import pyqrcode
import png
from pyqrcode import QRCode
from pyzbar.pyzbar import decode
import numpy as np

# ----- Create videocapture ----- #
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # --- Read QR codes --- #
    for codes in decode(frame):
        #information = codes.data
        
        # --- Decode --- #
        information = codes.data.decode('utf-8')
        
        # --- Type of employee --- #
        type_employee = information[0:2]
        type_employee = int(type_employee)
        
        # --- Extract coordinates --- #
        pts = np.array([codes.polygon], np.int32)
        xi, yi = codes.rect.left, codes.rect.top
        
        # --- Resize --- #
        pts = pts.reshape((-1, 1, 2))
        
        if type_employee == 65:    # A -> 65 (Manager)
            # --- Draw --- #
            cv2.polylines(frame, [pts], True, (255, 0, 0), 5)
            cv2.putText(frame, 'A-' + str(information[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print("Manager \n"
                  f"A-{information[2:]}")
        
        if type_employee == 66:    # B -> 66 (Production)
            # --- Draw --- #
            cv2.polylines(frame, [pts], True, (0, 255, 0), 5)
            cv2.putText(frame, 'B-' + str(information[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print("Production \n"
                  f"B-{information[2:]}")
        
        if type_employee == 67:    # C -> 67 (Maintenance)
            # --- Draw --- #
            cv2.polylines(frame, [pts], True, (0, 0, 255), 5)
            cv2.putText(frame, 'C-' + str(information[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print("Maintenance \n"
                  f"C-{information[2:]}")
        
        else:
            pass
        
        # --- Print Information (all numbers) --- #
        print (information)
    
    # ----- Show FPS ----- #
    cv2.imshow("QR Reader", frame)
    # ----- Read keyboard ----- #
    t = cv2.waitKey(5)
    if t == 27:
        break

cv2.destroyAllWindows()
cap.release()