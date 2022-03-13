from django.urls import path
from sdp import views

urlpatterns = [
    path('sdp/', views.sdp)
]
