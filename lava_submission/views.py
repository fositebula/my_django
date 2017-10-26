# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from .models import VerifyProjectInfo, LavaServerInfo
from django.http import HttpResponse
from .form import ProjectInfoFrom
from django.shortcuts import render

# Create your views here.
class IndexView(generic.ListView):
    template_name = "lava_submission/submission_index.html"
    context_object_name = 'project_infos'

    def get_queryset(self):
        infos =  VerifyProjectInfo.objects.order_by('-modify_date')
        if len(infos) == 0:
            return HttpResponse("No polls are available")
        return infos
        # if VerifyProjectInfo.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] == []:
        #     return HttpResponse("No polls are available")
        # return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def AddProjectInfo(request):
    #if request.method == "POST":
    info = VerifyProjectInfo.objects.get(pk=1)
    pform = ProjectInfoFrom(instance=info)
    return HttpResponse(render(request, 'lava_submission/add_project_info.html', {"project_form":pform}))
