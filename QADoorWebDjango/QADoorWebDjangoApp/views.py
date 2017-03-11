from django.shortcuts import render, redirect
from .models import Questions
# from django.core.paginator import Paginator

def question_index(request):
    questions = Questions.objects
    context = {
        'questions': questions,
    }
    return render(request, 'QADoorWebDjangoApp/index.html', context)

def question_tag(request, tag_name):
    questions = Questions.objects.filter(tags=tag_name)
    context = {
        'questions': questions,
    }
    return render(request, 'QADoorWebDjangoApp/index.html', context)


def question_search(request,):
    search_for = request.GET['search_for']
    if search_for:
        questions = Questions.objects.filter(title__icontains=search_for)
        context = {
            'questions': questions,
        }
        return render(request, 'QADoorWebDjangoApp/index.html', context)
    else:
        return redirect('app:index')


def question_detail(request, question_id):
    question = Questions.objects.filter(_id=question_id).first()
    return render(request, 'QADoorWebDjangoApp/detail.html', {'question':question})


def not_found(request, error):
    return render(request, 'QADoorWebDjangoApp/404.html')
