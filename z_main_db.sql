-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               12.2.2-MariaDB - MariaDB Server
-- Server OS:                    Win64
-- HeidiSQL Version:             12.14.0.7165
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for test
CREATE DATABASE IF NOT EXISTS `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `test`;

-- Dumping structure for table test.attraction_images
CREATE TABLE IF NOT EXISTS `attraction_images` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `attraction_id` bigint(20) NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `caption` varchar(255) DEFAULT NULL,
  `display_order` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_attraction_images_attraction` (`attraction_id`),
  KEY `idx_attraction_images_order` (`attraction_id`,`display_order`),
  CONSTRAINT `fk_attraction_images_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=908 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='در این بخش تصاویر جاذبه های گردشگری موجود است\r\nکه شامل Id - url - caption ,... میشود';

-- Dumping data for table test.attraction_images: ~907 rows (approximately)
INSERT INTO `attraction_images` (`id`, `attraction_id`, `image_url`, `caption`, `display_order`) VALUES
	(1, 1, 'images/image_2.jpg', NULL, 0),
	(905, 905, 'images/image_43.jpg', NULL, 0);

-- Dumping structure for table test.attraction_profiles
CREATE TABLE IF NOT EXISTS `attraction_profiles` (
  `attraction_id` bigint(20) NOT NULL,
  `attraction_type` enum('طبیعت','فرهنگی تاریخی','سلامت') DEFAULT NULL,
  `visit_motivation` enum('یادگیری','استراحت','ماجراجویی','عکاسی','زیارت','سرگرمی','خرید','تجربه اجتماعی','طبیعت‌گردی','کشف فرهنگ') DEFAULT NULL,
  `environment` enum('شهری','روستایی','کوهستانی','جنگلی','کویری','ساحلی','جزیره‌ای','تالابی','رودخانه‌ای','دریاچه‌ای') DEFAULT NULL,
  `cost_band` enum('رایگان','دارای بلیت ورودی','اقتصادی','متوسط','سطح بالا','لوکس') DEFAULT NULL,
  `travel_companion` enum('سفر انفرادی','زوج‌ها','خانواده‌ها','گروه دوستان','سالمندان','کودکان','گروه‌های ترکیبی') DEFAULT NULL,
  `required_mobility` enum('مناسب ویلچر','پیاده‌روی کوتاه','گردش پیاده','پیاده‌روی طبیعت','کوه‌پیمایی','صعود فنی') DEFAULT NULL,
  `best_visit_time` enum('طلوع آفتاب','صبح','بعدازظهر','غروب آفتاب','شب','تمام روز','چند روزه') DEFAULT NULL,
  `best_season` enum('بهار','تابستان','پاییز','زمستان','چهار فصل') DEFAULT NULL,
  `cltural_experience` enum('سبک زندگی محلی','معماری سنتی','روایت تاریخی','میراث مذهبی','فرهنگ مدرن','فرهنگ قومی') DEFAULT NULL,
  `dominant_natural_element` enum('آب','جنگل','کوهستان','کویر','دریا','حیات وحش','پوشش گیاهی','پدیده‌های زمین‌شناسی') DEFAULT NULL,
  `tourist_activity` enum('بازدید و گردش','عکاسی','کمپینگ','قایق‌سواری','شنا','پیاده‌روی طبیعت','صخره‌نوردی','خرید','صرف غذا','زیارت') DEFAULT NULL,
  `access_level` enum('حمل‌ونقل عمومی','خودروی شخصی','خودروی آفرود','تله‌کابین','دسترسی با قایق','فقط پیاده') DEFAULT NULL,
  `visit_duration` enum('کمتر از یک ساعت','نیم‌روز','یک روز کامل','سفر آخر هفته','سفر چندروزه') DEFAULT NULL,
  `popularity_level` enum('جاذبه کمتر شناخته‌شده','جاذبه منطقه‌ای','جاذبه ملی','جاذبه بین‌المللی') DEFAULT NULL,
  PRIMARY KEY (`attraction_id`),
  CONSTRAINT `fk_attraction_profiles_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attraction_profiles: ~700 rows (approximately)
