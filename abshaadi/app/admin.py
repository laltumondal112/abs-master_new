from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import * 


#******************************************************************************
#
#****************************************************************************** 

admin.site.site_header = 'abshaadi.com'
admin.site.site_title = "Atut Bandhan Shaadi.com || Hum Bandhan Nahi Sambandh Banate Hai."

#******************************************************************************
#
#****************************************************************************** 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    

#******************************************************************************
#
#******************************************************************************    

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):    
    model = Religion
    list_display = ('religion_name', 'is_active',)
    ordering = ('id',)
    
    
#******************************************************************************
#
#******************************************************************************    

@admin.register(Caste)
class CasteAdmin(admin.ModelAdmin):    
    model = Caste
    list_display = ('religion', 'caste_name', 'is_active',)
    ordering = ('id',)    
    
    
#******************************************************************************
#
#******************************************************************************    

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):    
    model = Package
    list_display = ('package_name', 'value', 'tenure', 'tenure_types', 'description', 'created_on')
    ordering = ('id',)    
      
    
    
    