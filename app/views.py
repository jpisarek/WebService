from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, QuizAddForm, QuestionAddForm, AnswerAddForm
from app.models import Candidate, Quiz, Question, Answer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
            return redirect('home_page')
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

@login_required
def recruiter_home(request):
    return render(request, 'recruiter/recruiter_home.html')

@login_required
def recruiter_rank(request):
    candidates = Candidate.objects.all().order_by('id')
    return render(request, 'recruiter/recruiter_rank.html', {'candidates': candidates})


def recruiter_quiz_add(request):
    if request.method == 'POST':
        quiz_form = QuizAddForm(request.POST)
        if quiz_form.is_valid():
            organization = quiz_form.cleaned_data.get('organization')
            name = quiz_form.cleaned_data.get('name')
            level = quiz_form.cleaned_data.get('level')
            quiz_form.save()
            quiz_id = quiz_form.take_id()
            print(quiz_id)
            return redirect('/recruiter/quiz/%d/question/' % (quiz_id,))
    else:
        quiz_form = QuizAddForm()
    return render(request, 'recruiter/recruiter_quiz_add.html', {'quiz_form': quiz_form,},)

def recruiter_question_add(request, quiz_id):
    quiz_ = Quiz.objects.get(id=quiz_id)
    print(quiz_id)
    if request.method == 'POST':
        question_form = QuestionAddForm(request.POST)
        if question_form.is_valid():
            content = question_form.cleaned_data.get('content')
            question_form.save(for_quiz=quiz_)
            question_id = question_form.take_id()
            return redirect('/recruiter/question/%d/answer/' % (question_id,))
    else:
        question_form = QuestionAddForm()
    return render(request, 'recruiter/recruiter_question_add.html', {'question_form': question_form, 'quiz_id': quiz_id},)

def recruiter_quiz_overview(request):
    quizzes = Quiz.objects.all().order_by('id')
    return render(request, 'recruiter/recruiter_quiz_overview.html', {'quizzes': quizzes})

def recruiter_answer_add(request, question_id):
    return render(request, 'recruiter/recruiter_answer_add.html')
