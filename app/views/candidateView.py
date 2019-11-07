from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from app.forms import SignUpForm, QuizAddForm, QuestionAddForm, AnswerAddForm, LoginForm, JobPostingAddForm, ApplicationAddForm, ApplicationRecruiterForm
from app.models import Organization, Recruiter, Candidate, Quiz, Question, Answer, JobPosting, User, Application, QuizResult
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory


@login_required(login_url='/login')
def candidate_home(request):
    user = User.objects.get(username=request.user)
    return render(request, 'candidate/candidate_home.html', {'user': user})


@login_required(login_url='/login')
def candidate_quiz_overview(request):
    quizzes = Quiz.objects.all().order_by('id')
    return render(request, 'candidate/candidate_quiz_overview.html', {'quizzes': quizzes})


@login_required(login_url='/login')
def candidate_add_application(request, quiz_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        candidate = Candidate.objects.get(user_id=user.id)
        for_candidate = candidate.id

        print(for_candidate)

    quiz_ = Quiz.objects.get(id=quiz_id)
    quiz_name = quiz_.name
    print(quiz_name)

    if request.method == 'POST':
        application_form = ApplicationAddForm(request.POST, request.FILES)
        if application_form.is_valid():
            description = application_form.cleaned_data.get('description')
            attachment = application_form.cleaned_data.get('attachment')
            application_form.save(for_candidate, quiz_id)
            application_id = application_form.take_id()
            print(application_id)
            return redirect('/candidate/quiz/%d/%d/' % (int(quiz_id), int(application_id),))
    else:
        application_form = ApplicationAddForm()
    return render(request, 'candidate/candidate_add_application.html', {'application_form': application_form, 'quiz_id': quiz_id,})


@login_required(login_url='/login')
def candidate_quiz_start(request, quiz_id, application_id):
    quiz_ = Quiz.objects.get(id=quiz_id)
    quiz_name = quiz_.name
    questions = Question.objects.all().filter(quiz_id=quiz_id)
    for q in range(len(questions)):
        questions_id = questions[q].id
        answers = Answer.objects.all().filter(question_id=questions_id)
        for answer in answers:
            answer.is_clicked = True
        questions[q].answers = answers

    if request.method == 'POST':
        point_counter = 0
        x = dict(request.POST)
        y = list(x.values())
        y.pop(0)
        for length in range(len(y)):
            answer_id = str(y[length]).replace("['", '')
            answer_id = str(answer_id).replace("']", '')
            answer = Answer.objects.get(id=answer_id)

            question_id = answer.question_id
            question = Question.objects.get(id=question_id)

            result = QuizResult.objects.create(application_id = application_id)
            result.question = question_id
            result.candidate_answer = answer_id
            result.save()
            
            if answer.is_true == 1:
                result.is_correct = 'True'
                result.save()
                point_counter = point_counter + 1
        application = Application.objects.filter(id=application_id).update(score=point_counter, full_score=len(questions))
        return redirect('/candidate/%d/score' % (int(application_id),))
     
    return render(request, 'candidate/candidate_quiz_start.html', {'quiz_name': quiz_name, 'quiz_id': quiz_id, 'questions': questions})


@login_required(login_url='/login')
def candidate_quiz_score(request, application_id):
    application = Application.objects.get(id=application_id)
    quiz_id = application.quiz_id
    questions = len(Question.objects.all().filter(quiz_id=quiz_id))
    return render(request, 'candidate/candidate_quiz_score.html', {'application': application, 'questions': questions})


@login_required(login_url='/login')
def candidate_position_overview(request):
    positions = JobPosting.objects.all().order_by('id')
    return render(request, 'candidate/candidate_position_overview.html', {'positions': positions})


@login_required(login_url='/login')
def candidate_position_quiz(request, position_id):
    position = JobPosting.objects.all()
    quizzes = Quiz.objects.all().filter(job_position_id=position_id)
    return render(request, 'candidate/candidate_position_quiz.html', {'quizzes': quizzes})


@login_required(login_url='/login')
def candidate_applications_overview(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        candidate = Candidate.objects.get(user_id=user.id)
        applications = Application.objects.all().filter(candidate_id=candidate.id)
        i = 0
        for app in applications:
            quiz_id = app.quiz_id
            quizes = Quiz.objects.get(id=quiz_id)
            applications[i].position = JobPosting.objects.get(id=quizes.job_position_id)
            applications[i].quiz_name = quizes.name
            i = i + 1
        return render(request, 'candidate/candidate_applications_overview.html', {'applications': applications})
