from django.urls import path
from contacts import views

urlpatterns = [
    path('contacts/contactus', views.contacts),
    path('contacts/address/', views.address),
    path('contacts/subscribe/', views.subscribe)
]