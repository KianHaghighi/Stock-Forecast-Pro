"""vis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
import sys
import stockVisualizer.views
import prediction_app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", stockVisualizer.views.home),
    path('get_stock_data/', stockVisualizer.views.get_stock_data),
    #adding next line to fix error of "Improperly Configured"
    path('prediction_app/', include('prediction_app.urls', 'prediction_app')),
    path('streamlit_view/', prediction_app.views.streamlit_prediction, name='streamlit_view'),
    path('home/', stockVisualizer.views.home, name='home'),
    path('about/',stockVisualizer.views.about, name='about'),
    path('contact/', stockVisualizer.views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', stockVisualizer.views.signup_view, name='signup'),
    path('accounts/profile/', stockVisualizer.views.profile_view, name='profile'),
]
