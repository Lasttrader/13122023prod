from django.urls import path
from . import views

urlpatterns = [path("predict", views.get_predict, name='get_predict'),]
