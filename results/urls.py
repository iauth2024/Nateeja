from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_excel, name='search_excel'),
]