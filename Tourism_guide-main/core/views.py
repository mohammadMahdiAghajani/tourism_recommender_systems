from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import (
    Attractions,
    Cities,
    AttractionImages,
    AttractionProfiles,
    Tags,
    Users,
    UserProfiles,
    Interactions,
    Countries
)
import uuid


def get_current_user(request):
    """Simple session-based user using existing Users table."""
    user_id = request.session.get('user_id')

    if user_id:
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            pass

    return None


"""
تابع `home` داده‌های موردنیاز صفحه اصلی را آماده می‌کند؛ ابتدا فهرست شهرها، شش جاذبه 
محبوب بر اساس تعداد تعامل کاربران و شش جاذبه جدید را از پایگاه داده دریافت می‌کند. سپس اگر
 کاربر وارد سیستم شده باشد، با پیدا کردن کاربرانی که با جاذبه‌های مشابه تعامل داشته‌اند،
 حداکثر شش جاذبه جدید را به‌صورت مشارکتی به او پیشنهاد می‌دهد؛ اگر پیشنهاد مناسبی پیدا 
نشود یا کاربر وارد نشده باشد، جاذبه‌های محبوب به‌عنوان گزینه جایگزین نمایش داده می‌شوند.
 در پایان، این اطلاعات به‌همراه تعداد کل شهرها و جاذبه‌ها در قالب `context` به تمپلیت `core/home.html` ارسال می‌شود.
"""
def home(request):
    cities = Cities.objects.all().order_by('name')

    popular = (
        Attractions.objects
        .annotate(interaction_count=Count('interactions'))
        .order_by('-interaction_count', '-id')[:6]
    )

    recent = Attractions.objects.order_by('-created_at')[:6]

    user = get_current_user(request)
    recommendations = []

    if user:
        user_actions = (
            Interactions.objects
            .filter(user=user)
            .values_list('attraction_id', flat=True)
        )

        similar_user_ids = (
            Interactions.objects
            .filter(attraction_id__in=user_actions)
            .exclude(user=user)
            .values_list('user_id', flat=True)
            .distinct()
        )

        recommendations = (
            Attractions.objects
            .filter(interactions__user_id__in=similar_user_ids)
            .exclude(id__in=user_actions)
            .annotate(score=Count('interactions'))
            .order_by('-score')[:6]
        )

        if not recommendations:
            recommendations = popular

    else:
        recommendations = popular

    context = {
        'cities': cities,
        'popular': popular,
        'recent': recent,
        'recommendations': recommendations,
        'current_user': user,
        'total_attractions': Attractions.objects.count(),
        'total_cities': Cities.objects.count(),
    }

    return render(request, 'core/home.html', context)


# =========================================================
# فهرست جاذبه‌ها + فیلترها
# =========================================================

