#coding=utf-8

from __future__ import unicode_literals

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django.settings")#
django.setup()

from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

template = get_template('LAVA_job_check/email_content_job_complete.html')
context = {'name':'dongpl', 'age':18}
res = HttpResponse(template.render(context))
print(template.render(context))


from_mail = settings.DEFAULT_FROM_EMAIL

my_to_addr = ['dongpl@spreadst.com']
my_subject = "lava_test_django"
my_content = "test here!!!"
msg = EmailMultiAlternatives(my_subject, my_content, from_mail, my_to_addr)
#msg.content_subtype = 'html'
msg.attach_alternative(str(template.render(context)), 'text/html')
msg.send()
