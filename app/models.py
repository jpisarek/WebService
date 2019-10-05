from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse




class Organization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)
      

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class JobPosting(models.Model):
    job_possition = models.CharField(max_length=30)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Application(models.Model):
    job_possition = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='files/')
    status = models.CharField(max_length=50)


class Task(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class ApplicationTask(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    score = models.IntegerField()


class Quiz(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    name = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)


class Answer(models.Model):
    content = models.CharField(max_length=300)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_boolean = models.BooleanField(default=False)


class ApplicationQuiz(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()