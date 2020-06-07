"""survey_fox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from survey import views
from auth_app.forms import UserLoginForm
from auth_app import views as auth_app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sentry-debug/', views.trigger_error),
    path('', views.index, name="survey.index"),
    path('my-surveys', views.my_surveys, name="survey.my_surveys"),
    path('surveys/<int:id>', views.view_questionnaire, name="survey.view_questionnaire"),
    path('surveys/<int:id>/entry', views.entry_survey, name="survey.entry_survey"),
    path('surveys/new', views.new_questionnaire, name="survey.new_questionnaire"),
    path('surveys/<int:id>/publish', views.publish_questionnaire, name="survey.publish_questionnaire"),
    path('surveys/<int:id>/close', views.close_questionnaire, name="survey.close_questionnaire"),
    path('surveys/<int:id>/delete', views.delete_questionnaire, name="survey.delete_questionnaire"),
    path('surveys/<int:questionnaire_id>/new-question', views.new_question, name="survey.new_question"),
    path('surveys/<int:questionnaire_id>/questions/<int:id>/delete', views.delete_question, name="survey.delete_question"),
    path('login', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', auth_app_views.create_user, name='register'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns