from PyQt6.QtWidgets import QApplication
from go import Go
import sys
from game_logic import GameLogic

#cc = GameLogic()

app = QApplication([])
myGo = Go()
sys.exit(app.exec())
