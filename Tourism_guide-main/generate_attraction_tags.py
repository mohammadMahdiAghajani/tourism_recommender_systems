import mariadb


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "yourpass",
    "database": "test",
    "port": 3306,
}


# --------------------------------------------------
# نگاشت attraction_type به tag_id
# --------------------------------------------------

TYPE_TO_TAGS = {
    "طبیعت": [2],                 # طبیعت

    "فرهنگی تاریخی": [1, 4],      # تاریخی + فرهنگی

    "سلامت": [12],                # سلامت
}


# --------------------------------------------------
# نگاشت environment به tag_id
# --------------------------------------------------

ENVIRONMENT_TO_TAGS = {
    "شهری": [11],                 # شهری

    "روستایی": [2],               # طبیعت

    "کوهستانی": [2, 16],          # طبیعت + کوهستان

    "جنگلی": [2],                 # طبیعت

    "کویری": [2, 10],             # طبیعت + کویری

    "ساحلی": [2, 9],              # طبیعت + ساحلی

    "جزیره‌ای": [2, 9],           # طبیعت + ساحلی

    "تالابی": [2],                # طبیعت

    "رودخانه‌ای": [2],            # طبیعت

    "دریاچه‌ای": [2],             # طبیعت
}


# --------------------------------------------------
# اتصال به MariaDB
# --------------------------------------------------

try:
    connection = mariadb.connect(**DB_CONFIG)
    cursor = connection.cursor()

except mariadb.Error as e:
    print("خطا در اتصال به MariaDB:")
    print(e)
    raise SystemExit


# --------------------------------------------------
# گرفتن attraction profile ها
# --------------------------------------------------

cursor.execute(
    """
    SELECT
        attraction_id,
        attraction_type,
        environment
    FROM attraction_profiles
    """
)

profiles = cursor.fetchall()

print(f"{len(profiles)} attraction profiles found.")


created_tags = 0
skipped_profiles = 0


# --------------------------------------------------
# پردازش هر attraction
# --------------------------------------------------

for attraction_id, attraction_type, environment in profiles:

    tag_ids = set()


    # ----------------------------------------------
    # attraction_type
    # ----------------------------------------------

    if attraction_type in TYPE_TO_TAGS:

        tag_ids.update(
            TYPE_TO_TAGS[attraction_type]
        )


    # ----------------------------------------------
    # environment
    # ----------------------------------------------

    if environment in ENVIRONMENT_TO_TAGS:

        tag_ids.update(
            ENVIRONMENT_TO_TAGS[environment]
        )


    # ----------------------------------------------
    # اگر هیچ تگی پیدا نشد
    # ----------------------------------------------

    if not tag_ids:

        skipped_profiles += 1

        continue


    # ----------------------------------------------
    # INSERT attraction_tags
    # ----------------------------------------------

    for tag_id in tag_ids:

        cursor.execute(
            """
            INSERT IGNORE INTO attraction_tags
            (
                attraction_id,
                tag_id
            )
            VALUES (?, ?)
            """,
            (
                attraction_id,
                tag_id,
            )
        )

        if cursor.rowcount > 0:
            created_tags += 1


    print(
        f"Attraction {attraction_id} "
        f"-> tags: {sorted(tag_ids)}"
    )


# --------------------------------------------------
# ذخیره تغییرات
# --------------------------------------------------

connection.commit()


cursor.close()
connection.close()


print()
print("=" * 50)
print("DONE")
print("=" * 50)

print(f"Profiles processed : {len(profiles)}")
print(f"Tags created       : {created_tags}")
print(f"Skipped profiles   : {skipped_profiles}")