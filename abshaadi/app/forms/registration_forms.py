from django.forms import *
from app.models import *
from django.conf import settings

from app.constants import form_constants

import glob, os

from django.contrib.auth.forms import UserCreationForm



#******************************************************************************
# REGISTRATION FORM
#******************************************************************************

class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

        widgets = {
            'email' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
        }



#******************************************************************************
# PROFILE PHOTO FORM
#******************************************************************************

class ProfilePicturesForm(ModelForm):

    class Meta:
        model = ProfilePictures
        fields = ('picture',)

        widgets = {
            'picture' : FileInput(attrs = {'class':'item-img file center-block', 'required':'true', 'style':'height:0px;width:0px;margin:0px;'}),
        }



#******************************************************************************
# PROFILE FORM ,'country','state','city'
#******************************************************************************

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('fullname','gender' ,'father_name','looking_for_gender', 'mother_name', 'religion', 'caste_creed', 'phone_number',
                  'phone_number_alternative', 'address', 'dob','country','state','city')

        MALE = 'M'
        FEMALE = 'F'

        gender_choices = ((MALE, 'Male'), (FEMALE, 'Female'))

        widgets = {
            'fullname' : TextInput(attrs = {'class':'form-control', 'required':'true'}),
            'father_name' : TextInput(attrs = {'class':'form-control',}),
            'mother_name' : TextInput(attrs = {'class':'form-control',}),
            'gender' : Select(attrs = {'class':'form-control'}, choices = gender_choices),
            'looking_for_gender' : Select(attrs = {'class':'form-control'}, choices = gender_choices),
            'religion' : Select(attrs = {'class':'form-control'}),
            'caste_creed' : Select(attrs = {'class':'form-control'}),
            'phone_number': TextInput(attrs = {'class':'form-control',}),
            'phone_number_alternative' : TextInput(attrs = {'class':'form-control',}),
            'address' : Textarea(attrs = {'class':'form-control', 'rows':'2'}),
            'dob': TextInput(attrs = {'class':'form-control', 'type':'date'}),
            'country' : Select(attrs = {'class':'form-control selectpicker country_select' ,'multiple':'true'}),
            'state' : Select(attrs = {'class':'form-control states_select selectpicker', 'multiple':'true',}),
            'city' : Select(attrs = {'class':'form-control selectpicker city_select', 'multiple':'true'}),
        }

#******************************************************************************
# OTHER PROFILE FORM
#******************************************************************************

class OtherProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ( 'height', 'weight', 'complexion',  'job_details','qualification')

        widgets = {

            'height' :  TextInput(attrs = {'class':'form-control', 'type':'integer'}),
            'weight' : TextInput(attrs = {'class':'form-control', 'type':'integer'}),
            # 'complexion' : Select(attrs = {'class':'form-control'}),
            'qualification' : TextInput(attrs = {'class':'form-control',}),
            'job_details' : Textarea(attrs = {'class':'form-control',}),

        }

#******************************************************************************
# PROFILE SUMMARY FORM
#******************************************************************************

class SummaryForm(ModelForm):

    class Meta:
        model = Profile
        fields = ( 'descriptions', 'biodata')

        widgets = {

            'descriptions' : Textarea(attrs = {'class':'form-control'}),
            'biodata' : FileInput(attrs = {'class':'form-control','accept':'application/pdf,docx',}),

        }
