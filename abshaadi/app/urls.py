from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from app.views import home, dashboard, profiles_filters, site_management
from app.views.staff import package_management, user_management
#from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

def staff_member_required(view_func=None, login_url='/page_403/'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator



# Authorization
urlpatterns = [
    path('',home.HomeView.as_view(), name="home"),
    path('page_403/',home.page_403, name="page_403" ),
    path('login/', home.LoginView.as_view(template_name = 'app/base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/base/logout.html'), name = 'logout'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('registration/', home.register_form, name='registration'),
    path('my_redirect_page/', home.my_redirect_page, name='my_redirect_page'),
    path('change_password/', home.change_password, name='change_password'),
]

# Site Managers
urlpatterns += [
    path('staff/religion-management/', never_cache(staff_member_required(site_management.ReligionManagementView.as_view())), name='religion_management'),
    path('load_religions_into_db/', never_cache(staff_member_required(site_management.load_religions_into_db)), name="load_religions_into_db"),
    path('add_religion/', never_cache(staff_member_required(site_management.add_religion)), name="add_religion"),
    path('staff/delete_religion/<int:ins>/', never_cache(staff_member_required(site_management.delete_religion)), name="delete_religion"),
    path('add_caste/', never_cache(staff_member_required(site_management.add_caste)), name="add_caste"),
    path('staff/delete_caste/<int:ins>/', never_cache(staff_member_required(site_management.delete_caste)), name="delete_caste"),
    path('staff/site_managers/load_countries/', never_cache(staff_member_required(site_management.add_countries_to_db)), name="add_countries_to_db"),
]

# Common Urls
urlpatterns += [
    path('get_states_dropdown/', never_cache(login_required(site_management.get_states_dropdown)), name="get_states_dropdown"),
    path('get_cities_dropdown/', never_cache(login_required(site_management.get_cities_dropdown)), name="get_cities_dropdown"),
    path('get_castes_dropdown/', never_cache(login_required(site_management.get_castes_dropdown)), name="get_castes_dropdown"),
]

# Dashboard
urlpatterns += [
    path('staff/dashboard/', never_cache(staff_member_required(dashboard.StaffDashboardView.as_view())), name="staff_dashboard"),
    path('dashboard/', never_cache(login_required(dashboard.UserDashboardView.as_view())), name="dashboard"),
]


# Profile
urlpatterns += [
    path('profile/', never_cache(login_required(profiles_filters.UserProfileView.as_view())), name="user_profile"),
    path('edit_personal_info/', never_cache(login_required(profiles_filters.edit_personal_info)), name="edit_personal_info"),
    path('upload_profile_pic/', never_cache(login_required(profiles_filters.upload_profile_pic)), name="upload_profile_pic"),
    path('upload_picture/', never_cache(login_required(profiles_filters.upload_profile_pic)), name="upload_picture"),
    path('Pay/', never_cache(login_required(profiles_filters.Pay)), name="Pay"),
    path('edit_other_detalis/', never_cache(login_required(profiles_filters.edit_other_detalis)), name="edit_other_detalis"),
    path('edit_summary_detalis/', never_cache(login_required(profiles_filters.edit_summary_detalis)), name="edit_summary_detalis"),
]


# Staff
urlpatterns += [
    path('staff/package_management/view/', never_cache(staff_member_required(package_management.PackageManagementView.as_view())), name="staff_package_management_view"),
    path('staff/user_management/users/view/', never_cache(staff_member_required(user_management.UserManagementView.as_view())), name="user_management_view"),
    path('staff/user_management/users/delete/<int:ins>/', never_cache(staff_member_required(user_management.delete_user)), name="delete_user"),
    path('staff/user_management/staff/view/', never_cache(staff_member_required(user_management.StaffManagementView.as_view())), name="staff_management_view"),
    path('staff/user_management/staff/add/', never_cache(staff_member_required(user_management.add_staff)), name="add_staff"),
]


# Search Pages
urlpatterns += [
    path('search_results/', never_cache(login_required(profiles_filters.MySearchView.as_view())), name="user_search_results"),
    path('save_partner_preferences/', never_cache(login_required(profiles_filters.save_partner_preferences)), name="save_partner_preferences")
]

# Partner Profile Views
urlpatterns += [
    path('connect_msg_save/', never_cache(login_required(profiles_filters.connect_message)), name="connect_msg_save"),
    path('profile_like/<int:to_user_id>/', never_cache(login_required(profiles_filters.profile_like)), name="profile_like"),
    path('partner_profile/<int:user_id>/', never_cache(login_required(profiles_filters.partner_profile_view)), name="partner_profile"),


]

#
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
