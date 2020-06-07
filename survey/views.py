from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Question, Answer, Survey, SurveyResponse
from .forms import QuestionnaireForm, QuestionForm
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    questionnaires = Questionnaire.objects.select_related('creator').order_by('-created_at')
    paginator = Paginator(questionnaires, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "survey/index.html", context)

@login_required(login_url='login')
def my_surveys(request):
    user = request.user
    questionnaires = Questionnaire.objects.filter(creator=user).order_by('-created_at')
    context = {
        'questionnaires': questionnaires
    }
    return render(request, "survey/my_surveys.html", context)


def view_questionnaire(request, id):
    # questionnaire = get_object_or_404(Questionnaire, pk=id)
    questionnaire = Questionnaire.objects.select_related('creator').prefetch_related('surveys').prefetch_related('questions__answers').get(pk=id)
    return render(request, 'survey/view_survey.html', {'questionnaire': questionnaire})

@login_required(login_url='login')
def publish_questionnaire(request, id):
    questionnaire = get_object_or_404(Questionnaire, pk=id)
    questionnaire.is_published = True
    questionnaire.save()
    messages.success(request, 'Your survey is now live!')
    return redirect("survey.view_questionnaire", id=id)

@login_required(login_url='login')
def close_questionnaire(request, id):
    questionnaire = get_object_or_404(Questionnaire, pk=id)
    questionnaire.is_completed = True
    questionnaire.save()
    messages.success(request, 'Your survey closed successfully!')
    return redirect("survey.view_questionnaire", id=id)

def entry_survey(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email", None)

        survey = Survey(name=name, email=email, questionnaire=Questionnaire.objects.get(pk=id))
        survey.save()

        questions = request.POST.getlist("questions")
        for question in questions:
            answers = request.POST.getlist("answers"+question)
            for ans in answers:
                survey_resp = SurveyResponse(survey=survey, question=Question.objects.get(pk=question), answer=Answer.objects.get(pk=ans))
                survey_resp.save()
        messages.success(request, 'Your survey response saved successfully!')
        return HttpResponseRedirect("/")
    else:
        questionnaire = Questionnaire.objects.select_related('creator').prefetch_related('surveys').prefetch_related('questions__answers').get(pk=id)
        context = {
            'questionnaire': questionnaire
        }
    return render(request, 'survey/entry_survey.html', context)


@login_required(login_url='login')
def new_questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            questionnaire = Questionnaire(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                response_type=form.cleaned_data["response_type"],
                is_published=form.cleaned_data["is_published"],
                creator=request.user
            )
            questionnaire.save()
            messages.success(request, 'Your survey created successfully!')
            return HttpResponseRedirect('/')
    else:
        form = QuestionnaireForm()

    return render(request, 'survey/new_survey.html', {'form': form})

@login_required(login_url='login')
def delete_questionnaire(request, id):
    questionnaire = get_object_or_404(Questionnaire, pk=id)
    try:
        questionnaire.delete()
        messages.success(request, 'Your survey deleted successfully!')
    except Exception:
        messages.error(request, 'Your survey delete failed!')

    return HttpResponseRedirect('/')


@login_required(login_url='login')
def new_question(request, questionnaire_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question(
                title=form.cleaned_data["title"],
                questionnaire=Questionnaire.objects.get(pk=questionnaire_id)
            )
            question.save()
            for i in range(1, 5):
                ans_data = form.cleaned_data["answer_field"+str(i)]
                if ans_data:
                    ans = Answer(title=ans_data, question=question)
                    ans.save()
            messages.success(request, 'Your question created successfully!')
            return redirect('survey.new_question', questionnaire_id=questionnaire_id)
    else:
        form = QuestionForm()
    return render(request, 'survey/new_question.html', {'form': form, 'id': questionnaire_id})


@login_required(login_url='login')
def delete_question(request, questionnaire_id, id):
    question = get_object_or_404(Question, pk=id)
    try:
        question.delete()
        messages.success(request, 'Deleted successfully!')
    except Exception:
        messages.error(request, 'Delete failed!')
    return redirect('survey.view_questionnaire', id=questionnaire_id)