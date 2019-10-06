"""WebService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
import sys
sys.path.append("..")
from app import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^register/', views.register_page, name='register_page'),
    # url(r'^login/', views.login_page, name='login_page'),
    url(r'^user/', include('django.contrib.auth.urls'), name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^recruiter/home', views.recruiter_home, name='recruiter_home'),
    url(r'^recruiter/rank', views.recruiter_rank, name='recruiter_rank'),
    url(r'^recruiter/quiz/add/', views.recruiter_quiz_add, name='recruiter_quiz_add'),
    url(r'^recruiter/quiz/(\d+)/question/', views.recruiter_question_add, name='recruiter_question_add'),
]
