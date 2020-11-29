#
# AUTHOR : LAWRENCE GANDHAR
#
from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.core import serializers

from app.models import *
from app.forms import *
from django.shortcuts import get_object_or_404
from app.forms.registration_forms import RegisterForm, ProfileForm, SummaryForm, OtherProfileForm, ProfilePicturesForm
from django.http import Http404
from django.utils import timezone

from django.utils import safestring

from datetime import date, datetime
import json

from app.helpers import *






import razorpay
from django.views.decorators.csrf import csrf_exempt



    # return render(request, 'index.html')

# @csrf_exempt
# def success(request):
#     return render(request, "success.html")

#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************

class UserProfileView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/users/profile.html'

    data["page_title"] = "My Profile"

    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    # data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js',
    #                     'custom_files/js/common.js', 'custom_files/js/search_filters.js']

    #
    #
    #
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js',
                        'custom_files/js/common.js', 'custom_files/js/search_filters.js']

    def get(self, request):

        try:
            profile_pic = ProfilePictures.objects.get(user=request.user, set_as_profile_pic=True)
            pro_pic = profile_pic.picture

        except:
            pro_pic = ""
            pass

        self.data["pro_pic"] = pro_pic
        self.data["profile"] = Profile.objects.get(user=request.user)
        self.data["gallery"] = ProfilePictures.objects.filter(user=request.user, set_as_profile_pic=False)

        self.data["packages_list"] = Package.objects.filter(is_active = True)

        self.data["search_profile"] = search_forms.MyFiltersForm()
        self.data["profile_picture"] = ProfilePicturesForm()


        self.data["edit_form"] = ProfileForm(instance=self.data["profile"])
        self.data["edit_form1"] = OtherProfileForm(instance=self.data["profile"])
        self.data["edit_form2"] = SummaryForm(instance=self.data["profile"])


        return render(request, self.template_name, self.data)


#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************

class UserProfileEdit(View):
    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'i'


    data["page_title"] = "My Profile"

    data["css_files"] = ['custom_files/css/Chart.min.css', 'custom_files/css/croppie.css']
    # data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js',
                    # 'custom_files/js/common.js', 'custom_files/js/search_filters.js']
    data["js_files"] = ['custom_files/js/Chart.min.js', 'custom_files/js/croppie.js', 'custom_files/js/user_dashboard.js',
                        'custom_files/js/common.js', 'custom_files/js/search_filters.js']

    def get(self,request,id):
        try:
            profile_pic = ProfilePictures.objects.get(user=request.user, set_as_profile_pic=True)
            pro_pic = profile_pic.picture

        except:
            pro_pic = ""
            pass

        self.data["pro_pic"] = pro_pic
        self.data["profile"] = Profile.objects.get(user=request.user)
        self.data["gallery"] = ProfilePictures.objects.filter(user=request.user, set_as_profile_pic=False)

        self.data['profile'] = Profile.objects.get(id=id)

        # print(profile.user)
        return render(request,self.template_name,self.data)


#******************************************************************************
# USER PROFILE VIEW
#******************************************************************************

def upload_profile_pic(request):

    if request.method == 'POST' and request.FILES['picture']:

        files = request.FILES

        ProfilePictures.objects.filter(user = request.user).update(set_as_profile_pic = False)

        profile_pic = ProfilePictures(
                picture = request.FILES['picture'],
                user = request.user,
                set_as_profile_pic = True,
            )

        profile_pic.save()

        return HttpResponse('1')

def upload_picture(request):
    
    if request.method == 'POST' and request.FILES['picture']:

        files = request.FILES

        ProfilePictures.objects.filter(user = request.user).update(set_as_profile_pic = True)

        profile_pic = ProfilePictures(
                picture = request.FILES['picture'],
                user = request.user,
                set_as_profile_pic = False,
            )

        profile_pic.save()

        return HttpResponse('1')

#******************************************************************************
# EDIT PERSONAL INFO
#******************************************************************************

def edit_personal_info(request):
    if request.POST:

        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return redirect('/page_403/')

        pers_info = ProfileForm(request.POST, instance=profile)

        if pers_info.is_valid():
            pers_info.save()
        else:
            print(pers_info.errors)

        return redirect('/profile/')
    return redirect('/page_403/')


#******************************************************************************
# EDIT OTHER DETAILS
#******************************************************************************

def edit_other_detalis(request):
    if request.POST:

        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return redirect('/page_403/')

        pers_info = OtherProfileForm(request.POST, instance=profile)

        if pers_info.is_valid():
            pers_info.save()

        else:
            print(pers_info.errors)

        return redirect('/profile/')
    return redirect('/page_403/')


#******************************************************************************
# EDIT SUMMARY DETAILS
#******************************************************************************

def edit_summary_detalis(request):
    if request.POST:

        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return redirect('/page_403/')

        pers_info = SummaryForm(request.POST, request.FILES, instance=profile)

        if pers_info.is_valid():

            try:
                handle_uploaded_file(request.FILES['biodata'],profile.user_id)
            except:
                pass

            pers_info.save()

        else:
            print(pers_info.errors)

        return redirect('/profile/')
    return redirect('/page_403/')


