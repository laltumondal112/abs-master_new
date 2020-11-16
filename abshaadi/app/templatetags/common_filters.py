from django import template
from django.conf import settings
from django.utils import timezone, safestring

# use Library
register = template.Library()


#*********************************************************************************
#   Tag for loading css files
#*********************************************************************************

@register.simple_tag
def load_css_files(scripts = list()):

    html = []

    for script in scripts:
        html.append('<link rel="stylesheet" href="'+settings.STATIC_URL+script+'"/>')
        
    return safestring.mark_safe(''.join(html))


#*********************************************************************************
#   Tag for loading javascript files
#*********************************************************************************

@register.simple_tag
def load_javascript_files(scripts = list()):

    html = []

    for script in scripts:
        html.append('<script src="'+settings.STATIC_URL+script+'"></script>')
        
    return safestring.mark_safe(''.join(html))
    

#*********************************************************************************
#   PAGINATION HTML
#*********************************************************************************

@register.simple_tag
def pagination_html(page_obj, url = ""):

    dc = page_obj.paginator

    html = []
    html.append('<p class="text-center" style="background-color: #24262d; color: #ffffff; padding:7px 10px;border: 1px solid #3d404c;">')
    html.append('<strong>Page '+ str(page_obj.number)+ ' of '+ str(page_obj.paginator.num_pages)+'</strong>')
    html.append('</p>')
    html.append('<ul class="pagination pull-right" style="margin: 0px;">')

    for i in dc.page_range:
        html.append('<li>'+'<a href="'+url+'?page='+str(i)+'">'+str(i)+'</a></li>')

    html.append('</ul>')

    return safestring.mark_safe(''.join(html))
    

#*********************************************************************************
#   TICK MARK - ICON FOR TRUE AND FALSE
#*********************************************************************************

@register.simple_tag
def tick_mark(value):
    if value:
        html = '<span class="mdi mdi-check-all" style="color:#20cc35; font-size:15px;"></span>'
    else:
        html = '<span class="mdi mdi-close" style="color:#FF0000; font-size:15px;"></span>'

    return safestring.mark_safe(html)