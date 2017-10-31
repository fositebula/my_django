# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from .models import VerifyProjectInfo, LavaServerInfo,
from django.http import HttpResponse
from .form import ProjectInfoFrom
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


import requests
import re

from .models import BranchProjectInfo

verify_8_0_url = "http://10.0.64.29:8080/jenkins/job/gerrit_do_verify_sprdroid8.x/build?delay=1sec"
baidu_url = "http://www.baidu.com"

def get_branch_project_info_from_jenkins(verify_url):
    r = requests.get(verify_url)
    t = re.findall("<option value=\"(.*?)\">.*?</option>", r.text)

    infos = {}
    for project_info in t:
        if ":" in project_info:
            ii = project_info.strip().split(":")
            if infos.has_key(ii[0]):
                infos[ii[0]].append(ii[1])
            else:
                infos[ii[0]] = [ii[1]]
    return infos

def db_save_branch_project_infos(infos):
    for branch_info in infos.keys():
        p_info = BranchProjectInfo.objects.filter(Q(branch_name=))



# Create your views here.
class IndexView(generic.ListView):
    template_name = "lava_submission/submission_index.html"
    context_object_name = 'project_infos'

    def get_queryset(self):
        infos =  VerifyProjectInfo.objects.order_by('-modify_date')
        if infos.count() == 0:
            return HttpResponse("No polls are available")
        else:
            return infos

    def get_context_data(self, **kwargs):
        infos = VerifyProjectInfo.objects.order_by('-modify_date')
        context = super(IndexView, self).get_context_data(**kwargs)
        context['query_len'] = infos.count()
        context['project_infos'] = infos
        return context
        # if VerifyProjectInfo.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] == []:
        #     return HttpResponse("No polls are available")
        # return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    #def render_to_response(self, context, **response_kwargs):


def AddProjectInfo(request):
    if request.method == "POST":
        #info = VerifyProjectInfo.objects.create()
        pform = ProjectInfoFrom(request.POST)
        return HttpResponse(render(request, 'lava_submission/add_project_info.html', {"project_form":pform}))
    else:
        raise Http404('Method not POST')

def modify_info_iterm(request):
    if request.method == "POST":
        info = VerifyProjectInfo.objects.get(pk=request.POST['edit'])
        pform = ProjectInfoFrom(instance=info)
        return HttpResponse(render(request, 'lava_submission/add_project_info.html', {"project_form":pform, "infoID":info.id}))
    else:
        raise Http404('Method not POST')
def save_info_iterm(request):
    if request.method == "POST":
        pk = request.POST['infoID']
        if pk:
            info = VerifyProjectInfo.objects.get(pk=pk)
            form = ProjectInfoFrom(request.POST, instance=info)
            form.save()
            return HttpResponseRedirect(reverse('lava_submission:submission_index'))
        else:
            form = ProjectInfoFrom(request.POST)
            form.save()
            return HttpResponseRedirect(reverse('lava_submission:submission_index'))

    else:
        raise Http404('Method not POST')

def SearchProjectInfo(request):
    searched_results = []
    if request.method == "POST":
        template = get_template("lava_submission/search_info_results.html")
        searched_info = request.POST['searched_info'].strip()
        searched_results = VerifyProjectInfo.objects.filter(Q(branch_name__contains=searched_info) |
                                                         Q(project_name__contains=searched_info) |
                                                         Q(device_type__contains=searched_info))
        context = {"project_infos":searched_results}

        return HttpResponse(template.render(context))
    else:
        raise Http404('Method not POST')

def update_branch_project_infos(request):
    web_infos = get_branch_project_info_from_jenkins(verify_8_0_url)
    db_save_branch_project_infos(web_infos)
    return HttpResponseRedirect(reverse('lava_submission:submission_index'))
