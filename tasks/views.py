from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.contrib import messages
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(title__icontains=query) | tasks.filter(description__icontains=query)

    pending_count    = Task.objects.filter(user=request.user, status='pending').count()
    inprogress_count = Task.objects.filter(user=request.user, status='in_progress').count()
    completed_count  = Task.objects.filter(user=request.user, status='completed').count()

    return render(request, 'tasks/task_list.html', {
        'tasks':            tasks,
        'query':            query,
        'status':           status,
        'pending_count':    pending_count,
        'inprogress_count': inprogress_count,
        'completed_count':  completed_count,
        'now':              timezone.now(),
    })

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, '✅ Task created successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, '✏️ Task updated successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit'})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, '🗑️ Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

def profile(request):
    total_tasks     = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, status='completed').count()
    pending_tasks   = Task.objects.filter(user=request.user, status='pending').count()
    overdue_tasks   = Task.objects.filter(
        user=request.user,
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).count()
    completion_rate = int((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)

    return render(request, 'tasks/profile.html', {
        'total_tasks':     total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks':   pending_tasks,
        'overdue_tasks':   overdue_tasks,
        'completion_rate': completion_rate,
    })