from django.urls import path
from trainingworkshops import views

urlpatterns = [
    path('training-workshops/', views.trainingworkshops)
]
