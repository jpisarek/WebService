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
      

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return str(self.first_name + " " + self.last_name)


class JobPosting(models.Model):
    job_position = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.job_position)


class Quiz(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    job_position = models.ForeignKey(JobPosting, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('recruiter_question_add', args=[self.id])


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)

    def __str__(self):
        return str(self.content)


class Answer(models.Model):
    content = models.CharField(max_length=500)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_true)


class Application(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    attachment = models.FileField()
    score = models.IntegerField(default=0)
    full_score = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="Rozpatrywana")
    grade = models.IntegerField(default=0)

    def __str__(self):
        return str(self.quiz)


class QuizResult(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    candidate_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.candidate_answer)
    
