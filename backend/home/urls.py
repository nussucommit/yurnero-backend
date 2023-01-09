
from django.urls import path
from home import views

urlpatterns = [
  path('training-workshops/', views.training_workshops),
  path('elevate-the-creativity/', views.elevate_creativity),
  path('study-print-scan/', views.study_print_scan),
]
