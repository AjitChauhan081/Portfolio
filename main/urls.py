from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.main, name='main'),
    path('', views.portfolio_view, name='portfolio_view'),
    # path('skill/', views.skill, name='skill'),
    
]