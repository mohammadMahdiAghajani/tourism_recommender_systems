import mariadb
import uuid
import random


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    # "password": "yourpass",
    "database": "test",
    "port": 3306,
}


NUMBER_OF_USERS = 50


# -----------------------------------------
# داده‌های مصنوعی
# -----------------------------------------

NATIONALITIES = [
    "iranian",
    "turkish",
    "azerbaijani",
    "kurdish",
    "arab",
    "afghan",
    "pakistani",
    "other",
]

LANGUAGES = [
    "fa",
    "en",
    "tr",
    "ar",
    "az",
    "ku",
    "other",
]

AGE_BANDS = [
    "under_18",
    "18_24",
    "25_34",
    "35_44",
    "45_54",
    "55_plus",
]

BUDGET_BANDS = [
    "low",
    "medium",
    "high",
    "luxury",
]

TRAVEL_STYLES = [
    "budget",
    "balanced",
    "luxury",
    "backpacker",
    "family",
    "romantic",
    "adventure",
    "religious",
    "cultural",
]

TRAVEL_PARTY_TYPES = [
    "solo",
    "couple",
    "family",
    "friends",
    "group",
]

ACTIVITY_LEVELS = [
    "low",
    "moderate",
    "high",
]

MOBILITY_LEVELS = [
    "no_limit",
    "minor_limit",
    "limited",
    "wheelchair_needed",
]

SEASONS = [
    "spring",
    "summer",
    "autumn",
    "winter",
    "all_year",
]

RELIGIOUS_PREFERENCES = [
    "none",
    "halal_friendly",
    "prayer_space_needed",
    "modest_environment_preferred",
    "gender_sensitive",
]

ETHNIC_GROUPS = [
    "persian",
    "kurdish",
    "azerbaijani",
    "lor",
    "arab",
    "baluch",
    "other",
    "prefer_not_to_say",
]

ACTION_TYPES = [
    "view",
    "click",
    "save",
    "like",
    "rate",
    "visit",
    "share",
    "dislike",
]


# -----------------------------------------
# ارتباط Travel Style با Tagها
# -----------------------------------------

STYLE_TAGS = {
    "budget": [6, 2, 18],
    "balanced": [2, 4, 5, 12],
    "luxury": [7, 12, 19],
    "backpacker": [2, 6, 8, 18],
    "family": [5, 14, 11],
    "romantic": [12, 2, 17, 19],
    "adventure": [2, 8, 16, 18],
    "religious": [3, 1, 4],
    "cultural": [1, 4, 13, 15],
}


# -----------------------------------------
# اتصال به دیتابیس
# -----------------------------------------

try:
    connection = mariadb.connect(**DB_CONFIG)
    cursor = connection.cursor()

except mariadb.Error as e:
    print("Database connection error:")
    print(e)
    raise SystemExit


# -----------------------------------------
# گرفتن attraction ها
# -----------------------------------------

cursor.execute("SELECT id FROM attractions")
attraction_ids = [row[0] for row in cursor.fetchall()]

if not attraction_ids:
    print("هیچ attraction ای در دیتابیس پیدا نشد.")
    connection.close()
    raise SystemExit


print(f"{len(attraction_ids)} attractions found.")


# -----------------------------------------
# ساخت کاربران
# -----------------------------------------

created_users = 0
created_profiles = 0
created_tags = 0
created_interactions = 0


for i in range(1, NUMBER_OF_USERS + 1):

    public_id = str(uuid.uuid4())

    username = f"synthetic_user_{i:03d}"

    email = f"synthetic_user_{i:03d}@example.com"

    password = "Synthetic123!"


    # -----------------------------
    # انتخاب پروفایل
    # -----------------------------

    nationality = random.choice(NATIONALITIES)

    language = random.choice(LANGUAGES)

    age_band = random.choice(AGE_BANDS)

    budget_band = random.choice(BUDGET_BANDS)

    travel_style = random.choice(TRAVEL_STYLES)

    travel_party_type = random.choice(TRAVEL_PARTY_TYPES)

    activity_level = random.choice(ACTIVITY_LEVELS)

    mobility_level = random.choice(MOBILITY_LEVELS)

    season_preference = random.choice(SEASONS)

    religious_preference = random.choice(
        RELIGIOUS_PREFERENCES
    )

    ethnic_group = random.choice(
        ETHNIC_GROUPS
    )


    # -----------------------------
    # INSERT users
    # -----------------------------

    cursor.execute(
        """
        INSERT INTO users
        (
            public_id,
            username,
            email,
            password
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            public_id,
            username,
            email,
            password,
        )
    )

    user_id = cursor.lastrowid

    created_users += 1


    # -----------------------------
    # INSERT user_profiles
    # -----------------------------

    cursor.execute(
        """
        INSERT INTO user_profiles
        (
            user_id,
            nationality,
            language,
            age_band,
            budget_band,
            travel_style,
            travel_party_type,
            activity_level,
            mobility_level,
            season_preference,
            religious_travel_preference,
            ethnic_group
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            nationality,
            language,
            age_band,
            budget_band,
            travel_style,
            travel_party_type,
            activity_level,
            mobility_level,
            season_preference,
            religious_preference,
            ethnic_group,
        )
    )

    created_profiles += 1


    # -----------------------------
    # INSERT user_tags
    # -----------------------------

    preferred_tags = STYLE_TAGS[travel_style]

    number_of_tags = random.randint(
        2,
        min(5, len(preferred_tags))
    )

    selected_tags = random.sample(
        preferred_tags,
        number_of_tags
    )

    for tag_id in selected_tags:

        weight = round(
            random.uniform(0.5, 1.0),
            3
        )

        cursor.execute(
            """
            INSERT INTO user_tags
            (
                user_id,
                tag_id,
                weight
            )
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                tag_id,
                weight,
            )
        )

        created_tags += 1


    # -----------------------------
    # INSERT interactions
    # -----------------------------

    number_of_interactions = random.randint(
        30,
        80
    )

    selected_attractions = random.sample(
        attraction_ids,
        min(
            number_of_interactions,
            len(attraction_ids)
        )
    )

    for attraction_id in selected_attractions:

        action_type = random.choices(
            ACTION_TYPES,
            weights=[
                35,  # view
                15,  # click
                10,  # save
                10,  # like
                5,   # rate
                8,   # visit
                5,   # share
                2,   # dislike
            ],
            k=1
        )[0]


        score = None

        if action_type == "rate":
            score = round(
                random.uniform(1, 5),
                2
            )

        elif action_type == "like":
            score = round(
                random.uniform(4, 5),
                2
            )

        elif action_type == "dislike":
            score = round(
                random.uniform(1, 2),
                2
            )


        cursor.execute(
            """
            INSERT INTO interactions
            (
                user_id,
                attraction_id,
                action_type,
                score
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                attraction_id,
                action_type,
                score,
            )
        )

        created_interactions += 1


    print(
        f"User {i:02d}/{NUMBER_OF_USERS} created "
        f"| style={travel_style}"
    )


# -----------------------------------------
# ذخیره تغییرات
# -----------------------------------------

connection.commit()

cursor.close()
connection.close()


print()
print("=" * 50)
print("DONE")
print("=" * 50)

print(f"Users:        {created_users}")
print(f"Profiles:     {created_profiles}")
print(f"User tags:    {created_tags}")
print(f"Interactions: {created_interactions}")