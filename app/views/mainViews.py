from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, LoginForm, UserCreateForm
from django.contrib.auth.forms import UserCreationForm
from app.models import User


def home_page(request):
    return render(request, 'home.html')


def register_page(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        candidate_form = SignUpForm(request.POST)
        if user_form.is_valid() and candidate_form.is_valid():
            user = user_form.save()
            candidate = candidate_form.save(commit=False)
            candidate.user = user
            candidate.save()            
            return redirect('home_page')
    else:
        user_form = UserCreateForm()
        candidate_form = SignUpForm()
    return render(request, 'register.html', {'user_form': user_form, 'candidate_form': candidate_form})


def login_page(request):
    users = User.objects.all().order_by('id')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        users_recruiters = User.objects.all().filter(is_staff=1)
        if user is not None:
            login(request, user)
            log_user = User.objects.all().filter(username=username)            
            if log_user[0].is_staff == 1 and log_user[0].is_superuser == 0:
                return redirect('recruiter_home')
            elif log_user[0].is_superuser == 1:
                return redirect('/admin/')
            else:
                return redirect('candidate_home')
        else:
            return render(request, 'registration/login.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})