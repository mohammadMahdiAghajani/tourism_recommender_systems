# سامانه راهنمای گردشگری ایران (Tourism Decision Support System)


## ویژگی‌ها

- اتصال به دیتابیس موجود MariaDB  با جداول: cities, attractions, attraction_images, attraction_profiles, users, interactions و ...
- صفحه اصلی با آمار، پیشنهادهای ساده مبتنی بر تعاملات کاربران مشابه، و محبوب‌ترین‌ها
- فهرست جاذبه‌ها با جستجو و فیلتر
- صفحه جزئیات جاذبه + تصاویر + ویژگی‌های پروفایل + نقشه (لینک OpenStreetMap)
- ثبت تعامل (like / save / visit) برای کاربران
- پروفایل کاربر + تاریخچه تعاملات
- پنل ادمین Django
- رابط کاربری RTL فارسی با Bootstrap 5

## پیش‌نیازها

- Python 3.10+
- MariaDB / MySQL با دیتابیس import‌شده از فایل `db_v1.sql`
- پکیج‌های سیستم برای mysqlclient: `libmariadb-dev` یا `default-libmysqlclient-dev`

## راه‌اندازی سریع

```bash
# 1. ساخت محیط مجازی
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. تنظیم دیتابیس در tourism_guide/settings.py
#    NAME, USER, PASSWORD, HOST, PORT را مطابق محیط خود تغییر دهید.

# 4. ساخت جداول auth/session ادمین (مدل‌های اصلی managed=False هستند)
python manage.py migrate

# 5. (اختیاری) ساخت سوپریوزر
python manage.py createsuperuser

# 6. اجرا
python manage.py runserver
```

سپس باز کنید: http://127.0.0.1:8000/

## ساختار پروژه

```
tourism_guide/     # تنظیمات پروژه
core/              # مدل‌ها، ویوها، URLهای اصلی
accounts/          # ورود / خروج / پروفایل
templates/         # قالب‌های HTML (RTL)
static/            # فایل‌های استاتیک
media/             # رسانه (در صورت نیاز)
requirements.txt
README.md
```
