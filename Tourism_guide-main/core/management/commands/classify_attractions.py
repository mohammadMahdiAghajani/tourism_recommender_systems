from django.core.management.base import BaseCommand
from django.db import connection

from core.models import Attractions


class BaseClassifier:

    HEALTH_KEYWORDS = [
        'آبگرم',
        'آب گرم',
        'چشمه آب گرم',
        'چشمه آبگرم',
        'آب معدنی',
        'آب‌معدنی',
        'آب‌درمانی',
        'آب درمانی',
        'درمانی',
        'شفابخش',
        'خواص درمانی',
        'سلامت',
    ]

    NATURE_KEYWORDS = [
        'آبشار',
        'دریاچه',
        'تالاب',
        'رودخانه',
        'جنگل',
        'کوه',
        'قله',
        'دره',
        'دشت',
        'چشمه',
        'ساحل',
        'کویر',
        'غار',
        'جزیره',
        'پارک ملی',
        'منطقه حفاظت‌شده',
        'منطقه حفاظت شده',
        'طبیعت',
        'صخره',
        'یخچال',
        'گردشگاه',
    ]

    CULTURAL_KEYWORDS = [
        'مسجد',
        'کلیسا',
        'موزه',
        'بازار',
        'حمام',
        'قلعه',
        'کاخ',
        'عمارت',
        'آرامگاه',
        'مقبره',
        'بقعه',
        'امامزاده',
        'معبد',
        'پل تاریخی',
        'پل ',
        'کاروانسرا',
        'خانه تاریخی',
        'باغ تاریخی',
        'آتشکده',
        'کتیبه',
        'محوطه باستانی',
        'باستانی',
        'رصدخانه',
        'برج',
        'مناره',
        'مدرسه تاریخی',
        'خانه ',
        'آسیاب آبی',
        'آب انبار',
        'آب‌انبار',
        'یخدان',
        'گورستان',
        'خانقاه',
        'حسینیه',
        'مدرسه ',
        'باغ ',
    ]

    EXCLUDED_KEYWORDS = [
        'مرکز خرید',
        'مجتمع تجاری',
        'مجتمع تفریحی',
        'کافه',
        'رستوران',
        'فلافل',
        'سمبوسه',
        'غذا',
        'کشتی تفریحی',
        'کشتی ',
        'پارک کودک',
        'پارک علمی',
        'پارک مینیاتوری',
        'سرزمین موج',
        'پیست اسکی',
        'اسکله تفریحی',
        'فروشگاه',
        'خرید',
    ]

    @classmethod
    def classify(cls, attraction):

        text = " ".join([
            attraction.name or "",
            attraction.short_description or "",
            attraction.full_description or "",
        ]).lower()

        # مواردی که اصلاً جاذبه قابل دسته‌بندی نیستند
        if any(
            keyword.lower() in text
            for keyword in cls.EXCLUDED_KEYWORDS
        ):
            return None

        # سلامت
        if any(
            keyword.lower() in text
            for keyword in cls.HEALTH_KEYWORDS
        ):
            return 'سلامت'

        # فرهنگی تاریخی
        if any(
            keyword.lower() in text
            for keyword in cls.CULTURAL_KEYWORDS
        ):
            return 'فرهنگی تاریخی'

        # طبیعت
        if any(
            keyword.lower() in text
            for keyword in cls.NATURE_KEYWORDS
        ):
            return 'طبیعت'

        return None


class Command(BaseCommand):

    help = 'دسته‌بندی جاذبه‌ها'

    def handle(self, *args, **options):

        attractions = Attractions.objects.all().order_by('id')

        counts = {
            'طبیعت': 0,
            'فرهنگی تاریخی': 0,
            'سلامت': 0,
            'بدون دسته‌بندی': 0,
        }

        with connection.cursor() as cursor:

            for attraction in attractions:

                category = BaseClassifier.classify(attraction)

                # -------------------------
                # بدون دسته‌بندی
                # -------------------------
                if category is None:

                    cursor.execute(
                        """
                        DELETE FROM attraction_profiles
                        WHERE attraction_id = %s
                        """,
                        [attraction.id]
                    )

                    counts['بدون دسته‌بندی'] += 1
                    continue

                # -------------------------
                # بررسی اینکه پروفایل وجود دارد یا نه
                # -------------------------
                cursor.execute(
                    """
                    SELECT attraction_id
                    FROM attraction_profiles
                    WHERE attraction_id = %s
                    """,
                    [attraction.id]
                )

                exists = cursor.fetchone()

                # -------------------------
                # اگر وجود دارد فقط نوع را تغییر بده
                # -------------------------
                if exists:

                    cursor.execute(
                        """
                        UPDATE attraction_profiles
                        SET attraction_type = %s
                        WHERE attraction_id = %s
                        """,
                        [category, attraction.id]
                    )

                # -------------------------
                # اگر وجود ندارد، فقط
                # attraction_id و attraction_type
                # را وارد کن
                # -------------------------
                else:

                    cursor.execute(
                        """
                        INSERT INTO attraction_profiles
                        (
                            attraction_id,
                            attraction_type
                        )
                        VALUES (%s, %s)
                        """,
                        [attraction.id, category]
                    )

                counts[category] += 1

        # -------------------------
        # نتیجه
        # -------------------------

        self.stdout.write(
            '\n========== نتیجه دسته‌بندی ==========\n'
        )

        for category, count in counts.items():
            self.stdout.write(
                f'{category}: {count}'
            )

        self.stdout.write(
            f'\nمجموع: {sum(counts.values())}\n'
        )

        self.stdout.write(
            '\nدسته‌بندی با موفقیت انجام شد.\n'
        )