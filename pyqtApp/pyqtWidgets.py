import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, 
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QTimeEdit,
                             QDial, 
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             QWidget,
                             QDoubleSpinBox,
                             QLabel,
                             QMainWindow)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Демонстрация виджетов')
        layout = QVBoxLayout()
        widgets = (
                    QCheckBox,
                    QComboBox,
                    QDateEdit,
                    QDateTimeEdit,
                    QTimeEdit,
                    QDial, 
                    QProgressBar,
                    QPushButton,
                    QRadioButton,
                    QSlider,
                    QSpinBox,
                    QDoubleSpinBox,
                    QLabel,
                    )
        for i in widgets:
            layout.addWidget(i())
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget) # 

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()