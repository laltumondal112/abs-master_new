#
# AUTHOR : LAWRENCE GANDHAR
# 
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.conf import settings
from app.models import * 
from app.forms import user_management_forms


#******************************************************************************
# USER MANAGEMENT VIEW
#******************************************************************************    

class UserManagementView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/user_management.html'

    data["page_title"] = "User Management"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/user_management.js']
    
    #
    #
    #
    
    def get(self, request):
        
        self.data["users"] = Profile.objects.all()
        
        return render(request, self.template_name, self.data)
   


#******************************************************************************
# STAFF MANAGEMENT VIEW
#******************************************************************************    

class StaffManagementView(View):
    
    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/staff_management.html'

    data["page_title"] = "User Management"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/user_management.js']
    
    #
    #
    #
    
    def get(self, request):
        
        self.data["users"] = CustomUser.objects.filter(is_staff = True)
        self.data["add_user_form"] = user_management_forms.CreateUserForm(auto_id="form_%s")
        
        return render(request, self.template_name, self.data)
   
  
#******************************************************************************
# ADD USER
#******************************************************************************    

def add_staff(request):
    if request.POST:
        add_staff = user_management_forms.CreateUserForm(request.POST, auto_id="form_%s")
    
        if add_staff.is_valid():
            add_staff.save(commit = False)
            add_staff.is_satff = True
            add_staff.save()
            return HttpResponse('1')
        else:
            return HttpResponse(add_staff.errors)
    return HttpResponse('0')
    
    

  
#******************************************************************************
# DELETE USER
#******************************************************************************    
    
def delete_user(request, ins=None):
    
    if ins is not None:
       
        try:
            CustomUser.objects.get(pk = ins).delete()
            return HttpResponse('1')
        except:
            return HttpResponse('2')
        
    return HttpResponse('0')
    