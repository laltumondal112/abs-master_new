from django.forms import *
from app.models import *
from django.conf import settings 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.constants import form_constants

import glob, os
   
#
#
#

class CreateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'is_superuser',)
        
        widgets = {
            'first_name' : TextInput(attrs = {'class':'form-control',}),
            'last_name' : TextInput(attrs = {'class':'form-control',}),
            'email' : TextInput(attrs = {'class':'form-control', 'type':'email',}),
            'username' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'password' : TextInput(attrs = {'class':'form-control', 'type':'password', 'required':'true', 'id':'passwd1'}),
            'is_superuser' : Select(attrs = {'class':'form-control', 'required':'true',}, choices=((True, 'Yes'),(False, 'No')))
        }
 
#
#
#
class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        
        widgets = {
            'username' : TextInput(attrs = {'class':'form-control', 'required':'true', 'readonly':'true'}),
            'first_name' : TextInput(attrs = {'class':'form-control',}),
            'last_name' : TextInput(attrs = {'class':'form-control',}),
            'email' : TextInput(attrs = {'class':'form-control', 'type':'email',}),   
        }

   
#******************************************************************************
# PROFILE FORM
#******************************************************************************          
       
class EditProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('fullname', 'father_name', 'mother_name', 'height', 'weight', 'complexion', 'religion', 'caste_creed', 'qualification', 
            'job_details', 'phone_number', 'phone_number_alternative', 'address', 'descriptions', 'biodata', 'block_profile_pics'
        )
        
        widgets = {
            'fullname' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'father_name' : TextInput(attrs = {'class':'form-control',}),
            'mother_name' : TextInput(attrs = {'class':'form-control',}),
            'height' :  TextInput(attrs = {'class':'form-control', 'type':'integer'}),
            'weight' : TextInput(attrs = {'class':'form-control', 'type':'integer'}),
            'complexion' : Select(attrs = {'class':'form-control'}),
            'religion' : Select(attrs = {'class':'form-control'}),
            'caste_creed' : Select(attrs = {'class':'form-control'}),
            'qualification' : TextInput(attrs = {'class':'form-control',}),
            'job_details' : Textarea(attrs = {'class':'form-control',}),
            'phone_number': TextInput(attrs = {'class':'form-control',}),
            'phone_number_alternative' : TextInput(attrs = {'class':'form-control',}),
            'address' : Textarea(attrs = {'class':'form-control',}),
            'descriptions' : Textarea(attrs = {'class':'form-control',}),
            'biodata' : FileInput(attrs = {'class':'form-control',}), 
            'block_profile_pics' : Select(attrs = {'class':'form-control'}),
        }
       
