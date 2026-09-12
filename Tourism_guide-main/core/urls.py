from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # خانه
    # =========================

    path(
        '',
        views.home,
        name='home'
    ),

    # =========================
    # جاذبه ها
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
    # تعامل
    # =========================

    path(
        'attractions/<int:pk>/interact/',
        views.interact,
        name='interact'
    ),

    # =========================
    # ثبت ویو
    # =========================

    path(
        'attractions/<int:pk>/record-view/',
        views.record_view,
        name='record_view'
    ),

    # =========================
    # شهر ها
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