from django import forms
from .models import VerifyProjectInfo, LavaServerInfo, VerifyBranchType
from django.core.exceptions import NON_FIELD_ERRORS

# class AddProjectInfo(forms.Form):
#
#     branch_name = forms.CharField(label='branch name', max_length=100)
#     project_name = forms.CharField(label='project name', max_length=100)
#     managers_mail = forms.EmailField(label='managers email', max_length=100)
#     task_type = forms.CharField(label='task type', max_length=100)
#     device_type = forms.CharField(label='device type', max_length=100)
#     stop_flag = forms.BooleanField(label='stop', max_length=100)
#     device_in_server = forms.ModelForm(m)
#     modify_date = forms.CharField(label='modify date', max_length=100)

class ProjectInfoFrom(forms.ModelForm):
    class Meta:
        model = VerifyProjectInfo
        fields = ["branch_project_info", "managers_mail", "task_type", "device_type",
                  "stop_flag", "device_in_server"]
        error_messages = {
            NON_FIELD_ERRORS:{
                'unique_together':"%(model_name)'s %(field_labels)s are not unique.",
            }
        }
        # widgets = {
        #     'branch_name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        #     'project_name': forms.
        # }


class ProjectInfoForm(forms.Form):
    # DEVICE_TYPE = (
    #     ('verify', 'verify'),
    #     ('daily', 'daily'),
    #     ('manual', 'manual'),
    # )
    # BRANCH_TYPE = (
    #     ('Android 8.0', 'Android 8.0'),
    #     ('Android 7.0', 'Android 7.0'),
    # )
    # branch_type_str = forms.CharField(max_length=50)
    # branch_project_info = forms.ModelChoiceField(
    #     queryset=VerifyProjectInfo.objects.filter(branch_type__name="Android 8.0")
    # )
    # managers_mail = forms.EmailField(max_length=254)
    # task_type = forms.CharField('Task Type', max_length=20, choices=DEVICE_TYPE)
    # device_type = forms.CharField('Device Type', max_length=50)
    # stop_flag = forms.BooleanField('Stopping Test', default=False)
    # device_in_server = forms.ModelChoiceField(queryset=LavaServerInfo.objects.all())
    # modify_date = forms.DateField(auto_now=True)
    # branch_type = forms.ModelChoiceField(queryset=VerifyBranchType.objects.get(name=branch_type_str))
    pass