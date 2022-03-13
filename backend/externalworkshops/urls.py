from django.urls import path
from externalworkshops import views

urlpatterns = [
    path('external-workshops/', views.externalworkshops)
]
