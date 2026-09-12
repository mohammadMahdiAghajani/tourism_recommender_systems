# Models mapped to existing MariaDB schema (managed=False)
from django.db import models

# مدل مربوط به کشورها
class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'countries'
        verbose_name = 'کشور'
        verbose_name_plural = 'کشورها'

    def __str__(self):
        return self.name

# مدل مربوط به شهرها که هر شهر به یک کشور مرتبط است
class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, db_column='country_id')
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'cities'
        unique_together = (('country', 'name'),)
        verbose_name = 'شهر'
        verbose_name_plural = 'شهرها'

    def __str__(self):
        return self.name

# اطلاعات پایه هر جاذبه مانند نام، توضیحات، موقعیت جغرافیایی
class Attractions(models.Model):
    id = models.BigAutoField(primary_key=True)
    public_id = models.CharField(unique=True, max_length=36)
    city = models.ForeignKey(Cities, models.DO_NOTHING, db_column='city_id', related_name='attractions')
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attractions'
        verbose_name = 'جاذبه'
        verbose_name_plural = 'جاذبه‌ها'

    def __str__(self):
        return self.name

    @property
    def main_image(self):
        img = self.images.order_by('display_order').first()
        return img.image_url_full if img else None


# مدل مربوط به تصاویر جاذبه‌های گردشگری
class AttractionImages(models.Model):
    id = models.BigAutoField(primary_key=True)

    attraction = models.ForeignKey(
        Attractions,
        models.CASCADE,
        db_column='attraction_id',
        related_name='images'
    )

    image_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'attraction_images'
        verbose_name = 'تصویر جاذبه'
        verbose_name_plural = 'تصاویر جاذبه‌ها'

    @property
    def image_url_full(self):
        from urllib.parse import quote

        city_name = quote(self.attraction.city.name)
        image_path = self.image_url.lstrip('/')

        return f'/media/{city_name}/{image_path}'

    def __str__(self):
        return f'{self.attraction.name} - {self.display_order}'

# مدل مربوط به اطلاعات تکمیلی و ویژگی‌های هر جاذبه
class AttractionProfiles(models.Model):
    attraction = models.OneToOneField(
        Attractions, models.CASCADE, db_column='attraction_id',
        primary_key=True, related_name='profile'
    )
    attraction_type = models.CharField(max_length=50)
    visit_motivation = models.CharField(max_length=50)

    # environment = models.CharField(max_length=50)

    ENVIRONMENT_CHOICES = [
        ('urban', 'شهری'),
        ('rural', 'روستایی'),
        ('mountainous', 'کوهستانی'),
        ('forest', 'جنگلی'),
        ('desert', 'کویری'),
        ('coastal', 'ساحلی'),
        ('island', 'جزیره‌ای'),
        ('wetland', 'تالابی'),
        ('river', 'رودخانه‌ای'),
        ('lake', 'دریاچه‌ای'),
    ]

    environment = models.CharField(
        max_length=50,
        choices=ENVIRONMENT_CHOICES,
    )
    
    cost_band = models.CharField(max_length=50)
    travel_companion = models.CharField(max_length=50)
    required_mobility = models.CharField(max_length=50)
    best_visit_time = models.CharField(max_length=50)
    best_season = models.CharField(max_length=50)
    cltural_experience = models.CharField(max_length=50)  # typo in original schema
    dominant_natural_element = models.CharField(max_length=50)
    tourist_activity = models.CharField(max_length=50)
    access_level = models.CharField(max_length=50)
    visit_duration = models.CharField(max_length=50)
    popularity_level = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'attraction_profiles'
        verbose_name = 'پروفایل جاذبه'
        verbose_name_plural = 'پروفایل جاذبه‌ها'

    def __str__(self):
        return f'Profile of {self.attraction_id}'

# مدل مربوط به برچسب‌های قابل استفاده برای دسته‌بندی جاذبه‌ها و کاربران
class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'tags'
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

    def __str__(self):
        return self.name

# این مدل مشخص می‌کند هر جاذبه چه برچسب‌هایی دارد
class AttractionTags(models.Model):
    attraction = models.ForeignKey(
        Attractions, models.CASCADE, db_column='attraction_id', related_name='attraction_tags'
    )
    tag = models.ForeignKey(Tags, models.CASCADE, db_column='tag_id', related_name='attraction_tags')

    class Meta:
        managed = False
        db_table = 'attraction_tags'
        unique_together = (('attraction', 'tag'),)
        verbose_name = 'برچسب جاذبه'
        verbose_name_plural = 'برچسب‌های جاذبه'

# این مدل برای کاربران است
class Users(models.Model):
    """Custom users table (separate from Django auth.User for existing schema)"""
    id = models.BigAutoField(primary_key=True)
    public_id = models.CharField(unique=True, max_length=36)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    profile_image_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

# اطلاعات تکمیلی مربوط به کاربران
class UserProfiles(models.Model):
    user = models.OneToOneField(
        Users, models.CASCADE, db_column='user_id', primary_key=True, related_name='profile'
    )
    nationality = models.CharField(max_length=20, default='iranian')
    language = models.CharField(max_length=10, default='fa')
    age_band = models.CharField(max_length=20, default='25_34')
    budget_band = models.CharField(max_length=20, default='medium')
    travel_style = models.CharField(max_length=20, default='balanced')
    travel_party_type = models.CharField(max_length=20, default='solo')
    activity_level = models.CharField(max_length=20, default='moderate')
    mobility_level = models.CharField(max_length=20, default='no_limit')
    season_preference = models.CharField(max_length=20, default='all_year')
    religious_travel_preference = models.CharField(max_length=40, default='none')
    ethnic_group = models.CharField(max_length=30, default='prefer_not_to_say')

    class Meta:
        managed = False
        db_table = 'user_profiles'
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def __str__(self):
        return f'Profile of {self.user_id}'

# جدول واسط بین کاربران و برچسب‌ها
class UserTags(models.Model):
    user = models.ForeignKey(Users, models.CASCADE, db_column='user_id', related_name='user_tags')
    tag = models.ForeignKey(Tags, models.CASCADE, db_column='tag_id', related_name='user_tags')
    weight = models.DecimalField(max_digits=5, decimal_places=3, default=1.000)

    class Meta:
        managed = False
        db_table = 'user_tags'
        unique_together = (('user', 'tag'),)
        verbose_name = 'برچسب کاربر'
        verbose_name_plural = 'برچسب‌های کاربر'

# مدل ثبت تعامل کاربران با جاذبه‌های گردشگری
class Interactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, models.CASCADE, db_column='user_id', related_name='interactions')
    attraction = models.ForeignKey(
        Attractions, models.CASCADE, db_column='attraction_id', related_name='interactions'
    )
    action_type = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'interactions'
        verbose_name = 'تعامل'
        verbose_name_plural = 'تعاملات'

    def __str__(self):
        return f'{self.user_id} {self.action_type} {self.attraction_id}'


