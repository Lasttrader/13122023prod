from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.


def get_predict(request):
    X_scaled = [0.73769513,  0.66490369, (-2.1037683),   0.58111394,  0.82737724, -0.42199068,
                0.43279337, (-0.47367361),  0.78114114]
    api_message = requests.post('http://0.0.0.0:5000/api/v1/add_message/',
                                json={'X_scaled': [X_scaled]})
    print(api_message)
    if api_message.ok:
        print(api_message.json())

    return HttpResponse(f'Predict: your passenger is {api_message.json()}')