def attraction_list(request):

    qs = (
        Attractions.objects
        .select_related('city', 'city__country')
        .prefetch_related('images', 'profile')
    )

    # -------------------------
    # دریافت فیلترها
    # -------------------------

    city_id = request.GET.get('city')
    q = request.GET.get('q', '').strip()

    # نوع جاذبه
    attr_type = request.GET.get('type')

    # محیط / موقعیت جاذبه
    environment = request.GET.get('environment')

    # -------------------------
    # فیلتر شهر
    # -------------------------

    if city_id:
        qs = qs.filter(city_id=city_id)

    # -------------------------
    # جستجو
    # -------------------------

    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(short_description__icontains=q) |
            Q(full_description__icontains=q)
        )

    # -------------------------
    # نوع جاذبه
    # -------------------------

    allowed_types = [
        'طبیعت',
        'فرهنگی تاریخی',
        'سلامت',
    ]

    if attr_type in allowed_types:
        qs = qs.filter(
            profile__attraction_type=attr_type
        )
    else:
        attr_type = ''

    # -------------------------
    # محیط / موقعیت
    # -------------------------

    allowed_environments = [
        'شهری',
        'روستایی',
        'کوهستانی',
        'جنگلی',
        'کویری',
        'ساحلی',
        'جزیره‌ای',
        'تالابی',
        'رودخانه‌ای',
        'دریاچه‌ای',
    ]

    if environment in allowed_environments:
        qs = qs.filter(
            profile__environment=environment
        )
    else:
        environment = ''

    # -------------------------
    # تعداد لایک‌ها
    # -------------------------

    qs = qs.annotate(
        likes=Count(
            'interactions',
            filter=Q(
                interactions__action_type='like'
            )
        )
    )

    # -------------------------
    # مرتب‌سازی
    # -------------------------

    qs = qs.order_by(
        '-likes',
        'name'
    )

    # -------------------------
    # اطلاعات فیلترها
    # -------------------------

    cities = (
        Cities.objects
        .all()
        .order_by('name')
    )

    types = [
        'طبیعت',
        'فرهنگی تاریخی',
        'سلامت',
    ]

    environments = [
        'شهری',
        'روستایی',
        'کوهستانی',
        'جنگلی',
        'کویری',
        'ساحلی',
        'جزیره‌ای',
        'تالابی',
        'رودخانه‌ای',
        'دریاچه‌ای',
    ]

    # -------------------------
    # Context
    # -------------------------

    context = {
        'attractions': qs,

        'cities': cities,

        # فیلتر نوع جاذبه
        'types': types,

        # فیلتر محیط
        'environments': environments,

        # انتخاب‌های فعلی
        'selected_city': str(city_id) if city_id else '',
        'query': q,
        'selected_type': attr_type,
        'selected_environment': environment,

        # کاربر فعلی
        'current_user': get_current_user(request),
    }

    return render(
        request,
        'core/attraction_list.html',
        context
    )


# =========================================================
# جزئیات جاذبه
# =========================================================
def attraction_detail(request, pk):

    attraction = get_object_or_404(
        Attractions.objects
        .select_related('city', 'city__country')
        .prefetch_related('images', 'profile'),
        pk=pk
    )

    images = attraction.images.order_by('display_order')

    profile = getattr(
        attraction,
        'profile',
        None
    )

    user = get_current_user(request)

    # =========================================
    # تعاملات قبلی کاربر
    # =========================================

    user_actions = set()

    if user:
        user_actions = set(
            Interactions.objects
            .filter(
                user=user,
                attraction=attraction
            )
            .values_list(
                'action_type',
                flat=True
            )
        )

    # =========================================
    # آمار تعاملات
    # =========================================

    stats = (
        Interactions.objects
        .filter(attraction=attraction)
        .values('action_type')
        .annotate(c=Count('id'))
    )

    stats_dict = {
        s['action_type']: s['c']
        for s in stats
    }

    # =========================================
    # جاذبه‌های مرتبط
    # =========================================

    related = (
        Attractions.objects
        .filter(city=attraction.city)
        .exclude(pk=pk)[:4]
    )

    # =========================================
    # Context
    # =========================================

    context = {
        'attraction': attraction,
        'images': images,
        'profile': profile,
        'current_user': user,
        'user_actions': user_actions,
        'stats': stats_dict,
        'related': related,
    }

    return render(
        request,
        'core/attraction_detail.html',
        context
    )


@require_POST
def record_view(request, pk):

    user = get_current_user(request)

    if not user:
        return JsonResponse({
            'ok': False,
            'error': 'user_not_logged_in'
        }, status=401)

    attraction = get_object_or_404(
        Attractions,
        pk=pk
    )

    Interactions.objects.create(
        user=user,
        attraction=attraction,
        action_type='view',
        score=1.00,
        created_at=timezone.now()
    )

    return JsonResponse({
        'ok': True,
        'action': 'view'
    })


