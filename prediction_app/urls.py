from django.urls import path

from . import views
#the line above raises an error, so I have to 
#apply an "absolute import" 

app_name = 'streamlit_app'

urlpatterns = [
   path('streamlit_app/', views.streamlit_prediction, name=app_name),
]