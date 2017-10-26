from django import forms
from .models import VerifyProjectInfo

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
        fields = ["branch_name", "project_name", "managers_mail", "task_type", "device_type",
                  "stop_flag", "device_in_server", "modify_date"]
