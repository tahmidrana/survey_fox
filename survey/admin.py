from django.contrib import admin
from .models import Questionnaire, Question, Answer, Survey, SurveyResponse


admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(SurveyResponse)