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
from app.forms import packages_forms


#******************************************************************************
# STAFF DASHBOARD
#******************************************************************************    

class PackageManagementView(View):

    template_name = 'app/base/base.html'
    
    data = defaultdict()

    data["included_template"] = 'app/staff/package_management.html'

    data["page_title"] = "Package Management"
    
    data["css_files"] = []
    data["js_files"] = []
    
    #
    #
    #
    
    def get(self, request):
    
        self.data["packages"] = Package.objects.all()
        
        self.data["add_package_form"] = packages_forms.AddPackageForm()

         # edit pacakge management form

        edit_package_form = Package.objects.all()
        count = len(edit_package_form)

        self.data["count"] = [i for i in range(count)]
            
        self.data["edit_package_form"] = []
        
        for i in range(count):
            self.data["edit_package_form"].append(packages_forms.EditPackageForm(instance = edit_package_form[i], prefix = 'form_{}'.format(edit_package_form[i].id)))

        
        return render(request, self.template_name, self.data)
    
    def post(self, request):
        add_package_form = packages_forms.AddPackageForm(request.POST)

        if add_package_form.is_valid():
            inc = add_package_form.save(commit=False)
            inc.user = request.user
            inc.save()       
        else:
            print(add_package_form.errors.as_data())
        return redirect('/staff/package_management/view/', self.data)

#=======================================================================================
#   EDIT PACKAGE MANAGEMENT
#=======================================================================================
#
def edit_package_management(request):

    if request.POST:
# form_1-package_name
        keys = [i for i in request.POST.keys() if "package_name" in i]

        prefix = keys[0].replace("-package_name", "").replace("form_", "")

        try:
            obj = Package.objects.get(pk = int(prefix))    
        except:
            return redirect("/unauthorized/",permanent=False)

        edit_package_form = packages_forms.EditPackageForm(request.POST, prefix='form_'+prefix, instance = obj)
        if edit_package_form.is_valid():
            ins = edit_package_form.save()
            ins.save() 
        
        return redirect('/staff/package_management/view/',permanent = False)

#=======================================================================================
#   delete PACKAGE MANAGEMENT
#=======================================================================================
#
def delete_package_management(request,ins):
    Package.objects.get(pk = ins).delete()
    return redirect('/staff/package_management/view/',permanent = False)