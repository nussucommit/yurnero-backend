from django.urls import path
from FAQ import views

urlpatterns = [
    path('faq/', views.faq)
]
