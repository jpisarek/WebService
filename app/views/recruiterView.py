from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, QuizAddForm, QuestionAddForm, AnswerAddForm, LoginForm, JobPostingAddForm, ApplicationAddForm, ApplicationRecruiterForm, UserCreateForm
from app.models import Organization, Recruiter, Candidate, Quiz, Question, Answer, JobPosting, User, Application, QuizResult
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory


def take_organization(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        recruiter = Recruiter.objects.get(user_id=user.id)
        organization = Organization.objects.get(id=recruiter.organization_id)
        return(organization.id)


@login_required(login_url='/login')
def recruiter_home(request):
    user = User.objects.get(username=request.user)
    return render(request, 'recruiter/recruiter_home.html', {'user': user})


@login_required(login_url='/login')
def recruiter_rank(request):
    organization = take_organization(request)
    quiz = list(Quiz.objects.all().filter(organization_id=organization).values_list('id', flat=True))
    applications = Application.objects.all().filter(quiz_id__in=quiz).order_by('-grade')
    i = 0
    for app in applications:
        quiz_id = app.quiz_id
        quizes = Quiz.objects.get(id=quiz_id)
        applications[i].position = JobPosting.objects.get(id=quizes.job_position_id)
        applications[i].quiz_name = quizes.name
        applications[i].candidate_name = Candidate.objects.get(id=applications[i].candidate_id)
        i = i + 1
    return render(request, 'recruiter/recruiter_rank.html', {'applications': applications})


@login_required(login_url='/login')
def recruiter_quiz_add(request):
    organization = take_organization(request)

    if request.method == 'POST':
        quiz_form = QuizAddForm(request.POST, organization)
        if quiz_form.is_valid():
            name = quiz_form.cleaned_data.get('name')
            quiz_form.save(for_organization=organization)
            quiz_id = quiz_form.take_id()
            return redirect('/recruiter/quiz/%d/question/' % (quiz_id,))
    else:
        quiz_form = QuizAddForm()
        quiz_form.fields["job_position"].queryset = JobPosting.objects.filter(organization_id = organization)
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
            is_true = formset[0].cleaned_data.get('is_true')
            formset[0].save(for_question=question_)

        if formset[1].is_valid():
            content = formset[1].cleaned_data.get('content')
            is_true = formset[1].cleaned_data.get('is_true')
            formset[1].save(for_question=question_)

        if formset[2].is_valid():
            content = formset[2].cleaned_data.get('content')
            is_true = formset[2].cleaned_data.get('is_true')
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
def recruiter_position_quiz(request, position_id):
    organization = take_organization(request)
    position = JobPosting.objects.all().filter(organization_id=organization)
    print(position)
    quizzes = Quiz.objects.all().filter(job_position_id=position_id)
    print(quizzes)
    return render(request, 'recruiter/recruiter_position_quiz.html', {'quizzes': quizzes})


@login_required(login_url='/login') 
def recruiter_applications_overview(request):
    organization = take_organization(request)
    quiz = list(Quiz.objects.all().filter(organization_id=organization).values_list('id', flat=True))
    applications = Application.objects.all().filter(quiz_id__in=quiz)
    i = 0
    for app in applications:
        quiz_id = app.quiz_id
        quizes = Quiz.objects.get(id=quiz_id)
        applications[i].position = JobPosting.objects.get(id=quizes.job_position_id)
        applications[i].quiz_name = quizes.name
        applications[i].candidate_name = Candidate.objects.get(id=applications[i].candidate_id)
        i = i + 1
    return render(request,'recruiter/recruiter_applications_overview.html', {'applications': applications})


def recruiter_application_edit(request, application_id):
    application = Application.objects.get(id=application_id)
    quizes = Quiz.objects.get(id=application.quiz_id)
    application.position = JobPosting.objects.get(id=quizes.job_position_id)
    application.quiz_name = Quiz.objects.get(id=application.quiz_id).name
    application.candidate_name = Candidate.objects.get(id=application.candidate_id)

    questions = Question.objects.all().filter(quiz_id=application.quiz_id)
    results = QuizResult.objects.all().filter(application_id=application_id)
    for q in range(len(results)):
        questions_id = results[q].question
        answer_id = results[q].candidate_answer
        results[q].question_content = Question.objects.get(id=results[q].question)
        results[q].answer_content = Answer.objects.get(id=results[q].candidate_answer).content
    
    print(results)
    
    if request.method == 'POST':
        application_recruit_form = ApplicationRecruiterForm(request.POST, instance=application)
        if application_recruit_form.is_valid():
            status = application_recruit_form.cleaned_data.get('status')
            grade = application_recruit_form.cleaned_data.get('grade')
            application_recruit_form.save()
            return redirect('/recruiter/applications/')
    else:
        application_recruit_form = ApplicationRecruiterForm(instance=application)
    return render(request, 'recruiter/recruiter_application_edit.html', {'application': application, 'application_recruit_form': application_recruit_form, 'questions': questions, 'results': results})
