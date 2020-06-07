from django.db import models
from django.contrib.auth.models import User


class Questionnaire(models.Model):
    ONE_OF_RESPONSE = 1
    MULTIPLE_RESPONSE = 2
    RESPONSE_TYPES = (
        (ONE_OF_RESPONSE, 'One of response'),
        (MULTIPLE_RESPONSE, 'Multiple response'),
    )
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    response_type = models.SmallIntegerField(choices=RESPONSE_TYPES, default=1)

    is_published = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    email_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def creator_name(self):
        return self.creator.first_name if self.creator.first_name else self.creator.username

    def is_running(self):
        return (True if self.is_published == True and self.is_completed == False else False)

    def status(self):
        if self.is_completed is True:
            return 'completed'
        if self.is_published is False and self.is_completed is False:
            return 'unpublished'
        elif self.is_published is True and self.is_completed is False:
            return 'running'

    def can_perform_action(self):
        if self.is_published is False and self.is_completed is False and not self.surveys.exists():
            return True
        return False


class Question(models.Model):
    title = models.CharField(max_length=250)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions', db_index=True)
    multi_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", db_index=True)

    def __str__(self):
        return self.title


class Survey(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="surveys", db_index=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.questionnaire.title


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="survey_responses", db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, db_index=True)
