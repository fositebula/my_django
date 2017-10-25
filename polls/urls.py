from django.conf.urls import url
from . import views

# urlpatterns = [
#     url(r'^$', views.index, name='polls_index'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='polls_detail'),
#     url(r'^(?P<question_id>[0-9]+)/result/$', views.results, name='polls_results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='polls_vote'),
#     #url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
# ]
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='polls_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='polls_detail'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultsView.as_view(), name='polls_results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='polls_vote'),
]