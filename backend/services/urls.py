from django.urls import path
from services import views

urlpatterns = [
    path('computer-centres/', views.computercentres),
    path('training-workshops/', views.trainingworkshops),
    path('external-workshops/', views.externalworkshops),
    path('sdp/', views.sdp)
]
