from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

app_name = 'QADoorWebDjangoApp'
urlpatterns = [
    url(r'^$', views.question_index, name='index'),
    url(r'^detail/(?P<question_id>\d+)$', cache_page(60 * 15)(views.question_detail), name='detail'),
    url(r'^search/$', views.question_search, name='search'),
    url(r'^tag/(?P<tag_name>.+)$', views.question_tag, name='tag'),
]