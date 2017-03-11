from django.shortcuts import render
from .models import Questions
from flask_mongoengine import Pagination
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator

PER_PAGE = 20

class IndexView(ListView):
    template_name = 'QADoorWebDjangoApp/index.html'
    # 制定获取的model数据列表的名字
    context_object_name = "questions"

    def get_queryset(self):
        """
        过滤数据，获取已发布文章列表，并转为html格式
        Returns:
        """
        questions = Questions.objects
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body,)
        return questions

    # 为上下文添加额外的变量，以便在模板中访问

    # def get_context_data(self, **kwargs):
    #     return super(IndexView, self).get_context_data(**kwargs)


def question_index(request):
    # paginate = Questions.query.filter(Questions.id).paginate(page, PER_PAGE)
    question_list = Questions.objects[:20]
    # print('questions',question_list)
    questions = question_list
    return questions
    # page = request.GET.get('page', 1)
    # paginator = Paginator(question_list, PER_PAGE)
    # questions = paginator.page(page)
    # print(dir(questions))
    # context = {
    #     'questions': questions,
    #     'total_pages': paginator.page_range
    # }
    # return render(request, 'QADoorWebDjangoApp/index.html', context)

    # page = request.GET.get('page', 1)
    # pagination = Questions.objects.paginate(page=page, per_page=PER_PAGE)
    # print(pagination)
    #
    # return render(request, 'QADoorWebDjangoApp/index.html', {'questions': pagination.items,
    #                                       'pagination': pagination}
    #               )


def question_search(request):
    # keyword = request.form['key']
    # keyword = request.form['key']
    page = request.GET.get('page', 1)
    keyword = request.GET.get('key', '')
    questions = Questions.objects(title__icontains=keyword)
    pagination = Pagination(questions, page=page, per_page=PER_PAGE)
    return render(request, 'QADoorWebDjangoApp/index.html', {'questions':pagination.items,
                                          'pagination': pagination}
                  )


def question_tag(request, tag):
    page = request.GET.get('page', 1)
    # paginate = Questions.query.filter(Questions.tags.like('%'+tag+'%')).paginate(page, PER_PAGE)
    questions = Questions.objects(tags=tag)
    pagination = Pagination(questions, page=page, per_page=PER_PAGE)
    return render(request, 'QADoorWebDjangoApp/index.html', {'questions': pagination.items,
                                          'pagination': pagination}
                  )


def question_detail(request, question_id):
    # question = Questions.query.filter(Questions.question_id==question_id).one()
    question = Questions.objects.get_or_404(_id=question_id)
    print(question.content)
    return render(request, 'QADoorWebDjangoApp/question_detail.html', {'question':question})


def not_found(request, error):
    return render(request, 'QADoorWebDjangoApp/404.html')
