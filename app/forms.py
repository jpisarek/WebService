from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Candidate, Quiz, Question, Answer, JobPosting, Application
from django.forms import ModelForm, Textarea, TextInput, FileField, ClearableFileInput

class SignUpForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ('first_name', 'last_name', 'email', 'description')


class QuizAddForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'job_position')
        labels = {
            'name': 'Tytuł quizu',
            'job_position': 'Pozycja'
        }

    def take_id(self):
        for_quiz = self.instance.id
        return for_quiz

    def save(self, for_organization):
        self.instance.organization_id = for_organization
        return super().save()


class QuestionAddForm(ModelForm):
    class Meta:
        model = Question
        fields = ('content',)
        labels = {
            'content': 'Pytanie'
        }
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 5}),
        }

    def save(self, for_quiz):
        self.instance.quiz = for_quiz
        return super().save()

    def take_id(self):
        for_question = self.instance.id
        return for_question


class AnswerAddForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('content', 'is_boolean',)
        labels = {
            'content': 'Odpowiedź',
            'is_boolean': 'Poprawna'
        }
        widgets = {
            'content': Textarea(attrs={'cols': 100, 'rows': 2}),
        }

    def save(self, for_question):
        self.instance.question = for_question
        return super().save()


class JobPostingAddForm(ModelForm):
    class Meta:
        model = JobPosting
        fields = ('job_position', 'description')
        labels = {
            'job_position': 'Pozycja',
            'description': 'Opis stanowiska'
        }

    def save(self, for_organization):
        self.instance.organization_id = for_organization
        return super().save()


class ApplicationAddForm(ModelForm):
    class Meta:
        model = Application
        fields = ('description', 'attachment')
        labels = {
            'description': 'Opis swojej osoby',
            'attachment': 'Załącznik'
        }
        widgets = {
            'description': Textarea(attrs={'cols': 100, 'rows': 2}), 
            'attachment': ClearableFileInput(attrs={'multiple': True})
        }

    def save(self, for_candidate, for_quiz):
        self.instance.candidate_id = for_candidate
        self.instance.quiz_id = for_quiz
        return super().save()

    def take_id(self):
        for_application = self.instance.id
        return for_application


class ApplicationRecruiterForm(ModelForm):
    class Meta:
        model = Application
        fields = ('status', 'grade')
        labels = {
            'status': 'Status',
            'grade': 'Ocena',
        }

        
class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

        widgets = {
            'password': TextInput(attrs={'type': 'password'})
        }