"""
این View وظیفهٔ
 ثبت تعاملات کاربر (مانند لایک، ذخیره، اشتراک‌گذاری یا امتیازدهی) با یک جاذبهٔ گردشگری مشخص را از طریق درخواست‌های `POST` 
 بر عهده دارد. ابتدا وضعیت احراز هویت کاربر را بررسی کرده و در صورت ورود، معتبر بودن نوع اکشن دریافتی را ارزیابی می‌کند؛
  سپس بر اساس نوع تعامل—یا مقدار ارسالی سفارشی—امتیاز متناظر با آن (مانند ۳ برای لایک و منفی ۱ برای دیس‌لایک) را تعیین و رکورد جدیدی در 
 جدول `Interactions` ذخیره می‌نماید و در نهایت نتیجه را در قالب پاسخ JSON برمی‌گرداند.
"""
@require_POST
def interact(request, pk):

    user = get_current_user(request)

    if not user:
        return JsonResponse(
            {
                'ok': False,
                'error': 'لطفاً ابتدا وارد شوید'
            },
            status=401
        )

    attraction = get_object_or_404(
        Attractions,
        pk=pk
    )

    action = request.POST.get('action')

    allowed_actions = (
        'like',
        'save',
        # 'visit',
        'share',
        'dislike',
        'rate'
    )

    if action not in allowed_actions:
        return HttpResponseBadRequest(
            'invalid action'
        )

    score_map = {
        'like': 3.0,
        'save': 2.0,
        'visit': 5.0,
        'share': 2.5,
        'dislike': -1.0,
        'rate': 4.0,
    }

    score = float(
        request.POST.get(
            'score',
            score_map.get(action, 1.0)
        )
    )

    Interactions.objects.create(
        user=user,
        attraction=attraction,
        action_type=action,
        score=score,
        created_at=timezone.now()
    )

    return JsonResponse({
        'ok': True,
        'action': action
    })


# =========================================================
# لیست شهرها
# =========================================================

def city_list(request):

    cities = (
        Cities.objects
        .annotate(
            attr_count=Count('attractions')
        )
        .select_related('country')
        .order_by(
            '-attr_count',
            'name'
        )
    )

    return render(
        request,
        'core/city_list.html',
        {
            'cities': cities,
            'current_user': get_current_user(request),
        }
    )


# =========================================================
# جزئیات شهر
# =========================================================

def city_detail(request, pk):

    city = get_object_or_404(
        Cities.objects.select_related('country'),
        pk=pk
    )

    attractions = (
        city.attractions
        .prefetch_related('images')
        .all()
    )

    return render(
        request,
        'core/city_detail.html',
        {
            'city': city,
            'attractions': attractions,
            'current_user': get_current_user(request),
        }
    )


# =========================================================
# ورود
# =========================================================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        try:
            user = Users.objects.get(
                username=username
            )

        except Users.DoesNotExist:

            messages.error(
                request,
                'نام کاربری یا رمز عبور اشتباه است.'
            )

            return render(
                request,
                'accounts/login.html'
            )

        if user.password != password:

            messages.error(
                request,
                'نام کاربری یا رمز عبور اشتباه است.'
            )

            return render(
                request,
                'accounts/login.html'
            )

        request.session['user_id'] = user.id

        messages.success(
            request,
            f'خوش آمدید {user.username}'
        )

        return redirect('home')

    return render(
        request,
        'accounts/login.html'
    )


