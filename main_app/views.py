# main_app/views.py

from django.shortcuts import render

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello World ᓚᘏᗢ</h1>')

def about(request):
    # Send a simple HTML response
    return HttpResponse('<h1>About the CatCollector</h1>')

def about(request):
    return render(request, 'about.html')

