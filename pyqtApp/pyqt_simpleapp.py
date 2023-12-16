import sys

from PyQt6.QtWidgets import (QApplication, 
                             QLabel,
                             QWidget)

#app
app = QApplication([])

#создаем окно с приложением
window = QWidget()
window.setWindowTitle('Наше первое  десктопное приложение ')
window.setGeometry(200, 200, 560, 160)
window_message = QLabel('<h1> Привет приложение </h1>', parent  = window)

window.show()

sys.exit(app.exec())