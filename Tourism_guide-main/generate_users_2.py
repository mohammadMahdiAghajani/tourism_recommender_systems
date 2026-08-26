import mariadb
import uuid
import random


# ==================================================
# Database Configuration
# ==================================================

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "yourpass",
    "database": "test",
    "port": 3306,
}


# ==================================================
# Settings
# ==================================================

NUMBER_OF_USERS = 50

START_NUMBER = 51


# ==================================================
# Possible values
# ==================================================

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


# ==================================================
# Travel Style → Tags
#
# tag IDs:
#
# 1  تاریخی
# 2  طبیعت
# 3  مذهبی
# 4  فرهنگی
# 5  خانوادگی
# 6  کم‌هزینه
# 7  لوکس
# 8  ماجراجویی
# 9  ساحلی
# 10 کویری
# 11 شهری
# 12 آرامش
# 13 موزه
# 14 باغ
# 15 بازار
# 16 کوهستان
# 17 عکاسی
# 18 پیاده‌روی
# 19 خوراکی
# ==================================================

STYLE_TAGS = {

    "budget": [
        6,
        2,
        18,
    ],

    "balanced": [
        2,
        4,
        5,
        12,
    ],

    "luxury": [
        7,
        12,
        19,
    ],

    "backpacker": [
        2,
        6,
        8,
        18,
    ],

    "family": [
        5,
        14,
        11,
    ],

    "romantic": [
        12,
        2,
        17,
        19,
    ],

    "adventure": [
        2,
        8,
        16,
        18,
    ],

    "religious": [
        3,
        1,
        4,
    ],

    "cultural": [
        1,
        4,
        13,
        15,
    ],
}


# ==================================================
# Connect to MariaDB
# ==================================================

try:

    connection = mariadb.connect(
        **DB_CONFIG
    )

    cursor = connection.cursor()

    print("Connected to MariaDB successfully.")

except mariadb.Error as e:

    print("Database connection error:")
    print(e)

    raise SystemExit


# ==================================================
# Get existing usernames
# ==================================================

cursor.execute(
    """
    SELECT username
    FROM users
    WHERE username LIKE 'synthetic_user_%'
    """
)

existing_usernames = {
    row[0]
    for row in cursor.fetchall()
}


print(
    f"Existing synthetic users: "
    f"{len(existing_usernames)}"
)


# ==================================================
# Get attractions
# ==================================================

cursor.execute(
    """
    SELECT id
    FROM attractions
    ORDER BY id
    """
)

attraction_ids = [
    row[0]
    for row in cursor.fetchall()
]


if not attraction_ids:

    print("No attractions found.")

    cursor.close()
    connection.close()

    raise SystemExit


print(
    f"Attractions found: "
    f"{len(attraction_ids)}"
)


# ==================================================
# Counters
# ==================================================

created_users = 0
created_profiles = 0
created_tags = 0
created_interactions = 0


# ==================================================
# Create 50 NEW users
# ==================================================

for i in range(NUMBER_OF_USERS):

    user_number = START_NUMBER + i

    username = (
        f"synthetic_user_{user_number:03d}"
    )

    email = (
        f"synthetic_user_{user_number:03d}"
        "@example.com"
    )


    # ------------------------------------------------
    # Safety check
    # ------------------------------------------------

    if username in existing_usernames:

        print(
            f"SKIPPED: {username} already exists."
        )

        continue


    # ------------------------------------------------
    # Generate UUID
    # ------------------------------------------------

    public_id = str(
        uuid.uuid4()
    )


    # ------------------------------------------------
    # Password
    # ------------------------------------------------

    password = "Synthetic123!"


    # ------------------------------------------------
    # Generate profile
    # ------------------------------------------------

    nationality = random.choice(
        NATIONALITIES
    )

    language = random.choice(
        LANGUAGES
    )

    age_band = random.choice(
        AGE_BANDS
    )

    budget_band = random.choice(
        BUDGET_BANDS
    )

    travel_style = random.choice(
        TRAVEL_STYLES
    )

    travel_party_type = random.choice(
        TRAVEL_PARTY_TYPES
    )

    activity_level = random.choice(
        ACTIVITY_LEVELS
    )

    mobility_level = random.choice(
        MOBILITY_LEVELS
    )

    season_preference = random.choice(
        SEASONS
    )

    religious_preference = random.choice(
        RELIGIOUS_PREFERENCES
    )

    ethnic_group = random.choice(
        ETHNIC_GROUPS
    )


    # ==================================================
    # Insert users
    # ==================================================

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


    # ==================================================
    # Insert user_profiles
    # ==================================================

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
        (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?
        )
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


    # ==================================================
    # Insert user_tags
    # ==================================================

    possible_tags = STYLE_TAGS[
        travel_style
    ]


    number_of_tags = random.randint(
        2,
        min(4, len(possible_tags))
    )


    selected_tags = random.sample(
        possible_tags,
        number_of_tags
    )


    for tag_id in selected_tags:

        weight = round(
            random.uniform(
                0.500,
                1.000
            ),
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


    # ==================================================
    # Generate interactions
    # ==================================================

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
                35,   # view
                15,   # click
                10,   # save
                10,   # like
                5,    # rate
                8,    # visit
                5,    # share
                2,    # dislike
            ],

            k=1

        )[0]


        # --------------------------------------------
        # Score
        # --------------------------------------------

        score = None


        if action_type == "rate":

            score = round(
                random.uniform(
                    1,
                    5
                ),
                2
            )


        elif action_type == "like":

            score = round(
                random.uniform(
                    4,
                    5
                ),
                2
            )


        elif action_type == "dislike":

            score = round(
                random.uniform(
                    1,
                    2
                ),
                2
            )


        # --------------------------------------------
        # Insert interaction
        # --------------------------------------------

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
        f"[{i + 1:02d}/50] "
        f"{username} "
        f"| style={travel_style} "
        f"| tags={number_of_tags} "
        f"| interactions={number_of_interactions}"
    )


# ==================================================
# Commit
# ==================================================

connection.commit()


# ==================================================
# Close
# ==================================================

cursor.close()
connection.close()


# ==================================================
# Final report
# ==================================================

print()
print("=" * 60)
print("50 NEW SYNTHETIC USERS CREATED")
print("=" * 60)

print(
    f"New users:        {created_users}"
)

print(
    f"New profiles:     {created_profiles}"
)

print(
    f"New user tags:    {created_tags}"
)

print(
    f"New interactions: {created_interactions}"
)

print("=" * 60)