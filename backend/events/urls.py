from django.urls import path
from events import views

urlpatterns = [
    path('cyberia/', views.cyberia),
    path('creation/', views.creation),
    path('chariteach/', views.chariteach)
]
