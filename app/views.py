from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, QuizAddForm, QuestionAddForm, AnswerAddForm, LoginForm, JobPostingAddForm
from app.models import Organization, Recruiter, Candidate, Quiz, Question, Answer, JobPosting, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory


def take_organization(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        recruiter = Recruiter.objects.get(user_id=user.id)
        organization = Organization.objects.get(id=recruiter.organization_id)
        return(organization.id)


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
            if log_user[0].is_staff == 1:
                return redirect('recruiter_home')
            else:
                return redirect('candidate_home')
        else:
            return render(request, 'registration/login.html', {'login_form': login_form})
    else:
        login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


@login_required(login_url='/login')
def recruiter_home(request):
    return render(request, 'recruiter/recruiter_home.html')


@login_required(login_url='/login')
def recruiter_rank(request):
    candidates = Candidate.objects.all().order_by('id')
    return render(request, 'recruiter/recruiter_rank.html', {'candidates': candidates})


@login_required(login_url='/login')
def recruiter_quiz_add(request):
    organization = take_organization(request)

    if request.method == 'POST':
        quiz_form = QuizAddForm(request.POST)
        if quiz_form.is_valid():
            name = quiz_form.cleaned_data.get('name')
            job_position = quiz_form.cleaned_data.get('job_position')
            quiz_form.save(for_organization=organization)
            quiz_id = quiz_form.take_id()
            return redirect('/recruiter/quiz/%d/question/' % (quiz_id,))
    else:
        quiz_form = QuizAddForm()
    return render(request, 'recruiter/recruiter_quiz_add.html', {'quiz_form': quiz_form,},)


@login_required(login_url='/login')
def recruiter_question_add(request, quiz_id):
    quiz_ = Quiz.objects.get(id=quiz_id)
    quiz_name = quiz_.name
    questionS = Question.objects.all().filter(quiz_id=quiz_id)
    if request.method == 'POST':
        question_form = QuestionAddForm(request.POST)
        if question_form.is_valid():
            content = question_form.cleaned_data.get('content')
            question_form.save(for_quiz=quiz_)
            question_id = question_form.take_id()
            return redirect('/recruiter/question/%d/answer/' % (question_id,))
    else:
        question_form = QuestionAddForm()
    return render(request, 'recruiter/recruiter_question_add.html', {'question_form': question_form, 'quiz_name': quiz_name, 'quiz_id': quiz_id, 'questionS': questionS})


@login_required(login_url='/login')
def recruiter_quiz_overview(request):
    organization = take_organization(request)
    quizzes = Quiz.objects.all().filter(organization_id=organization).order_by('id')
    return render(request, 'recruiter/recruiter_quiz_overview.html', {'quizzes': quizzes})


@login_required(login_url='/login')
def recruiter_answer_add(request, question_id):
    question_ = Question.objects.get(id=question_id)
    question_content = question_.content
    quiz_id = question_.quiz_id
    AnswerFormSet = formset_factory(AnswerAddForm, min_num=3, max_num=3)
    if request.method == 'POST':
        formset = AnswerFormSet(request.POST, request.FILES)
  
        if formset[0].is_valid():
            content = formset[0].cleaned_data.get('content')
            is_boolean = formset[0].cleaned_data.get('is_boolean')
            formset[0].save(for_question=question_)

        if formset[1].is_valid():
            content = formset[1].cleaned_data.get('content')
            is_boolean = formset[1].cleaned_data.get('is_boolean')
            formset[1].save(for_question=question_)

        if formset[2].is_valid():
            content = formset[2].cleaned_data.get('content')
            is_boolean = formset[2].cleaned_data.get('is_boolean')
            formset[2].save(for_question=question_)
            question_iD = int(question_id)
            return redirect('/recruiter/quiz/%d/question/' % (quiz_id,))
    else:
        formset = AnswerFormSet()
    return render(request, 'recruiter/recruiter_answer_add.html', {'formset': formset, 'question_content': question_content})


@login_required(login_url='/login')
def recruiter_position_add(request):
    organization = take_organization(request)

    if request.method == 'POST':
        position_form = JobPostingAddForm(request.POST)
        if position_form.is_valid():
            job_position = position_form.cleaned_data.get('job_position')
            description = position_form.cleaned_data.get('description')
            position_form.save(for_organization=organization)
            return redirect('/recruiter/position/add/')
    else:
        position_form = JobPostingAddForm()
    return render(request, 'recruiter/recruiter_position_add.html', {'position_form': position_form,},)


@login_required(login_url='/login')
def recruiter_position_overview(request):
    organization = take_organization(request)
    positions = JobPosting.objects.all().filter(organization_id=organization).order_by('id')
    return render(request, 'recruiter/recruiter_position_overview.html', {'positions': positions})


@login_required(login_url='/login')
def candidate_home(request):
    return render(request, 'candidate/candidate_home.html')


@login_required(login_url='/login')
def candidate_quiz_overview(request):
    quizzes = Quiz.objects.all().order_by('id')
    return render(request, 'candidate/candidate_quiz_overview.html', {'quizzes': quizzes})


@login_required(login_url='/login')
def candidate_quiz_start(request, quiz_id):
    quiz_ = Quiz.objects.get(id=quiz_id)
    quiz_name = quiz_.name
    questions = Question.objects.all().filter(quiz_id=quiz_id)
    for q in range(len(questions)):
        questions_id = questions[q].id
        answers = Answer.objects.all().filter(question_id=questions_id)
        for answer in answers:
            answer.is_clicked = True
        questions[q].answers = answers
    
    return render(request, 'candidate/candidate_quiz_start.html', {'quiz_name': quiz_name, 'quiz_id': quiz_id, 'questions': questions})
