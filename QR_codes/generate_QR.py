import pyqrcode
import png
from pyqrcode import QRCode

"""
ASCII code
A ---> 65 (Manager) 
B ---> 66 (Production)
C ---> 67 (Maintenance)
"""

# ----- Variables ----- #
counter = 1234

# ----- Generate QR codes ----- #
while counter <= 1234:
    #id = str('j') + str('counter')
    roster = counter
    id = '67' + str(counter)
    qr = pyqrcode.create(67 and id, error = 'L')
    # --- Save QR --- #
    qr.png('C' + str(roster) + '.png', scale = 6)
    # --- Increase counter --- #
    counter += 1