from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime 
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import TaskForm, RegisterForm
from .models import Task
from django.contrib import messages


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Already Signed In!!')
        return redirect('home')
    
    form = RegisterForm
    errors = None
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(request, username= username, password= password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Account Created and login Successful!!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username Or Password!!')
                return redirect('login')
        else:
            errors = form.errors.as_data()
            messages.error(request, errors)
            return redirect('register')

    context = {
        'form': form ,
        'errors': errors
    }        
    
    return render(request, 'register.html', context)    



@login_required(login_url='login')
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

    greeting = f'{msg} {request.user.username}!'
    
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    # To Read everything 
    
    context ={
        'greeting': greeting,
        'tasks':tasks
        
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Authentication Successful!!')
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!!')
            return redirect('home')
        else: 
            messages.error(request, 'Invalid Username Or Password!!')
            return redirect('login')
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successful!!')
    return redirect('login')
    
@login_required(login_url='login')
def add_task(request):
    forms = TaskForm()
    if request.method == "POST":
        forms = TaskForm(request.POST)
        # CHECK FOR VALIDATION
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Tasks Added Succesfully!!')
            
    #     title = request.POST.get('title')
    #     due_time = request.POST.get('due_time')
        
    #     task = Task.objects.create(
    #         title=title,
    #         due_time=due_time
    #      )
        
    #     task.save()
            return redirect ("home")
        else:
            errors = forms.errors.as_data()
            messages.error(request, errors)
            return redirect ("add_task")
        
    context = {
        "forms":forms
    }
        
    return render(request, 'add_task.html', context)

@login_required(login_url='login')
def filter_tasks(request, foo):
    if foo == "true":
        tasks = Task.objects.filter(done=True, user = request.user).order_by('-created_at')
    elif foo == "false":
        tasks = Task.objects.filter(done=False, user= request.user).order_by('-created_at')
    else:
        tasks = Task.objects.filter(user= request.user).order_by('-created_at')
        
    context = {
        "tasks":tasks
    }
    return render(request, "home.html", context)

@login_required(login_url='login')
def update_task(request, pk):
    #task = Task.objects.get(id=pk)
    task = get_object_or_404(Task, id=pk, user= request.user)
    form = TaskForm(instance=task)
    
    if request.method == "POST":
        form = TaskForm(request.post, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task Updated Succesfully!!')
        # title = request.POST.get('title')
        # done = request.POST.get('done')
        # due_time = request.POST.get('due_time')
        # # ===================== #
        # # Assign values to task #
        # # ====================== #
        # task.title = title
        # if done:
        #     task.done = True
        # else:
        #     task.done = False
        # if due_time:
        #     task.due_time = due_time
        
        # # save task
        # task.save()
            return redirect('home')
        else:
            errors = messages.error(request, errors)
            return redirect('task', pk=pk)
    
    context = {
        'task':task,
        'form':form
    }   
    return render(request, 'update_task.html', context) 

@login_required(login_url='login')
def delete_task(request, pk):    
    task = get_object_or_404(Task, id=pk)
    task.delete()
    messages.success(request, 'Task Succesfully Delected!!')
   
    return redirect('home')