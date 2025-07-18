from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Task
from .forms import EmailUserCreationForm, EmailAuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = EmailUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('task_list')
                else:
                    form.add_error(None, 'Invalid email or password.')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = EmailAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

@login_required
def task_list(request):
    user_tasks = Task.objects.filter(user=request.user)
    
    # Organize tasks by priority
    tasks_by_priority = {
        'high': user_tasks.filter(priority='H', is_complete=False).order_by('due_date'),
        'medium': user_tasks.filter(priority='M', is_complete=False).order_by('due_date'),
        'low': user_tasks.filter(priority='L', is_complete=False).order_by('due_date'),
        'completed': user_tasks.filter(is_complete=True).order_by('-due_date'),
    }
    
    return render(request, 'tasks/task_list.html', {'tasks_by_priority': tasks_by_priority})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    # For both GET and after POST, redirect to the task list
    return redirect('task_list')

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    # For both GET and after POST, redirect to the task list
    return redirect('task_list')

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render('task_list')

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_complete = True
    task.save()
    return redirect('task_list')