from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('load-data/', views.load_data, name='load_data'),  # API endpoint
]
