#coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")# project_name 项目名称
django.setup()

from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

template = get_template('./template/email_content_job_complete.html')

from_mail = settings.DEFAULT_FROM_EMAIL

my_to_addr = ['dongpl@spreadst.com']
my_subject = "lava_test_django"
my_content = "test here!!!"
msg = EmailMultiAlternatives(my_subject, my_content, from_mail, my_to_addr)
msg.content_subtype = 'html'

msg.send()

# send_mail('Subject here', 'Here is the message.', 'LAVA <lava@spreadtrum.com>',
#           ['dongpl@spreadst.com'], fail_silently=False)