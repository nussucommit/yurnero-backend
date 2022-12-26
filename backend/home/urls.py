
from django.urls import path
from home import views

urlpatterns = [
  path('training-workshops/', views.trainingworkshops),
  path('elevate-the-creativity/', views.elevatecreativity),
  path('study-print-scan/', views.studyprintscan),
]
