#import
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.naive_bayes import GaussianNB

import sys
from PyQt6.QtWidgets import (QApplication,
                             QDialog,
                             QDialogButtonBox, 
                             QFormLayout,
                             QLineEdit, 
                             QVBoxLayout, 
                             QGroupBox,
                             QLabel,
                             QMessageBox,
                             QPushButton)

print('import success')

#загрузка моделей
Sex_LE = pickle.load(open('../flaskApp/tech_models/Sex_LE.pkl', 'rb'))
Ticket_LE = pickle.load(open('../flaskApp/tech_models/Ticket_LE.pkl', 'rb'))
Cabin_LE = pickle.load(open('../flaskApp/tech_models/Cabin_LE.pkl', 'rb'))
Embarked_LE = pickle.load(open('../flaskApp/tech_models/Embarked_LE.pkl', 'rb'))
num_scaler = pickle.load(open('../flaskApp/tech_models/num_scaler.pkl', 'rb'))
gaussNB = pickle.load(open('../flaskApp/ml_models/gaussNB.pkl', 'rb'))
print('load models success')


#Класс диалога, указываем кнопки, и привязываем кнопку  "ок" на выполнения predict
class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.createFormGroupBox()
        self.x_for_predict = {}
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.get_predict)
        buttonBox.rejected.connect(self.rejected)

        mainLayout  = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle('desktop ML app')

    def createFormGroupBox(self):
        #поля для ввода
        self.formGroupBox = QGroupBox('Введите ваша данные')
        self.layout = QFormLayout()

        '''
        self.Sex = QLineEdit()
        self.Sex.textEdited.connect(self.create_x_for_predict(1))
        self.layout.addRow(QLabel('Sex'), self.Sex)
        
        self.Ticket = QLineEdit()
        self.Ticket.textEdited.connect(self.create_x_for_predict(2))
        self.layout.addRow(QLabel('Ticket'), self.Ticket)

        self.Cabin = QLineEdit()
        self.Cabin.textEdited.connect(self.create_x_for_predict(3))
        self.layout.addRow(QLabel('Cabin'), self.Cabin)

        self.Embarked = QLineEdit()
        self.Embarked.textEdited.connect(self.create_x_for_predict(4))
        self.layout.addRow(QLabel('Embarked'), self.Embarked)

        self.Pclass = QLineEdit()
        self.Pclass.textEdited.connect(self.create_x_for_predict(5))
        self.layout.addRow(QLabel('Pclass'), self.Pclass)

        self.Age = QLineEdit()
        self.Age.textEdited.connect(self.create_x_for_predict(6))
        self.layout.addRow(QLabel('Age'), self.Age)

        self.SibSp = QLineEdit()
        self.SibSp.textEdited.connect(self.create_x_for_predict(7))
        self.layout.addRow(QLabel('SibSp'), self.SibSp)

        self.Parch = QLineEdit()
        self.Parch.textEdited.connect(self.create_x_for_predict(8))
        self.layout.addRow(QLabel('Parch'), self.Parch)

        self.Fare = QLineEdit()
        self.Fare.textEdited.connect(self.create_x_for_predict(9))
        self.layout.addRow(QLabel('Fare'), self.Fare)
        '''

        buttons_list = ['Sex',
                        'Ticket',
                        'Cabin',
                        'Embarked',
                        'Pclass',
                        'Age',
                        'SibSp',
                        'Parch',
                        'Fare'
                        ]
        #компактные код, может пригодиться, когда нужно создать большое кол-во полей
        for index, label in enumerate(buttons_list):
            x = QLineEdit()
            x.textEdited.connect(self.create_x_for_predict(index + 1))
            self.layout.addRow(QLabel(label), x)
        self.formGroupBox.setLayout(self.layout)


    def create_x_for_predict(self, x):
        #функция собирает Х для прогноза
        def savedX(text):
            self.x_for_predict[x] = text
        return savedX

    #функция, выполнения прогноза (predict), которая запускается при нажатии на кнопку ОК   
    def get_predict(self):
        rslt = QMessageBox(self)
        rslt.setWindowTitle('Ваш прогноз')
        # preprocessing
        # категориальные
        x_list = list(self.x_for_predict.values())
        x_cat_list = x_list[:4] #это категориальные признаки с формы
        le_list = [Sex_LE, Ticket_LE, Cabin_LE, Embarked_LE]
        x_le_list = []  # под закодированные признаки
        for i in range(len(x_cat_list)):
            x_cat = le_list[i].transform([x_cat_list[i]])[0]
            print(x_cat)
            x_le_list.append(x_cat)
        print('LE_list: ', x_le_list)
        # числовые
        x_num = x_list[4:]
        # объединение категориальных и числовых в один вектор
        X = []
        X.extend(x_le_list)
        X.extend(x_num)
        # масштабируем вектор
        X_scaled = num_scaler.transform([X])
        print('X_scaled: ', X_scaled)
        # predict
        # подаём данные, котоыре отмасштабированы
        predict = gaussNB.predict(X_scaled)
        # result
        if predict == 0:
            result = 'not survived'
        else:
            result = 'survived'
        rslt.setText(f'you passeneger if {result}')
        rslt.exec() #исполнитель

#запус и закрытие приложения
app = QApplication(sys.argv)
dialog = Dialog()
dialog.exec() #исполнитель
app.exit()

