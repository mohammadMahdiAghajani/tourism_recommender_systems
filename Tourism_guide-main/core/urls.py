from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # Home
    # =========================

    path(
        '',
        views.home,
        name='home'
    ),

    # =========================
    # Attractions
    # =========================

    path(
        'attractions/',
        views.attraction_list,
        name='attraction_list'
    ),

    path(
        'attractions/<int:pk>/',
        views.attraction_detail,
        name='attraction_detail'
    ),

    # =========================
    # Interaction
    # =========================

    path(
        'attractions/<int:pk>/interact/',
        views.interact,
        name='interact'
    ),

    # =========================
    # Record View
    # =========================

    path(
        'attractions/<int:pk>/record-view/',
        views.record_view,
        name='record_view'
    ),

    # =========================
    # Cities
    # =========================

    path(
        'cities/',
        views.city_list,
        name='city_list'
    ),

    path(
        'cities/<int:pk>/',
        views.city_detail,
        name='city_detail'
    ),

    # =========================
    # API
    # =========================

    path(
        'api/attractions/',
        views.api_attractions,
        name='api_attractions'
    ),

    path(
        'api/attractions/<int:pk>/',
        views.api_attraction_detail,
        name='api_attraction_detail'
    ),
]