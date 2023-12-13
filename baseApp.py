#import
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.naive_bayes import GaussianNB
print('import success')

#load models

Sex_LE = pickle.load(open('../13122023prod/tech_models/Sex_LE.pkl', 'rb'))	
Ticket_LE = pickle.load(open('../13122023prod/tech_models/Ticket_LE.pkl', 'rb'))		
Cabin_LE = pickle.load(open('../13122023prod/tech_models/Cabin_LE.pkl', 'rb'))		
Embarked_LE	= pickle.load(open('../13122023prod/tech_models/Embarked_LE.pkl', 'rb'))	
num_scaler = pickle.load(open('../13122023prod/tech_models/num_scaler.pkl', 'rb'))	
gaussNB = pickle.load(open('../13122023prod/ml_models/gaussNB.pkl', 'rb'))	
print('load models success')

#get data
Sex = input('Sex: ')
Ticket = input('Ticket: ')	
Cabin  = input('Cabin: ')	
Embarked  = input('Embarked: ')
Pclass  = float(input('Pclass: '))	
Age	 = float(input('Age: '))	
SibSp  = float(input('SibSp: '))		
Parch  = float(input('Parch: '))		
Fare  = float(input('Fare: '))	

#preprocessing
#категориальные
x_cat_list = [Sex, Ticket, Cabin, Embarked]
le_list = [Sex_LE, Ticket_LE, Cabin_LE, Embarked_LE]
x_le_list = [] #под закодированные признаки
for i in range(len(x_cat_list)):
    x_cat = le_list[i].transform([x_cat_list[i]])[0]
    print(x_cat)
    x_le_list.append(x_cat)
print('LE_list: ', x_le_list)
#числовые
x_num = [Pclass, Age, SibSp, Parch, Fare]
#объединение категориальных и числовых в один вектор
X = []
X.extend(x_le_list)
X.extend(x_num)
#масштабируем вектор
X_scaled = num_scaler.transform([X])
print('X_scaled: ', X_scaled)

#predict
predict = gaussNB.predict(X_scaled) #подаём данные, котоыре отмасштабированы

#result
if predict == 0:
    result = 'not survived'
    print(f'Passenger is {result}')
else:
    result = 'survived'
    print(f'Passenger is {result}')

