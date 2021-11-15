from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('calculate/', views.calculate, name='calculate'),
    path('contact/', views.contact, name='contact'),

]
# path('calculate2/', views.calculate2, name='calculate2'),