"""
این View وظیفهٔ مدیریت فرآیند ثبت‌نام کاربران جدید
 را بر عهده دارد؛ در درخواست‌های `GET` فرم ثبت‌نام را نمایش
 می‌دهد و در درخواست‌های `POST` پس از اعتبارسنجی اولیه (شامل پر بودن تمام فیلدها و یکتا بودن نام کاربری و ایمیل در جدول
 سفارشی `Users`)، رکورد کاربر جدید را همراه با یک شناسه یکتای `UUID` ایجاد می‌کند. سپس با ذخیره کردن شناسه کاربر در 
 سشن (`request.session['user_id']`)، او را به‌صورت خودکار 
 وارد سیستم کرده و با ثبت پیام موفقیت، به صفحه اصلی (`home`) هدایت (Redirect) می‌نماید.
"""
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        if not username or not email or not password:

            messages.error(
                request,
                'لطفاً تمام فیلدها را تکمیل کنید.'
            )

            return render(
                request,
                'accounts/register.html'
            )

        if Users.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'این نام کاربری قبلاً ثبت شده است.'
            )

            return render(
                request,
                'accounts/register.html'
            )

        if Users.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'این ایمیل قبلاً ثبت شده است.'
            )

            return render(
                request,
                'accounts/register.html'
            )

        user = Users.objects.create(
            public_id=str(uuid.uuid4()),
            username=username,
            email=email,
            password=password,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        request.session['user_id'] = user.id

        messages.success(
            request,
            'ثبت‌نام با موفقیت انجام شد.'
        )

        return redirect('home')

    return render(
        request,
        'accounts/register.html'
    )


# =========================================================
# خروج
# =========================================================

def logout_view(request):

    request.session.flush()

    messages.info(
        request,
        'با موفقیت خارج شدید.'
    )

    return redirect('home')


# =========================================================
# پروفایل
# =========================================================

def profile_view(request):

    user = get_current_user(request)

    if not user:
        return redirect('login')

    profile = getattr(
        user,
        'profile',
        None
    )

    interactions = (
        Interactions.objects
        .filter(user=user)
        .select_related('attraction')
        .order_by('-created_at')[:50]
    )

    saved = (
        Interactions.objects
        .filter(
            user=user,
            action_type='save'
        )
        .select_related('attraction')
    )

    liked = (
        Interactions.objects
        .filter(
            user=user,
            action_type='like'
        )
        .select_related('attraction')
    )

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': user,
            'profile': profile,
            'interactions': interactions,
            'saved': saved,
            'liked': liked,
            'current_user': user,
        }
    )


# =========================================================
# API جاذبه‌ها
# =========================================================

def api_attractions(request):

    qs = (
        Attractions.objects
        .select_related('city')
        .prefetch_related('images')[:50]
    )

    data = []

    for a in qs:

        data.append({
            'id': a.id,
            'public_id': a.public_id,
            'name': a.name,
            'short_description': a.short_description,
            'city': a.city.name,
            'latitude': float(a.latitude),
            'longitude': float(a.longitude),
            'main_image': a.main_image,
        })

    return JsonResponse({
        'count': len(data),
        'results': data
    })


