from django.urls import path
from . import views

urlpatterns = [
    path('show_rates/', views.show_rates, name='show_rates'),
]