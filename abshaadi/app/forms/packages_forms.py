from django.forms import *
from app.models import *

     
#******************************************************************************
# PACKAGE FORM
#******************************************************************************          
       
class AddPackageForm(ModelForm):
    
    class Meta:
        model = Package
        
        fields = ('package_name', 'value', 'tenure', 'tenure_types', 'description')
        
        widgets = {
            'package_name' : TextInput(attrs = {'class':'form-control', 'required':'true'}), 
            'value' : NumberInput(attrs = {'class':'form-control', 'required':'true'}), 
            'tenure' : NumberInput(attrs = {'class':'form-control', 'required':'true'}), 
            'tenure_types' : Select(attrs = {'class':'form-control', 'required':'true'}), 
            'description' : Textarea(attrs = {'class':'form-control', 'required':'true', 'rows':'3'}),
        }
        
    
class EditPackageForm(ModelForm):
    
    class Meta:
        model = Package
        
        fields = ('package_name', 'value', 'tenure', 'tenure_types', 'description','is_active')
        
        widgets = {
            'package_name' : TextInput(attrs = {'class':'form-control', 'required':'true'}), 
            'value' : NumberInput(attrs = {'class':'form-control', 'required':'true'}), 
            'tenure' : NumberInput(attrs = {'class':'form-control', 'required':'true'}), 
            'tenure_types' : Select(attrs = {'class':'form-control', 'required':'true'}), 
            'description' : Textarea(attrs = {'class':'form-control', 'required':'true', 'rows':'3'}),
            'is_active' : Select(attrs = {'class':'form-control', 'required':'true'}), 
        }