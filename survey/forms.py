from django import forms
from .models import Questionnaire, Survey, SurveyResponse


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['title', 'description', 'response_type', 'is_published', 'email_required']

    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['description'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['response_type'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'


class QuestionForm(forms.Form):
    title = forms.CharField(label="Question", max_length=250)
    answer_field1 = forms.CharField(max_length=250)
    answer_field2 = forms.CharField(max_length=250)
    answer_field3 = forms.CharField(max_length=250, required=False)
    answer_field4 = forms.CharField(max_length=250, required=False)
    multi_choice = forms.BooleanField(label="Multiple Choice", required=False)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['answer_field1'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['answer_field2'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['answer_field3'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
        self.fields['answer_field4'].widget.attrs['class'] = 'block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
