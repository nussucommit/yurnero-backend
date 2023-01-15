from django.urls import path
from aboutus import views

urlpatterns = [
  path('our-family/', views.family),
  path('vision-and-mission/', views.vision_mission),
  path('our-structure/', views.structure),
  path('management-committee/', views.manag_comm),
  path('overview/', views.overview),
]