import urllib.request
from django.conf import settings
import os, json, csv
from django.http import HttpResponse
from app.models import *
from django.utils import safestring 
from collections import defaultdict
from django.views import View
from django.shortcuts import render, redirect
from app.forms import site_management_forms


#******************************************************************************
# LOAD RELIGIONS INTO DB
#******************************************************************************   

RELIGIONS_LIST = os.path.join(settings.STATICFILES_DIRS[0], 'site_managers', 'app_religion.csv')
CASTE_LIST = os.path.join(settings.STATICFILES_DIRS[0], 'site_managers', 'app_caste.csv')


def load_religions_into_db(request):

    Religion.objects.all().delete()

    with open(RELIGIONS_LIST) as rel_file:

        rel_reader = csv.reader(rel_file, delimiter=',')
        
        line_count = 0
        for row in rel_reader:
        
            if line_count >= 1:
                
                rel = Religion(
                    id =  row[0],
                    religion_name = row[1]
                )
                
                rel.save()
                
                with open(CASTE_LIST) as cas_file:
                    cas_reader = csv.reader(cas_file, delimiter=',')
        
                    for cas in cas_reader:
                        if cas[3] == row[0]:
                        
                            caste = Caste(
                                id = cas[0],
                                religion = rel,
                                caste_name = cas[1]
                            )
                            
                            caste.save()                
            line_count += 1
            
    return HttpResponse('1')
    

#******************************************************************************
# LOAD COUNTRIES INTO DB
#******************************************************************************   

COUNTRIES_LIST = os.path.join(settings.STATICFILES_DIRS[0], 'site_managers')
COUNTRIES_LIST = os.path.join(COUNTRIES_LIST,'countries+states+cities.txt')


def add_countries_to_db(request):

    with open(COUNTRIES_LIST, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        Countries.objects.all().delete()
        Countries_States.objects.all().delete()
        Countries_Cities.objects.all().delete()
        
        for row in data:
            country = Countries(
                country_name = row["name"]
            )
            
            country.save()
            
            
            for state in row["states"]:
                if "name" in state.keys():            
                    if state["name"]:
                    
                        state_ins = Countries_States(
                            country = country,
                            state_name = state["name"]
                        )
                        
                        state_ins.save()
                        
                    for city in state["cities"]:
                    
                        city_ins = Countries_Cities(
                            country = country,
                            state_name = state_ins,
                            city_name = city["name"]
                        )
                    
                        city_ins.save()
                
                else:
                    for city in state["cities"]:
                    
                        city_ins = Countries_Cities(
                            country = country,
                            state_name = state_ins,
                            city_name = city["name"]
                        )
                    
                        city_ins.save()
            
                print(state["name"])
            
    return HttpResponse('1')
    

#******************************************************************************
# FETCH STATES HTML DROPDOWN
#****************************************************************************** 

def get_states_dropdown(request):
    
    id = request.POST.getlist("ids[]")
    
    
    if len(id) > 0 :
    
        html = ["<option value='0'>Any State</option>"]
    
          
        states = Countries_States.objects.filter(country__in = id)

        if states is not None:
            for state in states:
                html.append("<option value='{0}'>{1}</option>".format(state.id, state))
            return HttpResponse(safestring.mark_safe(''.join(html)))
        else:
            return HttpResponse('')
            
            
#******************************************************************************
# FETCH CITIES HTML DROPDOWN
#****************************************************************************** 

def get_cities_dropdown(request):
    
    id = request.POST.getlist("ids[]")
    
    if len(id) > 0 :
    
        html = ["<option value='0'>Any City</option>"]
                  
        cities = Countries_Cities.objects.filter(state_name__in = id)

        if cities is not None:
            for city in cities:
                html.append("<option value='{0}'>{1}</option>".format(city.id, city))
            return HttpResponse(safestring.mark_safe(''.join(html)))
        else:
            return HttpResponse('')          


#******************************************************************************
# RELIGION MANAGEMENT
#****************************************************************************** 
           
           
class ReligionManagementView(View):
    
    data = defaultdict()
    
    template_name = 'app/base/base.html'
    
    data["included_template"] = 'app/staff/religion_management.html'

    data["page_title"] = "Site Management"
    
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/site_management.js']
    
    
    def get(self, request):
    
        self.data["re_list"] = defaultdict()
    
        re_list = Religion.objects.all().values_list('id', 'is_active', 'religion_name')
        cas_list = Caste.objects.all().values_list('id', 'is_active', 'religion', 'caste_name')
        
        for x in re_list:   
            self.data["re_list"][x[0]] = {"castes":[],"is_active":x[1],  "name":x[2]}
            
            for y in cas_list:                
                if y[2] == x[0]:
                    self.data["re_list"][x[0]]["castes"].append(y)
                    
        
        self.data["add_religion_form"] = site_management_forms.AddReligionForm(prefix='rel')
        
        self.data["add_caste_form"] = site_management_forms.AddCasteForm(prefix='cas')
        
        
        return render(request, self.template_name, self.data)
 
 
#******************************************************************************
# ADD RELIGION 
#****************************************************************************** 
 
def add_religion(request):
    
    if request.POST:
    
        add_rel = site_management_forms.AddReligionForm(request.POST, prefix='rel')
        
        if add_rel.is_valid():
            add_rel.save()
            return HttpResponse(json.dumps({'code':'1', 'error':''}))
        else:         
            return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(add_rel.errors)}))
    return HttpResponse(json.dumps({'code':'0', 'error':'In-Valid Request'}))
    

#******************************************************************************
# ADD CASTE 
#****************************************************************************** 

def add_caste(request):
    
    if request.POST:
    
        add_rel = site_management_forms.AddCasteForm(request.POST, prefix='cas')
    
        if add_rel.is_valid():
            add_rel.save()
            return HttpResponse(json.dumps({'code':'1', 'error':''}))
        else:         
            return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(add_rel.errors)}))
    return HttpResponse(json.dumps({'code':'0', 'error':'In-Valid Request'}))



#******************************************************************************
# DELETE CASTE 
#****************************************************************************** 

def delete_caste(request, ins=None):
    
    if ins is not None:
        try:
            cas = Caste.objects.get(pk = ins)
            cas.delete()
        except:
            pass
    return redirect("/staff/religion-management/")
  
  
#******************************************************************************
# DELETE RELIGION 
#****************************************************************************** 

def delete_religion(request, ins=None):
    
    if ins is not None:
        try:
            rel = Religion.objects.get(pk = ins)
            rel.delete()
        except:
            pass
    return redirect("/staff/religion-management/")    
    
    
#******************************************************************************
# CASTES DROPDOWN
#****************************************************************************** 

def get_castes_dropdown(request):
    
    if request.POST:
        
        id = request.POST.getlist("ids[]")
        
        if len(id) > 0 :
        
            html = []
    
            castes = Caste.objects.filter(religion__in = id)
            
            if castes is not None:
                for caste in castes:
                    html.append("<option value='{0}'>{1}</option>".format(caste.id, caste.caste_name))
                return HttpResponse(safestring.mark_safe(''.join(html)))
            else:
                return HttpResponse('')   
    