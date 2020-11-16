from django.forms import *
from app.models import *
from django.conf import settings 

from app.constants import form_constants

import glob, os


#******************************************************************************
# ADD RELIGION FORM
#******************************************************************************    

class AddReligionForm(ModelForm):
 
    class Meta:
        model = Religion
        fields = ('religion_name', 'is_active')
        
        widgets = {
            'religion_name' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'is_active' : Select(attrs = {'class':'form-control', 'required':'true',}, choices=((True, 'Yes'),(False, 'No'))),
        }
        

#******************************************************************************
# ADD CASTE FORM
#******************************************************************************    
        
class AddCasteForm(ModelForm):
 
    class Meta:
        model = Caste
        fields = ('caste_name', 'religion', 'is_active')
        
        widgets = {
            'caste_name' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'religion' : Select(attrs = {'class':'form-control', 'required':'true'}),
            'is_active' : Select(attrs = {'class':'form-control', 'required':'true',}, choices=((True, 'Yes'),(False, 'No'))),
        }        