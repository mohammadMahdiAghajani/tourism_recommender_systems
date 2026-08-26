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
DROP TABLE IF EXISTS `attraction_images`;
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attraction_images: ~14 rows (approximately)
INSERT INTO `attraction_images` (`id`, `attraction_id`, `image_url`, `caption`, `display_order`) VALUES
	(1, 1, 'https://cdn.example.com/attractions/esfahan/naghshe_jahan_1.jpg', 'نمای میدان نقش جهان', 1),
	(2, 1, 'https://cdn.example.com/attractions/esfahan/naghshe_jahan_2.jpg', 'غروب در میدان نقش جهان', 2),
	(3, 2, 'https://cdn.example.com/attractions/shiraz/persepolis_1.jpg', 'نمای تخت جمشید', 1),
	(4, 2, 'https://cdn.example.com/attractions/shiraz/persepolis_2.jpg', 'ستون‌های تخت جمشید', 2),
	(5, 3, 'https://cdn.example.com/attractions/shiraz/eram_garden_1.jpg', 'باغ ارم', 1),
	(6, 4, 'https://cdn.example.com/attractions/tehran/golestan_palace_1.jpg', 'کاخ گلستان', 1),
	(7, 5, 'https://cdn.example.com/attractions/lorstan/gohar_lake_1.jpg', 'دریاچه گهر', 1),
	(8, 6, 'https://cdn.example.com/attractions/shiraz/nasir_al_mulk_1.jpg', 'مسجد نصیرالملک', 1),
	(9, 7, 'https://cdn.example.com/attractions/mazandaran/badab_surt_1.jpg', 'باداب سورت', 1),
	(10, 8, 'https://cdn.example.com/attractions/masuleh/masuleh_1.jpg', 'ماسوله', 1),
	(11, 9, 'https://cdn.example.com/attractions/tabriz/tabriz_bazaar_1.jpg', 'بازار تبریز', 1),
	(12, 10, 'https://cdn.example.com/attractions/qeshm/stars_valley_1.jpg', 'دره ستارگان', 1),
	(13, 11, 'https://cdn.example.com/attractions/ramsar/hotsprings_1.jpg', 'چشمه آبگرم رامسر', 1),
	(14, 12, 'https://cdn.example.com/attractions/kashan/tabatabaei_house_1.jpg', 'خانه طباطبایی‌ها', 1);

