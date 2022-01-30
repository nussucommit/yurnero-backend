from django.urls import path
from vrogros import views

urlpatterns = [
  path('database', views.get_notion_database),
  path('sample-page', views.get_sample_page),
  path('sample-block', views.get_sample_block)
]