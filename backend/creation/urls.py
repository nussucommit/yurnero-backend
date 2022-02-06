from django.urls import path
# from django.conf.urls import url

from creation.views import get_creation

urlpatterns = [
    path('creation', get_creation, name='get-creation' )
]