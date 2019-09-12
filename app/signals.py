
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Recruiter
from django.contrib.auth.models import User