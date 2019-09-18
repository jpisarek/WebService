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
        candidate_form = SignUpForm(request.POST)
        if user_form.is_valid() and candidate_form.is_valid():
            user = user_form.save()
            candidate = candidate_form.save(commit=False)
            candidate.user = user
            candidate.save()            
            return redirect('home.html')
    else:
        user_form = UserCreationForm()
        candidate_form = SignUpForm()
    return render(request, 'register.html', {'user_form': user_form, 'candidate_form': candidate_form})

# def login_page(request):
#     username = request.POST.get('username', '')
#     password = request.POST.get('password', '')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('home.html')
#     else:
#         return redirect('login.html')

def recruiter_home(request):
    return render(request, 'recruiter_home.html')