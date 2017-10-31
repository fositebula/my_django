from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='submission_index'),
    url(r'^modifyInfo/$', views.modify_info_iterm, name='modify_info'),
    url(r'^modifyInfo/saveInfo/$', views.save_info_iterm, name='save_info'),
    url(r'^addInfo/$', views.AddProjectInfo, name='add_info'),
    url(r'^addInfo/saveInfo/$', views.save_info_iterm, name='save_info'),
    url(r'^search_info/result/$', views.SearchProjectInfo, name='search_info'),
    url(r'^update_info/$', views.update_branch_project_infos, name='update_info'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='polls_detail'),
    # url(r'^(?P<pk>[0-9]+)/result/$', views.ResultsView.as_view(), name='polls_results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='polls_vote'),
]