INSERT INTO `attraction_profiles` (`attraction_id`, `attraction_type`, `visit_motivation`, `environment`, `cost_band`, `travel_companion`, `required_mobility`, `best_visit_time`, `best_season`, `cltural_experience`, `dominant_natural_element`, `tourist_activity`, `access_level`, `visit_duration`, `popularity_level`) VALUES
	(1, 'فرهنگی تاریخی', 'زیارت', 'روستایی', 'متوسط', 'سفر انفرادی', 'مناسب ویلچر', 'بعدازظهر', 'بهار', 'سبک زندگی محلی', 'آب', 'بازدید و گردش', 'حمل‌ونقل عمومی', 'کمتر از یک ساعت', 'جاذبه کمتر شناخته‌شده'),
	(2, 'فرهنگی تاریخی', NULL, 'شهری', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(903, 'طبیعت', NULL, 'کویری', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- Dumping structure for table test.attraction_profiles_backup
CREATE TABLE IF NOT EXISTS `attraction_profiles_backup` (
  `attraction_id` bigint(20) NOT NULL,
  `attraction_type` enum('مکان تاریخی','موزه','مکان مذهبی','جاذبه طبیعی','ساحل','جنگل','کوهستان','آبشار','کویر','روستا','جاذبه شهری','شهربازی','بازار','باغ','محوطه باستان‌شناسی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `visit_motivation` enum('یادگیری','استراحت','ماجراجویی','عکاسی','زیارت','سرگرمی','خرید','تجربه اجتماعی','طبیعت‌گردی','کشف فرهنگ') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `environment` enum('شهری','روستایی','کوهستانی','جنگلی','کویری','ساحلی','جزیره‌ای','تالابی','رودخانه‌ای','دریاچه‌ای') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cost_band` enum('رایگان','دارای بلیت ورودی','اقتصادی','متوسط','سطح بالا','لوکس') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `travel_companion` enum('سفر انفرادی','زوج‌ها','خانواده‌ها','گروه دوستان','سالمندان','کودکان','گروه‌های ترکیبی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `required_mobility` enum('مناسب ویلچر','پیاده‌روی کوتاه','گردش پیاده','پیاده‌روی طبیعت','کوه‌پیمایی','صعود فنی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `best_visit_time` enum('طلوع آفتاب','صبح','بعدازظهر','غروب آفتاب','شب','تمام روز','چند روزه') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `best_season` enum('بهار','تابستان','پاییز','زمستان','چهار فصل') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `cltural_experience` enum('سبک زندگی محلی','معماری سنتی','روایت تاریخی','میراث مذهبی','فرهنگ مدرن','فرهنگ قومی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dominant_natural_element` enum('آب','جنگل','کوهستان','کویر','دریا','حیات وحش','پوشش گیاهی','پدیده‌های زمین‌شناسی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tourist_activity` enum('بازدید و گردش','عکاسی','کمپینگ','قایق‌سواری','شنا','پیاده‌روی طبیعت','صخره‌نوردی','خرید','صرف غذا','زیارت') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `access_level` enum('حمل‌ونقل عمومی','خودروی شخصی','خودروی آفرود','تله‌کابین','دسترسی با قایق','فقط پیاده') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `visit_duration` enum('کمتر از یک ساعت','نیم‌روز','یک روز کامل','سفر آخر هفته','سفر چندروزه') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `popularity_level` enum('جاذبه کمتر شناخته‌شده','جاذبه منطقه‌ای','جاذبه ملی','جاذبه بین‌المللی') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.attraction_profiles_backup: ~1 rows (approximately)
INSERT INTO `attraction_profiles_backup` (`attraction_id`, `attraction_type`, `visit_motivation`, `environment`, `cost_band`, `travel_companion`, `required_mobility`, `best_visit_time`, `best_season`, `cltural_experience`, `dominant_natural_element`, `tourist_activity`, `access_level`, `visit_duration`, `popularity_level`) VALUES
	(1, 'مکان تاریخی', 'زیارت', 'کویری', 'متوسط', 'سفر انفرادی', 'مناسب ویلچر', 'بعدازظهر', 'بهار', 'سبک زندگی محلی', 'آب', 'بازدید و گردش', 'حمل‌ونقل عمومی', 'کمتر از یک ساعت', 'جاذبه کمتر شناخته‌شده');

-- Dumping structure for table test.attraction_tags
CREATE TABLE IF NOT EXISTS `attraction_tags` (
  `attraction_id` bigint(20) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`attraction_id`,`tag_id`),
  KEY `fk_attraction_tags_tag` (`tag_id`),
  CONSTRAINT `fk_attraction_tags_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_attraction_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attraction_tags: ~1,853 rows (approximately)
INSERT INTO `attraction_tags` (`attraction_id`, `tag_id`) VALUES
	(1, 1),
	(903, 10);

-- Dumping structure for table test.attractions
CREATE TABLE IF NOT EXISTS `attractions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `public_id` char(36) NOT NULL,
  `city_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `short_description` varchar(500) DEFAULT NULL,
  `full_description` longtext DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_attractions_public_id` (`public_id`),
  KEY `idx_attractions_city` (`city_id`),
  KEY `idx_attractions_geo` (`latitude`,`longitude`),
  CONSTRAINT `fk_attractions_city` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=908 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attractions: ~823 rows (approximately)
INSERT INTO `attractions` (`id`, `public_id`, `city_id`, `name`, `short_description`, `full_description`, `latitude`, `longitude`, `created_at`, `updated_at`) VALUES
	(1, '1a2751a3-72fe-4ca4-8fef-4b4c151ae240', 25, 'کلیسای سنت استپانوس', 'کلیسای سنت استپانوس (استپانوس مقدس) یکی از مشهورترین، مهم‌ترین و البته زیباترین کلیساهای تاریخی ارامنه در ایران است. این کلیسا در نزدیکی مرز ایران و آذربایجان و در بخش جنوبی رودخانه ارس قرار دارد. فاصله کلیسای سنت استپانوس از شهرستان جلفا در حدود ۲۰ کیلومتر است و برای رسیدن به آن باید به سمت شمال غربی جلفا حرکت کنید و از جاده مرزی بگذرید. سنت استپانوس در منطقه‌ای کوهستانی-دره‌ای قرار گرفته است. به دلیل موقعیت خاص این کلیسا و معماری منحصر به‌فردش یکی از معروف‌ترین جاهای دیدنی آذربایجان شرقی است.\n', 'کلیسای سنت استپانوس (استپانوس مقدس) یکی از مشهورترین، مهم‌ترین و البته زیباترین کلیساهای تاریخی ارامنه در ایران است. این کلیسا در نزدیکی مرز ایران و آذربایجان و در بخش جنوبی رودخانه ارس قرار دارد. فاصله کلیسای سنت استپانوس از شهرستان جلفا در حدود ۲۰ کیلومتر است و برای رسیدن به آن باید به سمت شمال غربی جلفا حرکت کنید و از جاده مرزی بگذرید. سنت استپانوس در منطقه‌ای کوهستانی-دره‌ای قرار گرفته است. به دلیل موقعیت خاص این کلیسا و معماری منحصر به‌فردش یکی از معروف‌ترین جاهای دیدنی آذربایجان شرقی است.\nاین کلیسا چندین سال است که در دست مرمت و از میراث جهانی ثبت شده در یونسکو است. در رابطه با ساخت اولیه کلیسا چندین روایت مختلف وجود دارد و دقیقا مشخص نیست اما طبق آخرین تحقیقات، ساخت کلیسا به دوره صفوی برمی‌گردد. سنت استپانوس یکی از یاران اصلی حضرت عیسی (ع) و اولین شهید در راه ابلاغ دین مسیحیت بوده است که این کلیسا با یاد این قدیس بزرگ، چنین نام گرفته است.\nبخوانید از: بهترین جاهای دیدنی تبریز در تمام فصول + آدرس و معرفی کامل', 38.9791610, 45.4733979, '2026-07-30 20:12:02', '2026-07-30 20:17:04'),
	(904, '6c0d5449-7d95-4b5e-920c-2cafaedaa598', 4, 'کافه دپسا | از بهترین کافه‌های روی بام', 'یکی از بهترین و جذاب‌ترین کافه‌های روی بام یزد همین کافه دپسا  است که در قلب بافت تاریخی یزد و نزدیکی هتل‌ سرای درویش قرار دارد. اگر دوست دارید فضایی سنتی رو در شهر یزد مشاهده کنید، می‌توانید به این کافه زیبا و البته عالی بروید. شب‌ها این کافه زیر آسمان پرستاره دیدنی‌تر می شود. منوی این کافه پر است از نوشیدنی‌های سنتی و انواع کیک‌ها و دسرهای جذاب. روزهای آخر هفته در این کافه صبحانه‌های محلی یزد سرو می‌شود.\nآدرس کافه دپسا روی نقشه گوگل', 'یکی از بهترین و جذاب‌ترین کافه‌های روی بام یزد همین کافه دپسا  است که در قلب بافت تاریخی یزد و نزدیکی هتل‌ سرای درویش قرار دارد. اگر دوست دارید فضایی سنتی رو در شهر یزد مشاهده کنید، می‌توانید به این کافه زیبا و البته عالی بروید. شب‌ها این کافه زیر آسمان پرستاره دیدنی‌تر می شود. منوی این کافه پر است از نوشیدنی‌های سنتی و انواع کیک‌ها و دسرهای جذاب. روزهای آخر هفته در این کافه صبحانه‌های محلی یزد سرو می‌شود.\nآدرس کافه دپسا روی نقشه گوگل', 32.0406164, 54.6657189, '2026-07-30 20:12:02', '2026-07-30 22:27:41'),
	(905, 'dbf4a307-4e61-4da5-9279-f9dca86b67b6', 4, 'کافه ایرانی قدیمی | با چشم اندازی زیبا', 'یکی از کافه‌هایی که می‌توانید پس از گشت و گذار در جاهای دیدنی یزد در بافت تاریخی، مراجعه کنید، کافه ایرانی قدیمی است. این کافه با چشم‌انداز گنبد بام خانه‌های اطراف منظره ای زیبا را برای شما ترسیم می‌کند.\nآدرس کافه ایرانی قدیمی روی نقشه گوگل', 'یکی از کافه‌هایی که می‌توانید پس از گشت و گذار در جاهای دیدنی یزد در بافت تاریخی، مراجعه کنید، کافه ایرانی قدیمی است. این کافه با چشم‌انداز گنبد بام خانه‌های اطراف منظره ای زیبا را برای شما ترسیم می‌کند.\nآدرس کافه ایرانی قدیمی روی نقشه گوگل', 32.0406164, 54.6657189, '2026-07-30 20:12:02', '2026-07-30 22:27:50');

-- Dumping structure for table test.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_group: ~0 rows (approximately)

-- Dumping structure for table test.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table test.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_permission: ~24 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session');

-- Dumping structure for table test.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_user: ~0 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$1500000$hMgOxYZ1NIelPfuLHLYsJM$nPHyPIshrU60JSSrbdGPsXXOkmN1Ro07O1KPinOcMV4=', '2026-08-19 06:25:12.379259', 1, 'iliya', '', '', '', 1, 1, '2026-08-12 17:03:30.239973');

-- Dumping structure for table test.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table test.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table test.cities
CREATE TABLE IF NOT EXISTS `cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_country_name` (`country_id`,`name`),
  KEY `idx_city_country` (`country_id`),
  CONSTRAINT `fk_city_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.cities: ~25 rows (approximately)
INSERT INTO `cities` (`id`, `country_id`, `name`) VALUES
	(1, 1, 'تهران'),
	(2, 1, 'اصفهان'),
	(3, 1, 'شیراز'),
	(4, 1, 'یزد'),
	(5, 1, 'مشهد'),
	(6, 1, 'تبریز'),
	(7, 1, 'رشت'),
	(8, 1, 'لرستان'),
	(9, 1, 'همدان'),
	(10, 1, 'رامسر'),
	(11, 1, 'کیش'),
	(12, 1, 'البرز'),
	(13, 1, 'ایلام'),
	(14, 1, 'اهواز'),
	(15, 1, 'بندرعباس'),
	(16, 1, 'بوشهر'),
	(17, 1, 'سنندج'),
	(18, 1, 'کرمانشاه'),
	(19, 1, 'کرمان'),
	(20, 1, 'اردبیل'),
	(21, 1, 'بندرانزلی'),
	(22, 1, 'چالوس'),
	(23, 1, 'سمنان'),
	(24, 1, 'سیستان و بلوچستان'),
	(25, 1, 'آذربایجان شرقی'),
	(26, 1, 'آذربایجان غربی');

-- Dumping structure for table test.countries
CREATE TABLE IF NOT EXISTS `countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_country_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.countries: ~1 rows (approximately)
INSERT INTO `countries` (`id`, `name`) VALUES
	(1, 'ایران');

-- Dumping structure for table test.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.django_admin_log: ~113 rows (approximately)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2026-08-18 21:53:30.490717', '116', '8 view 300', 3, '', 10, 1),
	(113, '2026-08-18 21:59:05.266462', '117', '8 view 214', 3, '', 10, 1);

-- Dumping structure for table test.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.django_content_type: ~10 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'core', 'users'),
	(8, 'core', 'attractions'),
	(9, 'core', 'attractionprofiles'),
	(10, 'core', 'interactions'),
	(11, 'core', 'userprofiles');

-- Dumping structure for table test.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.django_migrations: ~18 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-08-12 13:39:05.408826'),
	(2, 'auth', '0001_initial', '2026-08-12 13:39:05.568585'),
	(3, 'admin', '0001_initial', '2026-08-12 13:39:05.613243'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-08-12 13:39:05.619130'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-12 13:39:05.624719'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2026-08-12 13:39:05.660272'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2026-08-12 13:39:05.683319'),
	(8, 'auth', '0003_alter_user_email_max_length', '2026-08-12 13:39:05.694797'),
	(9, 'auth', '0004_alter_user_username_opts', '2026-08-12 13:39:05.700884'),
	(10, 'auth', '0005_alter_user_last_login_null', '2026-08-12 13:39:05.722090'),
	(11, 'auth', '0006_require_contenttypes_0002', '2026-08-12 13:39:05.723579'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2026-08-12 13:39:05.730959'),
	(13, 'auth', '0008_alter_user_username_max_length', '2026-08-12 13:39:05.745249'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2026-08-12 13:39:05.763015'),
	(15, 'auth', '0010_alter_group_name_max_length', '2026-08-12 13:39:05.776799'),
	(16, 'auth', '0011_update_proxy_permissions', '2026-08-12 13:39:05.784594'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2026-08-12 13:39:05.798472'),
	(18, 'sessions', '0001_initial', '2026-08-12 13:39:05.814727');

-- Dumping structure for table test.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table test.django_session: ~3 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('3dpf3qtm8gplmlgh6etn70hlmtrlmp2d', 'eyJ1c2VyX2lkIjo4fQ:1wupFM:l-Mk112sH1-DvjSFV04sb07LdNyTgmkYR_OrlYO-guM', '2026-08-28 10:34:44.715325'),
	('69f5tsxln83m09ca55vx4in1gg6bz1og', '.eJxVjkEOgjAQRe_SNWmG8gvo0j1naNqZ0aIGEgor490NCTG6_e_l5b9MiNuaw1Z0CaOYs6lN9bulyA-ddiD3ON1my_O0LmOyu2IPWuwwiz4vh_sXyLHkPdsLKwBKUCbPRHRtBBAkOGK0dVRPogJuQArqfEcn17CLQuhbU5nvx_79AYjpOxA:1wuCR7:KSw4k_0wUsoWkCFsyMnKIgjT77qa2btvKD_-tUeGaBc', '2026-08-26 17:08:17.843776'),
	('y6ctxgg3euafu6p3z61j00f5sbezrcpx', 'eyJ1c2VyX2lkIjozN30:1wwcqF:CIhvsOtI92kTrebBBHNp5RXFCoWPCgovPHfEe0vRHYI', '2026-09-02 09:44:15.884610');

-- Dumping structure for view test.full_database_view
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `full_database_view` (
	`attraction_id` BIGINT(20) NOT NULL,
	`public_id` CHAR(36) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`attraction_name` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`short_description` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`full_description` LONGTEXT NULL COLLATE 'utf8mb4_unicode_ci',
	`latitude` DECIMAL(10,7) NULL,
	`longitude` DECIMAL(10,7) NULL,
	`city_id` INT(11) NULL,
	`city_name` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`country_id` INT(11) NULL,
	`country_name` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`image_id` BIGINT(20) NULL,
	`image_url` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`tag_id` INT(11) NULL,
	`tag_name` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci'
);

-- Dumping structure for view test.full_tourism_report
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `full_tourism_report` (
	`id` BIGINT(20) NOT NULL,
	`attraction_name` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`city_name` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`country_name` VARCHAR(1) NULL COLLATE 'utf8mb4_unicode_ci',
	`latitude` DECIMAL(10,7) NULL,
	`longitude` DECIMAL(10,7) NULL
);

-- Dumping structure for table test.interactions
CREATE TABLE IF NOT EXISTS `interactions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `attraction_id` bigint(20) NOT NULL,
  `action_type` enum('view','click','save','like','rate','visit','share','dislike') NOT NULL,
  `score` decimal(6,2) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_interactions_user` (`user_id`),
  KEY `idx_interactions_attraction` (`attraction_id`),
  KEY `idx_interactions_action` (`action_type`),
  KEY `idx_interactions_created` (`created_at`),
  KEY `idx_interactions_user_attraction` (`user_id`,`attraction_id`),
  CONSTRAINT `fk_interactions_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_interactions_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5566 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.interactions: ~5,436 rows (approximately)
INSERT INTO `interactions` (`id`, `user_id`, `attraction_id`, `action_type`, `score`, `created_at`) VALUES
	(130, 10, 726, 'view', NULL, '2026-08-19 09:51:54'),
	(5565, 109, 44, 'view', NULL, '2026-08-19 13:11:41');

-- Dumping structure for table test.tags
CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_tag_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.tags: ~19 rows (approximately)
INSERT INTO `tags` (`id`, `name`) VALUES
	(1, 'تاریخی'),
	(2, 'طبیعت'),
	(3, 'مذهبی'),
	(4, 'فرهنگی'),
	(5, 'خانوادگی'),
	(6, 'کم‌هزینه'),
	(7, 'لوکس'),
	(8, 'ماجراجویی'),
	(9, 'ساحلی'),
	(10, 'کویری'),
	(11, 'شهری'),
	(12, 'آرامش'),
	(13, 'موزه'),
	(14, 'باغ'),
	(15, 'بازار'),
	(16, 'کوهستان'),
	(17, 'عکاسی'),
	(18, 'پیاده‌روی'),
	(19, 'خوراکی');

-- Dumping structure for table test.user_profiles
CREATE TABLE IF NOT EXISTS `user_profiles` (
  `user_id` bigint(20) NOT NULL,
  `nationality` enum('iranian','turkish','azerbaijani','kurdish','arab','afghan','pakistani','other') NOT NULL DEFAULT 'iranian',
  `language` enum('fa','en','tr','ar','az','ku','other') NOT NULL DEFAULT 'fa',
  `age_band` enum('under_18','18_24','25_34','35_44','45_54','55_plus') NOT NULL DEFAULT '25_34',
  `budget_band` enum('low','medium','high','luxury') NOT NULL DEFAULT 'medium',
  `travel_style` enum('budget','balanced','luxury','backpacker','family','romantic','adventure','religious','cultural') NOT NULL DEFAULT 'balanced',
  `travel_party_type` enum('solo','couple','family','friends','group') NOT NULL DEFAULT 'solo',
  `activity_level` enum('low','moderate','high') NOT NULL DEFAULT 'moderate',
  `mobility_level` enum('no_limit','minor_limit','limited','wheelchair_needed') NOT NULL DEFAULT 'no_limit',
  `season_preference` enum('spring','summer','autumn','winter','all_year') NOT NULL DEFAULT 'all_year',
  `religious_travel_preference` enum('none','halal_friendly','prayer_space_needed','modest_environment_preferred','gender_sensitive') NOT NULL DEFAULT 'none',
  `ethnic_group` enum('persian','kurdish','azerbaijani','lor','arab','baluch','other','prefer_not_to_say') NOT NULL DEFAULT 'prefer_not_to_say',
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_user_profiles_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.user_profiles: ~102 rows (approximately)
INSERT INTO `user_profiles` (`user_id`, `nationality`, `language`, `age_band`, `budget_band`, `travel_style`, `travel_party_type`, `activity_level`, `mobility_level`, `season_preference`, `religious_travel_preference`, `ethnic_group`) VALUES
	(7, 'iranian', 'fa', 'under_18', 'low', 'budget', 'solo', 'low', 'no_limit', 'spring', 'none', 'persian'),
	(108, 'iranian', 'tr', '45_54', 'luxury', 'adventure', 'couple', 'low', 'minor_limit', 'autumn', 'modest_environment_preferred', 'arab'),
	(109, 'kurdish', 'ku', '25_34', 'high', 'backpacker', 'couple', 'moderate', 'wheelchair_needed', 'summer', 'none', 'lor');

-- Dumping structure for table test.user_tags
CREATE TABLE IF NOT EXISTS `user_tags` (
  `user_id` bigint(20) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `weight` decimal(5,3) NOT NULL DEFAULT 1.000,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `fk_user_tags_tag` (`tag_id`),
  CONSTRAINT `fk_user_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_tags_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.user_tags: ~271 rows (approximately)
INSERT INTO `user_tags` (`user_id`, `tag_id`, `weight`) VALUES
	(10, 2, 0.774),
	(109, 18, 0.819);

-- Dumping structure for table test.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `public_id` char(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profile_image_url` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `password` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_public_id` (`public_id`),
  UNIQUE KEY `uk_users_username` (`username`),
  UNIQUE KEY `uk_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.users: ~103 rows (approximately)
INSERT INTO `users` (`id`, `public_id`, `username`, `email`, `profile_image_url`, `created_at`, `updated_at`, `password`) VALUES
	(7, '5310bed0-2381-46ed-96ee-8bed98e30977', 'rafieyan', 'rafeliya1297@gmail.com', NULL, '2026-08-12 14:32:14', '2026-08-19 10:06:48', '12345'),
	(108, '796d7516-61af-4b7a-a35a-67594503eaf7', 'synthetic_user_099', 'synthetic_user_099@example.com', NULL, '2026-08-19 13:11:41', '2026-08-19 13:11:41', 'Synthetic123!'),
	(109, 'f2291191-0634-4de2-a74a-83146a70c11c', 'synthetic_user_100', 'synthetic_user_100@example.com', NULL, '2026-08-19 13:11:41', '2026-08-19 13:11:41', 'Synthetic123!');

-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `full_database_view`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `full_database_view` AS SELECT
    a.id AS attraction_id,
    a.public_id,
    a.name AS attraction_name,
    a.short_description,
    a.full_description,
    a.latitude,
    a.longitude,
    c.id AS city_id,
    c.name AS city_name,
    co.id AS country_id,
    co.name AS country_name,
    ai.id AS image_id,
    ai.image_url,
    t.id AS tag_id,
    t.name AS tag_name
FROM attractions a
LEFT JOIN cities c ON a.city_id = c.id
LEFT JOIN countries co ON c.country_id = co.id
LEFT JOIN attraction_images ai ON ai.attraction_id = a.id
LEFT JOIN attraction_tags at ON at.attraction_id = a.id
LEFT JOIN tags t ON at.tag_id = t.id 
;

-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `full_tourism_report`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `full_tourism_report` AS SELECT 
    a.id,
    a.name AS attraction_name,
    c.name AS city_name,
    co.name AS country_name,
    a.latitude,
    a.longitude
FROM attractions a
LEFT JOIN cities c ON a.city_id = c.id
LEFT JOIN countries co ON c.country_id = co.id 
;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
