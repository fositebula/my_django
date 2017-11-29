# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from .models import VerifyProjectInfo, LavaServerInfo, VerifyBranchType, BranchProjectInfo,DeviceType
from django.http import HttpResponse
from .form import ProjectInfoFrom, ProjectInfoForm
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelformset_factory

import requests
import re

import xmlrpclib

def get_lava_servers():
    server_infos = LavaServerInfo.objects.all()
    servers = []
    print ("http://%s:%s@%s/RPC2" % (info.submit_user_name
                              , info.submit_user_token
                              , info.server_hostname))
    for info in server_infos:
        server = xmlrpclib.ServerProxy("http://%s:%s@%s/RPC2" % (info.submit_user_name
                                                                 , info.submit_user_token
                                                                 , info.server_hostname))
        servers.append(server)
    return servers

def get_device_type_from_server():
    server_infos = LavaServerInfo.objects.all()
    for info in server_infos:
        server = xmlrpclib.ServerProxy("http://%s:%s@%s/RPC2" % (info.submit_user_name
                                                                 , info.submit_user_token
                                                                 , info.server_hostname))
        device_types = server.scheduler.device_types.list()
        for device_type in device_types:
            #print("####",DeviceType.objects.filter(name=device_type['name']))
            dt = DeviceType.objects.filter(name=device_type['name'])
            if dt.count()==0:
                dt = DeviceType(name=device_type['name'], lava_server=info)
                dt.save()


def get_branch_project_info_from_jenkins():
    bp_info = VerifyBranchType.objects.all()
    infos = {}
    try:
        for info in bp_info:
            r = requests.get(info.url_str)
            t = re.findall("<option value=\"(.*?)\">.*?</option>", r.text)

            for project_info in t:
                if ":" in project_info:
                    ii = project_info.strip().split(":")
                    if infos.has_key(ii[0]):
                        infos[ii[0]].append(ii[1])
                    else:
                        infos[ii[0]] = [ii[1]]
        return infos
    except Exception as e:
        Http404(e.message)

def db_save_branch_project_infos(infos):

    try:
        for branch_info in infos.keys():
            for p_info in infos[branch_info]:
                try:
                   q_set = BranchProjectInfo.objects.filter(Q(branch_name=branch_info)
                                                  &Q(project_name=p_info))
                   if q_set.count() == 0:
                        t_info = BranchProjectInfo(branch_name=branch_info, project_name=p_info)
                        t_info.save()

                except ObjectDoesNotExist:
                        Http404(e.message)
    except Exception as e:
        Http404(e.message)

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
        get_device_type_from_server()
        infos = VerifyProjectInfo.objects.order_by('-modify_date')
        branch_types = VerifyBranchType.objects.all()
        context = super(IndexView, self).get_context_data(**kwargs)
        context['query_len'] = infos.count()
        context['project_infos'] = infos
        context['branch_types'] = branch_types
        return context
        # if VerifyProjectInfo.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] == []:
        #     return HttpResponse("No polls are available")
        # return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    #def render_to_response(self, context, **response_kwargs):


def AddProjectInfo(request):
    if request.method == "POST":
        web_infos = get_branch_project_info_from_jenkins()
        db_save_branch_project_infos(web_infos)
        info = VerifyProjectInfo.objects.all()
        if info.count() != 0:
            pform = ProjectInfoFrom(instance=info.first())
        else:
            pform = ProjectInfoFrom(request.POST)
        return HttpResponse(render(request, 'lava_submission/add_project_info.html', {"project_form":pform.as_ul()}))

    else:
        raise Http404('Method not POST')

def modify_info_iterm(request):
    if request.method == "POST":
        info = VerifyProjectInfo.objects.get(pk=request.POST['edit'])
        pform = ProjectInfoFrom(instance=info)
        return HttpResponse(render(request, 'lava_submission/modify_project_info.html',
                                   {"project_form":pform.as_ul(), "infoID":info.id}))
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
            branch_type = VerifyBranchType.objects.get(pk=2)
            info = VerifyProjectInfo(branch_type=branch_type)
            form = ProjectInfoFrom(request.POST, instance=info)
            form.save()
            return HttpResponseRedirect(reverse('lava_submission:submission_index'))

    else:
        raise Http404('Method not POST')

def SearchProjectInfo(request):
    searched_results = []
    if request.method == "POST":
        template = get_template("lava_submission/search_info_results.html")
        searched_info = request.POST['searched_info'].strip()
        if searched_info == "True" or searched_info == "False":
            searched_results = VerifyProjectInfo.objects.filter(Q(stop_flag=searched_info))
        else:
            searched_results = VerifyProjectInfo.objects.filter(Q(branch_project_info__branch_name__contains=searched_info)|
                                                             Q(branch_project_info__project_name__contains=searched_info)|
                                                             Q(device_type__name__contains=searched_info)|
                                                             Q(task_type__contains=searched_info))
        context = {"project_infos":searched_results}

        return HttpResponse(template.render(context))
    else:
        raise Http404('Method not POST')