-- Dumping structure for table test.attraction_profiles
DROP TABLE IF EXISTS `attraction_profiles`;
CREATE TABLE IF NOT EXISTS `attraction_profiles` (
  `attraction_id` bigint(20) NOT NULL,
  `attraction_type` enum('مکان تاریخی','موزه','مکان مذهبی','جاذبه طبیعی','ساحل','جنگل','کوهستان','آبشار','کویر','روستا','جاذبه شهری','شهربازی','بازار','باغ','محوطه باستان‌شناسی') NOT NULL,
  `visit_motivation` enum('یادگیری','استراحت','ماجراجویی','عکاسی','زیارت','سرگرمی','خرید','تجربه اجتماعی','طبیعت‌گردی','کشف فرهنگ') NOT NULL,
  `environment` enum('شهری','روستایی','کوهستانی','جنگلی','کویری','ساحلی','جزیره‌ای','تالابی','رودخانه‌ای','دریاچه‌ای') NOT NULL,
  `cost_band` enum('رایگان','دارای بلیت ورودی','اقتصادی','متوسط','سطح بالا','لوکس') NOT NULL,
  `travel_companion` enum('سفر انفرادی','زوج‌ها','خانواده‌ها','گروه دوستان','سالمندان','کودکان','گروه‌های ترکیبی') NOT NULL,
  `required_mobility` enum('مناسب ویلچر','پیاده‌روی کوتاه','گردش پیاده','پیاده‌روی طبیعت','کوه‌پیمایی','صعود فنی') NOT NULL,
  `best_visit_time` enum('طلوع آفتاب','صبح','بعدازظهر','غروب آفتاب','شب','تمام روز','چند روزه') NOT NULL,
  `best_season` enum('بهار','تابستان','پاییز','زمستان','چهار فصل') NOT NULL,
  `cltural_experience` enum('سبک زندگی محلی','معماری سنتی','روایت تاریخی','میراث مذهبی','فرهنگ مدرن','فرهنگ قومی') NOT NULL,
  `dominant_natural_element` enum('آب','جنگل','کوهستان','کویر','دریا','حیات وحش','پوشش گیاهی','پدیده‌های زمین‌شناسی') NOT NULL,
  `tourist_activity` enum('بازدید و گردش','عکاسی','کمپینگ','قایق‌سواری','شنا','پیاده‌روی طبیعت','صخره‌نوردی','خرید','صرف غذا','زیارت') NOT NULL,
  `access_level` enum('حمل‌ونقل عمومی','خودروی شخصی','خودروی آفرود','تله‌کابین','دسترسی با قایق','فقط پیاده') NOT NULL,
  `visit_duration` enum('کمتر از یک ساعت','نیم‌روز','یک روز کامل','سفر آخر هفته','سفر چندروزه') NOT NULL,
  `popularity_level` enum('جاذبه کمتر شناخته‌شده','جاذبه منطقه‌ای','جاذبه ملی','جاذبه بین‌المللی') NOT NULL,
  PRIMARY KEY (`attraction_id`),
  CONSTRAINT `fk_attraction_profiles_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attraction_profiles: ~1 rows (approximately)
INSERT INTO `attraction_profiles` (`attraction_id`, `attraction_type`, `visit_motivation`, `environment`, `cost_band`, `travel_companion`, `required_mobility`, `best_visit_time`, `best_season`, `cltural_experience`, `dominant_natural_element`, `tourist_activity`, `access_level`, `visit_duration`, `popularity_level`) VALUES
	(1, 'مکان تاریخی', 'زیارت', 'کویری', 'متوسط', 'سفر انفرادی', 'مناسب ویلچر', 'بعدازظهر', 'بهار', 'سبک زندگی محلی', 'آب', 'بازدید و گردش', 'حمل‌ونقل عمومی', 'کمتر از یک ساعت', 'جاذبه کمتر شناخته‌شده');

-- Dumping structure for table test.attraction_tags
DROP TABLE IF EXISTS `attraction_tags`;
CREATE TABLE IF NOT EXISTS `attraction_tags` (
  `attraction_id` bigint(20) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`attraction_id`,`tag_id`),
  KEY `fk_attraction_tags_tag` (`tag_id`),
  CONSTRAINT `fk_attraction_tags_attraction` FOREIGN KEY (`attraction_id`) REFERENCES `attractions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_attraction_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attraction_tags: ~0 rows (approximately)

-- Dumping structure for table test.attractions
DROP TABLE IF EXISTS `attractions`;
CREATE TABLE IF NOT EXISTS `attractions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `public_id` char(36) NOT NULL,
  `city_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `short_description` varchar(500) DEFAULT NULL,
  `full_description` longtext DEFAULT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_attractions_public_id` (`public_id`),
  KEY `idx_attractions_city` (`city_id`),
  KEY `idx_attractions_geo` (`latitude`,`longitude`),
  CONSTRAINT `fk_attractions_city` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.attractions: ~12 rows (approximately)
INSERT INTO `attractions` (`id`, `public_id`, `city_id`, `name`, `short_description`, `full_description`, `latitude`, `longitude`, `created_at`, `updated_at`) VALUES
	(1, '9a7b6c5d-1000-4000-9000-000000000001', 2, 'میدان نقش جهان', 'مجموعه‌ای تاریخی در قلب اصفهان', 'میدان نقش جهان از مشهورترین جاذبه‌های تاریخی و فرهنگی ایران است.', 51.6776000, 32.6577000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(2, '9a7b6c5d-1000-4000-9000-000000000002', 3, 'تخت جمشید', 'پایتخت باستانی هخامنشیان', 'تخت جمشید نماد شکوه تاریخ ایران باستان و از مهم‌ترین مقاصد گردشگری فرهنگی است.', 52.8917000, 29.9334000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(3, '9a7b6c5d-1000-4000-9000-000000000003', 3, 'باغ ارم', 'باغ ایرانی و فضای آرامش‌بخش', 'باغ ارم از باغ‌های زیبای شیراز با فضای سبز و معماری چشمگیر است.', 52.5405000, 29.6240000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(4, '9a7b6c5d-1000-4000-9000-000000000004', 1, 'کاخ گلستان', 'کاخ تاریخی در مرکز تهران', 'کاخ گلستان یکی از مهم‌ترین آثار تاریخی و ثبت جهانی در تهران است.', 51.4200000, 35.6790000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(5, '9a7b6c5d-1000-4000-9000-000000000005', 1, 'دریاچه گهر', 'جاذبه طبیعی کوهستانی', 'دریاچه گهر مقصدی محبوب برای طبیعت‌گردی و پیاده‌روی است.', 49.3000000, 33.0000000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(6, '9a7b6c5d-1000-4000-9000-000000000006', 3, 'مسجد نصیرالملک', 'مسجد معروف به مسجد صورتی', 'این مسجد به خاطر شیشه‌های رنگی و نورپردازی صبحگاهی مشهور است.', 52.5254000, 29.6219000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(7, '9a7b6c5d-1000-4000-9000-000000000007', 8, 'باداب سورت', 'چشمه‌های پلکانی طبیعی', 'باداب سورت از پدیده‌های طبیعی کم‌نظیر و مناسب علاقه‌مندان به طبیعت است.', 53.2800000, 36.3450000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(8, '9a7b6c5d-1000-4000-9000-000000000008', 7, 'روستای ماسوله', 'روستای پلکانی و تاریخی', 'ماسوله با معماری پلکانی و هوای مطبوع، مقصدی فرهنگی و طبیعی است.', 48.9910000, 37.1530000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(9, '9a7b6c5d-1000-4000-9000-000000000009', 6, 'بازار تبریز', 'بازار سرپوشیده تاریخی', 'بازار تبریز از بزرگ‌ترین بازارهای سرپوشیده جهان و مناسب خرید و بازدید فرهنگی است.', 46.2890000, 38.0876000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(10, '9a7b6c5d-1000-4000-9000-000000000010', 9, 'جزیره قشم - دره ستارگان', 'جاذبه طبیعی و زمین‌شناختی', 'دره ستارگان از معروف‌ترین جاذبه‌های طبیعی قشم است.', 55.9520000, 26.9490000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(11, '9a7b6c5d-1000-4000-9000-000000000011', 10, 'چشمه‌های آبگرم رامسر', 'مقصد آرامش و سلامت', 'رامسر برای سفرهای خانوادگی و آرامش‌بخش بسیار مناسب است.', 50.6660000, 36.9030000, '2026-05-01 09:00:00', '2026-05-01 09:00:00'),
	(12, '9a7b6c5d-1000-4000-9000-000000000012', 8, 'خانه طباطبایی‌ها', 'خانه تاریخی با معماری اصیل', 'خانه طباطبایی‌ها نمونه‌ای برجسته از معماری خانه‌های تاریخی کاشان است.', 51.4646000, 33.9865000, '2026-05-01 09:00:00', '2026-05-01 09:00:00');

-- Dumping structure for table test.cities
DROP TABLE IF EXISTS `cities`;
CREATE TABLE IF NOT EXISTS `cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_city_country_name` (`country_id`,`name`),
  KEY `idx_city_country` (`country_id`),
  CONSTRAINT `fk_city_country` FOREIGN KEY (`country_id`) REFERENCES `countries` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.cities: ~10 rows (approximately)
INSERT INTO `cities` (`id`, `country_id`, `name`) VALUES
	(1, 1, 'تهران'),
	(2, 1, 'اصفهان'),
	(3, 1, 'شیراز'),
	(4, 1, 'یزد'),
	(5, 1, 'مشهد'),
	(6, 1, 'تبریز'),
	(7, 1, 'رشت'),
	(8, 1, 'کاشان'),
	(9, 1, 'قشم'),
	(10, 1, 'رامسر');

-- Dumping structure for table test.countries
DROP TABLE IF EXISTS `countries`;
CREATE TABLE IF NOT EXISTS `countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_country_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.countries: ~5 rows (approximately)
INSERT INTO `countries` (`id`, `name`) VALUES
	(1, 'ایران'),
	(2, 'ترکیه'),
	(3, 'امارات متحده عربی'),
	(4, 'عراق'),
	(5, 'آذربایجان');

-- Dumping structure for table test.interactions
DROP TABLE IF EXISTS `interactions`;
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.interactions: ~27 rows (approximately)
INSERT INTO `interactions` (`id`, `user_id`, `attraction_id`, `action_type`, `score`, `created_at`) VALUES
	(1, 1, 1, 'view', 1.00, '2026-05-01 10:12:00'),
	(2, 1, 1, 'save', 2.00, '2026-05-01 10:13:00'),
	(3, 1, 4, 'view', 1.00, '2026-05-02 11:00:00'),
	(4, 1, 4, 'like', 3.00, '2026-05-02 11:01:00'),
	(5, 1, 12, 'rate', 4.00, '2026-05-03 09:40:00'),
	(6, 2, 5, 'view', 1.00, '2026-05-01 08:30:00'),
	(7, 2, 5, 'save', 2.00, '2026-05-01 08:31:00'),
	(8, 2, 7, 'view', 1.00, '2026-05-02 14:20:00'),
	(9, 2, 7, 'like', 3.00, '2026-05-02 14:21:00'),
	(10, 2, 10, 'visit', 5.00, '2026-05-05 16:00:00'),
	(11, 3, 3, 'view', 1.00, '2026-05-01 12:10:00'),
	(12, 3, 3, 'like', 3.00, '2026-05-01 12:11:00'),
	(13, 3, 11, 'view', 1.00, '2026-05-02 18:05:00'),
	(14, 3, 11, 'save', 2.00, '2026-05-02 18:06:00'),
	(15, 4, 6, 'view', 1.00, '2026-05-03 07:45:00'),
	(16, 4, 6, 'like', 3.00, '2026-05-03 07:46:00'),
	(17, 4, 1, 'view', 1.00, '2026-05-04 09:15:00'),
	(18, 4, 1, 'save', 2.00, '2026-05-04 09:16:00'),
	(19, 5, 9, 'view', 1.00, '2026-05-04 10:10:00'),
	(20, 5, 9, 'save', 2.00, '2026-05-04 10:11:00'),
	(21, 5, 8, 'view', 1.00, '2026-05-04 20:30:00'),
	(22, 5, 8, 'like', 3.00, '2026-05-04 20:31:00'),
	(23, 6, 2, 'view', 1.00, '2026-05-05 13:00:00'),
	(24, 6, 2, 'visit', 5.00, '2026-05-06 11:00:00'),
	(25, 6, 6, 'view', 1.00, '2026-05-06 12:00:00'),
	(26, 6, 6, 'like', 3.00, '2026-05-06 12:01:00'),
	(27, 6, 4, 'save', 2.00, '2026-05-06 12:02:00');

-- Dumping structure for table test.tags
DROP TABLE IF EXISTS `tags`;
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
DROP TABLE IF EXISTS `user_profiles`;
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

-- Dumping data for table test.user_profiles: ~6 rows (approximately)
INSERT INTO `user_profiles` (`user_id`, `nationality`, `language`, `age_band`, `budget_band`, `travel_style`, `travel_party_type`, `activity_level`, `mobility_level`, `season_preference`, `religious_travel_preference`, `ethnic_group`) VALUES
	(1, 'iranian', 'fa', '25_34', 'medium', 'cultural', 'couple', 'moderate', 'no_limit', 'spring', 'halal_friendly', 'prefer_not_to_say'),
	(2, 'iranian', 'fa', '18_24', 'low', 'backpacker', 'solo', 'high', 'minor_limit', 'all_year', 'none', 'persian'),
	(3, 'turkish', 'tr', '35_44', 'high', 'family', 'family', 'low', 'no_limit', 'summer', 'prayer_space_needed', 'prefer_not_to_say'),
	(4, 'iranian', 'fa', '25_34', 'medium', 'romantic', 'couple', 'low', 'no_limit', 'autumn', 'none', 'kurdish'),
	(5, 'afghan', 'fa', '18_24', 'low', 'budget', 'friends', 'high', 'no_limit', 'spring', 'halal_friendly', 'other'),
	(6, 'iranian', 'fa', '45_54', 'high', 'religious', 'group', 'low', 'limited', 'all_year', 'gender_sensitive', 'prefer_not_to_say');

-- Dumping structure for table test.user_tags
DROP TABLE IF EXISTS `user_tags`;
CREATE TABLE IF NOT EXISTS `user_tags` (
  `user_id` bigint(20) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `weight` decimal(5,3) NOT NULL DEFAULT 1.000,
  PRIMARY KEY (`user_id`,`tag_id`),
  KEY `fk_user_tags_tag` (`tag_id`),
  CONSTRAINT `fk_user_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_tags_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.user_tags: ~0 rows (approximately)

-- Dumping structure for table test.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `public_id` char(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profile_image_url` varchar(500) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_public_id` (`public_id`),
  UNIQUE KEY `uk_users_username` (`username`),
  UNIQUE KEY `uk_users_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table test.users: ~6 rows (approximately)
INSERT INTO `users` (`id`, `public_id`, `username`, `email`, `profile_image_url`, `created_at`, `updated_at`) VALUES
	(1, '8f2d7d5c-0000-4000-9000-000000000001', 'mh_rahimi', 'mh.rahimi@example.com', 'https://cdn.example.com/profiles/mh_rahimi.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00'),
	(2, '8f2d7d5c-0000-4000-9000-000000000002', 'sara_n', 'sara.n@example.com', 'https://cdn.example.com/profiles/sara_n.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00'),
	(3, '8f2d7d5c-0000-4000-9000-000000000003', 'ali_k', 'ali.k@example.com', 'https://cdn.example.com/profiles/ali_k.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00'),
	(4, '8f2d7d5c-0000-4000-9000-000000000004', 'leila_m', 'leila.m@example.com', 'https://cdn.example.com/profiles/leila_m.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00'),
	(5, '8f2d7d5c-0000-4000-9000-000000000005', 'reza_p', 'reza.p@example.com', 'https://cdn.example.com/profiles/reza_p.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00'),
	(6, '8f2d7d5c-0000-4000-9000-000000000006', 'neda_h', 'neda.h@example.com', 'https://cdn.example.com/profiles/neda_h.jpg', '2026-05-01 08:00:00', '2026-05-01 08:00:00');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
