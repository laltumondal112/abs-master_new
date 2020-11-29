#
# AUTHOR : LAWRENCE GANDHAR
#
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import *
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import sys, os, json

from django.utils import safestring

from django.contrib.auth.hashers import make_password

from collections import defaultdict

from app.forms.registration_forms import RegisterForm

from app.models import *


from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

#******************************************************************************
# LOGOUT SIGNALS
#******************************************************************************


@receiver(user_logged_out)
def post_login(sender, user, request, **kwargs):
    cus = CustomUser.objects.get(pk = request.user.id)
    cus.online_now = False
    cus.save()


#******************************************************************************
# 403 Page
#******************************************************************************

def page_403(request):
    return render(request, 'app/base/403_error.html')



#******************************************************************************
# HOMEPAGE
#******************************************************************************

def check_registered_email(email=None):
    if email is not None:
        try:
            user = CustomUser.objects.filter(username__iexact = email)
            return 2
        except:
            return 1
    return 3


#
#******************************************************************************
# HOMEPAGE
#******************************************************************************

class HomeView(View):

    template_name = 'app/base/home.html'
    data = defaultdict()

    def get(self, request):

        self.data["register_form"] = RegisterForm()

        return render(request, self.template_name, self.data)


#
#******************************************************************************
# LOGIN
#******************************************************************************

class LoginView(View):

    template_name = 'app/base/login.html'

    data = defaultdict()

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/common.js',]

    def get(self, request):

        self.data["register_form"] = RegisterForm()

        return render(request, self.template_name, self.data)


    def post(self, request):

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                cus = CustomUser.objects.get(pk = user.id)
                cus.online_now = True
                cus.save()

                return HttpResponse('1')
        else:
            return HttpResponse('Invalid username or password')


#
#******************************************************************************
#
#******************************************************************************

def my_redirect_page(request):

    if request.user.is_staff or request.user.is_superuser:
        return redirect('/staff/dashboard/', permanent=True)
    else:
        return redirect('/dashboard/', permanent=True)



#
#******************************************************************************
#
#******************************************************************************

def register_form(request):
    if request.POST:

        email = request.POST.get('email', None)
        #
        #
        #

        if email is not None:
            reg_form = RegisterForm(request.POST)

            chk_email = check_registered_email(email)

            if chk_email == 2:
                return HttpResponse("Email is already registered")

            elif chk_email == 3:
                return HttpResponse("Email cannot be blank")
            else:

                if reg_form.is_valid():
                    reg = reg_form.save(commit=False)
                    reg.is_staff = False
                    reg.is_superuser = False

                    reg.save()

                    path = os.path.join(settings.MEDIA_ROOT, str(reg.id))
                    os.mkdir(path, 0o777)

                    profile = Profile(
                        user = reg
                    )

                    profile.save()
                    cus = CustomUser.objects.get(email = email)
                    pr=Profile.objects.get(user_id=cus.pk)
                    abisaadi_id=pr.uid
                    print(pr.uid)
                    send_email_from_app(email,abisaadi_id)

                    return HttpResponse(json.dumps({'code':'1', 'error':''}))

                else:
                    print(reg_form.errors)
                    return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(reg_form.errors)}))

        else:
            return HttpResponse("Email cannot be blank")


def send_email_from_app(email,id):
    html_tpl_path = 'app/users/welcome.html'
    # pr=Profile.objects.get(user=request.user)
    context_data =  {'Email': email,'Abisaadi_id':id}
    email_html_template = get_template(html_tpl_path).render(context_data)
    receiver_email = email
    email_msg = EmailMessage('Welcome from ATUT BANDHAN SHAADI', 
                                email_html_template, 
                                settings. APPLICATION_EMAIL,
                                [receiver_email],
                                reply_to=[settings.APPLICATION_EMAIL]
                                )
    # this is the crucial part that sends email as html content but not as a plain text
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)


#======================================================================
# Change Password
#======================================================================
#

def change_password(request):
    if request.POST:
        if validate_password(request.POST["password1"]):
            request.user.set_password(request.POST["password1"])
            update_session_auth_hash(request, request.user)
            request.user.save()
            return HttpResponse("Password Changed Successfully")
        return HttpResponse('This password must contain at least 8 characters.')
    return HttpResponse(0)


#======================================================================
# Validate Password
#======================================================================
#

def validate_password(password):
    if len(password) < 8:
        return False
    return True
