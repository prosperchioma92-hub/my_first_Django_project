from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def home(request):
    date = datetime.datetime.now()
    hour = int(date.strftime('%H'))
    
    msg = 'Good '
    
    if hour < 12:
        msg += 'Morning'
    elif hour < 16:
        msg += 'Afternoon'
    elif hour < 18:
        msg += 'Evening'
    else:
        msg += 'Night'

    greeting = f'{msg} catalyst'
    
    tasks =[ 
        {'id':1, 'text': 'cook rice and stew', 'done':True},
        {'id':2, 'text': 'wash clothes', 'done':True},
        {'id':3,'text':'family get together', 'done':False},
        {'id':4,'text':'Hit the gym', 'done':False},
        {'id':5,'text':'practice django', 'done':False},
        {'id':6,'text':'Netflix and chill', 'done':True}
    ]
    
    context ={
        'greeting': greeting,
        'tasks':tasks
        
    }
    return render(request, 'home.html', context)

def login(request):
    return render(request, 'login.html')