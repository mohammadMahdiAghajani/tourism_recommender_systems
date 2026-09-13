from django.urls import path
from . import views


"""
این فایل پیکربندی مسیرهای برنامهٔ Django است و مشخص می‌کند هر URL به کدام تابع از `views` متصل شود.
 مسیر خالی (`''`) صفحهٔ اصلی را به `views.home` هدایت می‌کند؛ مسیرهای `attractions/` و `cities/` 
به‌ترتیب فهرست جاذبه‌ها و شهرها را نمایش می‌دهند و الگوی `<int:pk>` شناسهٔ عددی هر جاذبه یا شهر را دریافت
 کرده و به توابع جزئیات (`attraction_detail` و `city_detail`) ارسال می‌کند. مسیرهای `interact/` و 
`record-view/` برای ثبت تعامل کاربر و ثبت مشاهدهٔ جاذبه استفاده می‌شوند. همچنین دو مسیر دارای پیشوند 
`api/` endpointهای JSON هستند که فهرست جاذبه‌ها و جزئیات یک جاذبه را در اختیار کلاینت‌هایی مانند 
JavaScript یا برنامه‌های دیگر قرار می‌دهند. مقدار `name` برای هر مسیر نیز امکان ارجاع به URLها در قالب‌ها و 
کد Django، بدون نوشتن مستقیم آدرس، فراهم می‌کند.
"""

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