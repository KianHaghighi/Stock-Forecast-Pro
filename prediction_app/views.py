from django.shortcuts import render
import subprocess
# Create your views here.
#here, i need to fix the code, so that 
#it redirects to what the code should output and 
#not the code itself
def streamlit_prediction(request):
    #return render(request, 'main.py')
    result = subprocess.run(['streamlit', 'run', 'main.py'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return render(request, 'home.html', {'output': output})



#Steps to integrate my streamlit app on my Django project:
# 1.install django-streamlit
# 2.add "django_streamlit" to the INSTALLED_APPS list in settings.py
# 3.define the url for the streamlit app in the proper urls.py file
# 4.update 'href' button in home.html

#another method that i could try:
#1. create a views.py that links to "streamlit.html"
#2. create streamlit.html
#3. add a url patter in urls.py for the 'streamlit_view' function
#4. add a button to my django app template that links to the 'streamlit_view' view