from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
     path('user_profile/', views.user_info, name='user_info'),
       path('credit_score/', views.credit_score, name='credit_score'),  # Add this line to include user_info view
]