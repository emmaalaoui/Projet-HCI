from PyQt6.QtWidgets import QApplication
from go import Go
import sys



app = QApplication([])
myGo = Go(675, True, [0, 0])
sys.exit(app.exec())
