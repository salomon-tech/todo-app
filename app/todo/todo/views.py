from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .models import Todo


@login_required(login_url='login')
def todo_list(request):
    """Display all todos for the logged-in user"""
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo.html', {'todos': todos})


@login_required(login_url='login')
def add_todo(request):
    """Add a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'M')
        due_date = request.POST.get('due_date') or None
        
        Todo.objects.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user=request.user
        )
    return redirect('todo')


@login_required(login_url='login')
def toggle_todo(request, todo_id):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo')


@login_required(login_url='login')
def edit_todo(request, todo_id):
    """Edit a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title)
        todo.description = request.POST.get('description', todo.description)
        todo.priority = request.POST.get('priority', todo.priority)
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        todo.save()
        return redirect('todo')
    
    return render(request, 'edit.html', {'todo': todo})


@login_required(login_url='login')
def delete_todo(request, todo_id):
    """Delete a todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
    return redirect('todo')


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('todo')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def signup_view(request):
    """Handle user signup"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('todo')
    
    return render(request, 'signup.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')
