from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import StockData

import requests
import json
import streamlit as st

APIKEY = '9N1F7EYLZRR8K2KO' 


DATABASE_ACCESS = True 
#if False, the app will always query the Alpha Vantage APIs regardless of whether the stock data for a given ticker is already in the local database


#view function for rendering home.html
def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

#using template "streamlit.html"
def streamlit_view(request):
    return render(request, 'streamlit.html')

@csrf_exempt
def get_stock_data(request):
    #if request.accepts('application/json'):
    if is_ajax(request):
        #get ticker from the AJAX POST request
        ticker = request.POST.get('ticker', 'null')
        ticker = ticker.upper()

        if DATABASE_ACCESS == True:
            #checking if the database already has data stored for this ticker before querying the Alpha Vantage API
            if StockData.objects.filter(symbol=ticker).exists(): 
                #We have the data in our database! Get the data from the database directly and send it back to the frontend AJAX call
                entry = StockData.objects.filter(symbol=ticker)[0]
                return HttpResponse(entry.data, content_type='application/json')

        #obtain stock data from Alpha Vantage APIs
        #get adjusted close data
        price_series = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={APIKEY}&outputsize=full').json()
        
        #get SMA (simple moving average) data
        sma_series = requests.get(f'https://www.alphavantage.co/query?function=SMA&symbol={ticker}&interval=daily&time_period=10&series_type=close&apikey={APIKEY}').json()

        #package up the data in an output dictionary 
        output_dictionary = {}
        output_dictionary['prices'] = price_series
        output_dictionary['sma'] = sma_series

        #save the dictionary to database
        temp = StockData(symbol=ticker, data=json.dumps(output_dictionary))
        temp.save()

        #return the data back to the frontend AJAX call 
        return HttpResponse(json.dumps(output_dictionary), content_type='application/json')

    else:
        message = "Not AJAX"
        return HttpResponse(message)



#will potentially use this function to fix the error with json "Error Message"
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
