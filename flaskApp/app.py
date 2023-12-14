# import
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.naive_bayes import GaussianNB
from flask import (Flask,
                   render_template,
                   jsonify,
                   request)
from config import API_VERSION
print('import success')
# load models
Sex_LE = pickle.load(open('../flaskApp/tech_models/Sex_LE.pkl', 'rb'))
Ticket_LE = pickle.load(open('../flaskApp/tech_models/Ticket_LE.pkl', 'rb'))
Cabin_LE = pickle.load(open('../flaskApp/tech_models/Cabin_LE.pkl', 'rb'))
Embarked_LE = pickle.load(
    open('../flaskApp/tech_models/Embarked_LE.pkl', 'rb'))
num_scaler = pickle.load(open('../flaskApp/tech_models/num_scaler.pkl', 'rb'))
gaussNB = pickle.load(open('../flaskApp/ml_models/gaussNB.pkl', 'rb'))
print('load models success')

# app
app = Flask(__name__)

# route


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        Sex = request.form['Sex']
        Ticket = request.form['Ticket']
        Cabin = request.form['Cabin']
        Embarked = request.form['Embarked']

        Pclass = float(request.form['Pclass'])
        Age = float(request.form['Age'])
        SibSp = float(request.form['SibSp'])
        Parch = float(request.form['Parch'])
        Fare = float(request.form['Fare'])

        # preprocessing
        # категориальные
        x_cat_list = [Sex, Ticket, Cabin, Embarked]
        le_list = [Sex_LE, Ticket_LE, Cabin_LE, Embarked_LE]
        x_le_list = []  # под закодированные признаки
        for i in range(len(x_cat_list)):
            x_cat = le_list[i].transform([x_cat_list[i]])[0]
            print(x_cat)
            x_le_list.append(x_cat)
        print('LE_list: ', x_le_list)
        # числовые
        x_num = [Pclass, Age, SibSp, Parch, Fare]
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
        return render_template('main.html', result=result)


@app.route('/api/v1/add_message/', methods=['POST', 'GET'])
def api_message():
    get_message_x = request.json  # получили json с другого сервиса
    # подалди уже отмасштабированные данные
    predict = gaussNB.predict(get_message_x['X_scaled'])
    print(predict)
    if predict == 0:
        result = 'not survived'
    else:
        result = 'survived'

    # прогноз возвращение в сервис. который запросил
    return jsonify(str(result))


# вариант с версионностью API
@app.route(f'/api/{API_VERSION}/add_message/', methods=['POST', 'GET'])
def api_message_v3():
    get_message_x = request.json  # получили json с другого сервиса
    # подалди уже отмасштабированные данные
    predict = gaussNB.predict(get_message_x['X_scaled'])
    print(predict)
    if predict == 0:
        result = 'not survived'
    else:
        result = 'survived'

    # прогноз возвращение в сервис. который запросил
    return jsonify(str(result))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