"""
تابع `api_attraction_detail` یک endpoint برای دریافت اطلاعات یک
 جاذبه براساس شناسهٔ `pk` است. ابتدا با `get_object_or_404` 
 جاذبه را پیدا می‌کند و در صورت نامعتبر بودن شناسه، پاسخ 404 می‌دهد.
 برای بهینه‌سازی دسترسی به پایگاه داده، اطلاعات 
 شهر با `select_related('city')` و 
 روابط تصاویر و پروفایل با `prefetch_related('images', 'profile')` 
 از قبل بارگذاری می‌شوند تا هنگام ساخت پاسخ، کوئری‌های 
 اضافی اجرا نشود. سپس تصاویر مرتبط به فهرستی از دیکشنری‌ها شامل 
 نشانی تصویر، عنوان و ترتیب نمایش تبدیل می‌شوند. اگر جاذبه 
 دارای پروفایل طبقه‌بندی باشد، ویژگی‌هایی مانند نوع جاذبه،
 انگیزه بازدید، محیط، هزینه، فصل مناسب، 
 مدت بازدید و سطح محبوبیت نیز استخراج می‌شوند؛ 
 در غیر این صورت مقدار `profile` برابر `None` خواهد بود. در پایان، مشخصات جاذبه،
 نام شهر، مختصات تبدیل‌شده به `float`، تصاویر
 و پروفایل در قالب `JsonResponse` به کلاینت برگردانده می‌شوند.
تابع `update_preferences` اطلاعات فرم ترجیحات سفر کاربر را دریافت و در `UserProfiles` 
ذخیره می‌کند. ابتدا کاربر جاری از Session بازیابی می‌شود؛ اگر کاربر وارد
 نشده باشد به صفحه ورود و اگر نوع درخواست `POST` نباشد به
 صفحه پروفایل هدایت می‌شود. پس از آن، `get_or_create` پروفایل موجود را بازیابی می‌کند 
 یا برای کاربری که هنوز پروفایل ندارد، یک رکورد جدید 
 می‌سازد. هر فیلد با `request.POST.get` از فرم خوانده می‌شود و مقدار فعلی همان فیلد به‌عنوان مقدار پیش‌فرض
 در نظر گرفته می‌شود؛ بنابراین ارسال‌نشدن یک فیلد باعث حذف مقدار قبلی
 آن نمی‌شود. پس از مقداردهی مشخصاتی مانند ملیت، زبان، بودجه، سبک سفر،
 نوع گروه، سطح فعالیت و تحرک و ترجیحات فصلی، مذهبی و قومی، متد `save` تغییرات را ثبت می‌کند؛ سپس پیام
 موفقیت در سیستم پیام‌رسانی Django قرار می‌گیرد و کاربر به صفحه پروفایل بازگردانده می‌شود.
"""
def api_attraction_detail(request, pk):

    a = get_object_or_404(
        Attractions.objects
        .select_related('city')
        .prefetch_related('images', 'profile'),
        pk=pk
    )

    images = [
        {
            'url': i.image_url,
            'caption': i.caption,
            'order': i.display_order
        }
        for i in a.images.all()
    ]

    profile = None

    if hasattr(a, 'profile') and a.profile:

        p = a.profile

        profile = {
            'type': p.attraction_type,
            'motivation': p.visit_motivation,
            'environment': p.environment,
            'cost': p.cost_band,
            'season': p.best_season,
            'duration': p.visit_duration,
            'popularity': p.popularity_level,
        }

    return JsonResponse({
        'id': a.id,
        'name': a.name,
        'short_description': a.short_description,
        'full_description': a.full_description,
        'city': a.city.name,
        'latitude': float(a.latitude),
        'longitude': float(a.longitude),
        'images': images,
        'profile': profile,
    })

def update_preferences(request):

    user = get_current_user(request)

    if not user:
        return redirect('login')

    if request.method != 'POST':
        return redirect('profile')

    profile, created = UserProfiles.objects.get_or_create(
        user=user
    )

    profile.nationality = request.POST.get(
        'nationality',
        profile.nationality
    )

    profile.language = request.POST.get(
        'language',
        profile.language
    )

    profile.age_band = request.POST.get(
        'age_band',
        profile.age_band
    )

    profile.budget_band = request.POST.get(
        'budget_band',
        profile.budget_band
    )

    profile.travel_style = request.POST.get(
        'travel_style',
        profile.travel_style
    )

    profile.travel_party_type = request.POST.get(
        'travel_party_type',
        profile.travel_party_type
    )

    profile.activity_level = request.POST.get(
        'activity_level',
        profile.activity_level
    )

    profile.mobility_level = request.POST.get(
        'mobility_level',
        profile.mobility_level
    )

    profile.season_preference = request.POST.get(
        'season_preference',
        profile.season_preference
    )

    profile.religious_travel_preference = request.POST.get(
        'religious_travel_preference',
        profile.religious_travel_preference
    )

    profile.ethnic_group = request.POST.get(
        'ethnic_group',
        profile.ethnic_group
    )

    profile.save()

    messages.success(
        request,
        'ترجیحات سفر با موفقیت ذخیره شد.'
    )

    return redirect('profile')