from django.urls import path
from about_us import views

urlpatterns = [
    path('our-family/', views.our_family),
    path('vision-mission/', views.vision_mission),
    path('our-structure/', views.our_structure),
    path('overview/', views.overview),
]