from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Candidate, Quiz, Question, Answer
from django.forms import ModelForm, Textarea

class SignUpForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ('first_name', 'last_name', 'email', 'description')


class QuizAddForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('organization', 'name', 'level')
        labels = {
            'organization': 'Organizacja',
            'name': 'Tytuł quizu',
            'level': 'Poziom'
        }

    def take_id(self):
        for_quiz = self.instance.id
        return for_quiz


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
        self.instance.name = for_quiz
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


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')