from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm

def home_page(request):
    return render(request, 'home.html')

def register_page(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        recruiter_form = SignUpForm(request.POST)
        if user_form.is_valid() and recruiter_form.is_valid():
            user = user_form.save()
            recruiter = recruiter_form.save(commit=False)
            recruiter.user = user
            recruiter.save()            
            return redirect('home.html')
    else:
        user_form = UserCreationForm()
        recruiter_form = SignUpForm()
    return render(request, 'register.html', {'user_form': user_form, 'recruiter_form': recruiter_form})