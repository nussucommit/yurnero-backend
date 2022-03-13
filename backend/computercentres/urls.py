from django.urls import path
from computercentres import views

urlpatterns = [
    path('computer-centres/', views.computercentres)
]
