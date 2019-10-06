from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Candidate, Quiz, Question, Answer
from django.forms import ModelForm

class SignUpForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ('first_name', 'last_name', 'email', 'description')


class QuizAddForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('organization', 'name', 'level')

    def take_id(self):
        for_quiz = self.instance.id
        return for_quiz



class QuestionAddForm(ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'content')


class AnswerAddForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('content', 'question', 'is_boolean')