def handle_uploaded_file(f,user_id):
    with open('app/media/'+str(user_id)+'/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


#******************************************************************************
# SEARCH FILTER SAVE
#******************************************************************************


def save_partner_preferences(request):

    if request.POST:
        form = search_forms.MyFiltersForm(request.POST)

        inp = request.POST.get("inp", None)

        if inp is not None:

            if form.is_valid():
                ins = form.save(commit=False)
                ins.filter_name = inp
                ins.user = request.user
                ins.save()
                return HttpResponse(json.dumps({'code':'1', 'error':''}))
            else:
                return HttpResponse(json.dumps({'code':'0', 'error':safestring.mark_safe(form.errors)}))

        else:
            return HttpResponse(json.dumps({'code':'0', 'error':'Filter Name is required'}))
    return HttpResponse(json.dumps({'code':'0', 'error':'Invalid Operation'}))


#******************************************************************************
# SEARCH FILTERS
#******************************************************************************

class MySearchView(View):

    template_name = 'app/base/base.html'

    data = defaultdict()

    data["included_template"] = 'app/users/search_results.html'

    data["page_title"] = "Partner Profile Search"

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/common.js', 'custom_files/js/search_filters.js']

    #
    #
    #

    def get(self, request):

        self.data["search_profile"] = search_forms.MyFiltersForm()
        return render(request, self.template_name, self.data)

    #
    #
    #

    def post(self, request):

        my_profile = Profile.objects.get(user = request.user)

        self.data["search_profile"] = search_forms.MyFiltersForm()

        looking_for_gender = my_profile.looking_for_gender

        #
        # GET INPUTS
        #

        aged_from = request.POST.get('aged_from', None)
        aged_to = request.POST.get('aged_to', None)
        l_religions = request.POST.getlist('l_religions', None)
        l_cities = request.POST.getlist('l_cities', None)
        l_states = request.POST.getlist('l_states', None)
        l_countries = request.POST.getlist('l_countries', None)
        l_caste = request.POST.getlist('l_caste', None)
        l_qualifications = request.POST.getlist('l_qualifications', None)
        l_jobs = request.POST.getlist('l_jobs', None)
        l_attr = request.POST.getlist('l_attr', None)


        search = Profile.objects.filter(gender = looking_for_gender, user__is_active = True)

        if aged_to is not None:
            search = search.filter(dob__gte = get_birth_full_from_age(aged_to))

        if aged_from is not None:
            search = search.filter(dob__lte = get_birth_full_from_age(aged_from))

        if len(l_religions) > 0:
            rel = Religion.objects.filter(pk__in = l_religions).values_list('id', flat = True)
            search = search.filter(religion_id__in = rel)

        if len(l_caste) > 0:
            castes = Caste.objects.filter(pk__in = l_caste).values_list('id', flat = True)
            search = search.filter(caste_creed_id__in = castes)

        if len(l_countries) > 0:
            countries = Countries.objects.filter(pk__in = l_countries).values_list('id', flat=True)
            search = search.filter(country__in = countries)


        search = search.values('user', 'fullname', 'dob', 'city', 'country',)


        profile_like = ProfileLike.objects.filter(by_user = request.user).values_list('user_id', flat = True)

        search_res = []
        for row in search:

            row['age'] = get_age_from_dob(row['dob'].strftime("%Y-%m-%d"), True)

            if row["user"] not in profile_like:
                row["profile_counter"] = False
            else:
                row["profile_counter"] = True
            search_res.append(row)

        self.data["search_results"] = search_res

        return render(request, self.template_name, self.data)


#******************************************************************************
# CONNECT MEASSAGE
#******************************************************************************

def connect_message(request):

    if request.POST:

        to_user_id = request.POST.get('to_user_id', None)
        from_user_id = request.POST.get('from_user_id', None)
        connect_msg = request.POST.get('connect_msg', None)

        try:
            to_user = CustomUser.objects.get(pk = to_user_id)
        except:
            return HttpResponse(json.dumps({'code':'0', 'error':'Invalid Operation'}))

        try:
            msg_thread = MessageCenter.objects.get(user = request.user, to_user = to_user)
        except:
            msg_thread = MessageCenter(
                user = request.user,
                to_user = to_user,
                liked_on = date.today()
            )

            msg_thread = msg_thread.save()

        msgs = MessageHistory(
            msg = msg_thread,
            message = connect_msg,
        )

        msgs.save()
        return HttpResponse(json.dumps({'code':'1', 'error':''}))


#******************************************************************************
# CONNECT MEASSAGE
#******************************************************************************

def profile_like(request, to_user_id = None):

    if to_user_id is not None:
        try:
            to_user = CustomUser.objects.get(pk = to_user_id)
        except:
            return HttpResponse(json.dumps({'code':'0', 'error':'Invalid Operation'}))

        pro_like = ProfileLike(
            by_user = request.user,
            user = to_user,
            liked = True,
            liked_on = timezone.now(),
        )

        pro_like.save()
        return HttpResponse(json.dumps({'code':'1', 'error':''}))
    return HttpResponse(json.dumps({'code':'0', 'error':'Invalid Operation'}))



#******************************************************************************
# PARTNER PROFILE
#******************************************************************************

def partner_profile_view(request, user_id=None):

    if user_id is not None:

        template_name = 'app/base/base.html'

        data = defaultdict()

        data["included_template"] = 'app/users/partner_profile.html'

        data["page_title"] = "Partner Profile"

        data["css_files"] = []
        data["js_files"] = []

        try:
            user = CustomUser.objects.get(pk = user_id)
        except:
            return redirect('/page_403/')

        data["my_profile"] = Profile.objects.get(user = user)

        print(data["my_profile"].user.last_login)

        try:
            data["my_profile_pic"] = ProfilePictures.objects.get(user = user, set_as_profile_pic = True)
        except:
            data["my_profile_pic"] = None

        return render(request, template_name, data)

    return redirect('/page_403/')



def Pay(request):
    # if request.method == "POST":
    # name = request.POST.get('name')
    amount = 50000

    client = razorpay.Client(
        auth=("rzp_test_fX14iX9W836UYH", "Uqqe2Yg8D0WplUagwBygQwXG"))

    payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})