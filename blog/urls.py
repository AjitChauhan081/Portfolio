from django.urls import path
from . import views

urlpatterns = [
    # List view (e.g., /blog/)
    path('', views.blog_list_view, name='blog'), 
    
    # Detail view (e.g., /blog/ethical-ai-path/)
    path('archive/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('category/<slug:slug>/', views.category_filter_view, name='category_filter'),
    path('<slug:slug>/', views.blog_detail_view, name='blog_detail'),
]