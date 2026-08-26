from django.urls import path

from core import views as core_views


urlpatterns = [

    path(
        'login/',
        core_views.login_view,
        name='login'
    ),

    path(
        'register/',
        core_views.register_view,
        name='register'
    ),

    path(
        'logout/',
        core_views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        core_views.profile_view,
        name='profile'
    ),

    path(
        'profile/preferences/',
        core_views.update_preferences,
        name='update_preferences'
    ),

]