from django.urls import path
from creation import views

urlpatterns = [
    path('creation/', views.creation)
]
