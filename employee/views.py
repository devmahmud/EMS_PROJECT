from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from employee.decorators import role_required
from .forms import UserForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            return render(request, 'auth/success.html')
        else:
            return render(request, 'auth/login.html')
    else:
        return render(request, 'auth/login.html')


def user_logout(request):
    logout(request)
    return redirect('poll_list')


@login_required(login_url='user_login')
def employee_list(request):
    print(request.role)
    employees = User.objects.all()
    return render(request, 'employee/index.html', {'employees': employees})


@login_required(login_url='user_login')
def employee_detail(request, emp_id=None):
    employee = get_object_or_404(User, pk=emp_id)
    return render(request, 'employee/details.html', {'employee': employee})


@login_required(login_url='user_login')
@role_required(allowed_roles=['Admin', 'HR'])
def add_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('employee_list')
        else:
            return render(request, 'employee/add.html', {'form': user_form})
    else:
        user_form = UserForm()
        return render(request, 'employee/add.html', {'form': user_form})


@login_required(login_url='user_login')
def edit_employee(request, emp_id=None):
    user = get_object_or_404(User, pk=emp_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('employee_list')
        else:
            return render(request, 'employee/add.html', {'form': user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/add.html', {'form': user_form})


@login_required(login_url='user_login')
def delete_employee(request, emp_id=None):
    user = get_object_or_404(User, pk=emp_id)
    if request.method == 'POST':
        user.delete()
        return redirect('employee_list')
    else:
        return render(request, 'employee/delete.html', {'employee': user})
