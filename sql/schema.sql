CREATE DATABASE IF NOT EXISTS munkaDB;

USE munkaDB;

-- Таблица работодателей
CREATE TABLE IF NOT EXISTS employers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    telegram_id VARCHAR(255) DEFAULT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT NULL,
    INDEX idx_email (email),
    INDEX idx_telegram_id (telegram_id)
);

-- Дополнительная информация о работодателях
CREATE TABLE IF NOT EXISTS employers_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    city VARCHAR(255),
    profile_image_path VARCHAR(255),
    description TEXT,
    website_url VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE,
    INDEX idx_full_name (full_name)
);

-- Метрики работодателей
CREATE TABLE IF NOT EXISTS employers_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    login_count INT DEFAULT 0,
    last_login TIMESTAMP DEFAULT NULL,
    pages_visited INT DEFAULT 0,
    time_spent DECIMAL(10, 2) DEFAULT 0.0,
    actions_performed INT DEFAULT 0,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);

-- Соискатели работы через Telegram
CREATE TABLE IF NOT EXISTS job_seekers_tg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tgid BIGINT,
    tgname VARCHAR(32) DEFAULT NULL,
    tgfullname VARCHAR(255) DEFAULT NULL,
    fio VARCHAR(100) DEFAULT NULL,
    age INT DEFAULT NULL,
    employment ENUM('FULL','PARTIAL','ONEDAY','UNCLEAR') DEFAULT NULL,
    location VARCHAR(255) DEFAULT NULL,
    location_text VARCHAR(255) DEFAULT NULL,
    citizenship VARCHAR(255) DEFAULT NULL,
    desired_position VARCHAR(255) DEFAULT NULL,
    employment_type VARCHAR(255) DEFAULT NULL,
    profession VARCHAR(255) DEFAULT NULL,
    desired_salary_level VARCHAR(255) DEFAULT NULL,
    experience JSON,
    additional_info TEXT DEFAULT NULL,
    photo_path VARCHAR(255) DEFAULT NULL,
    language VARCHAR(255) DEFAULT NULL,
    INDEX idx_tgid (tgid),
    INDEX idx_desired_position (desired_position),
    INDEX idx_location (location)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Таблица вакансий
CREATE TABLE IF NOT EXISTS vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    employment_type ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'TEMPORARY', 'INTERN') DEFAULT 'FULL_TIME',
    location VARCHAR(255),
    working_time_modes TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    views INT DEFAULT 0,
    photo_path VARCHAR(255) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    salary DECIMAL(10, 2),
    requirements TEXT,
    responsibilities TEXT,
    benefits TEXT,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE,
    INDEX idx_employer_id (employer_id),
    INDEX idx_created_at (created_at),
    INDEX idx_location (location)
);

-- Таблица заявок на вакансии
CREATE TABLE IF NOT EXISTS job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_seeker_id INT NOT NULL,
    vacancy_id INT NOT NULL,
    status ENUM('PENDING','REJECTED','ACCEPTED') DEFAULT 'PENDING',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_seeker_id) REFERENCES job_seekers_tg(id) ON DELETE CASCADE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(id) ON DELETE CASCADE,
    INDEX idx_vacancy_id (vacancy_id),
    INDEX idx_job_seeker_id (job_seeker_id)
);

-- Изменение делимитера для создания триггера
DELIMITER $$

-- Триггер для обновления времени изменения вакансии
CREATE TRIGGER trg_update_vacancy_updated_date
BEFORE UPDATE ON vacancies
FOR EACH ROW
BEGIN
    IF NEW.description != OLD.description OR NEW.title != OLD.title THEN
        SET NEW.updated_at = NOW();
    END IF;
END$$

DELIMITER ;

-- Таблица балансов работодателей
CREATE TABLE IF NOT EXISTS employer_balance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);

-- Изменение делимитера для создания триггера
DELIMITER $$

-- Триггер для обновления времени изменения баланса работодателей
CREATE TRIGGER trg_update_employer_balance
AFTER UPDATE ON employer_balance
FOR EACH ROW
BEGIN
    UPDATE employer_balance
    SET last_updated = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END$$

DELIMITER ;


-- Добавляем индексы заново
ALTER TABLE job_seekers_tg ADD INDEX idx_tgid (tgid);
ALTER TABLE job_seekers_tg ADD INDEX idx_desired_position (desired_position);
ALTER TABLE job_seekers_tg ADD INDEX idx_location (location);

ALTER TABLE employers ADD INDEX idx_telegram_id (telegram_id);
ALTER TABLE employers_info ADD INDEX idx_full_name (full_name);

ALTER TABLE vacancies ADD INDEX idx_employer_id (employer_id);
ALTER TABLE vacancies ADD INDEX idx_created_at (created_at);
ALTER TABLE vacancies ADD INDEX idx_location (location);

ALTER TABLE job_applications ADD INDEX idx_vacancy_id (vacancy_id);
ALTER TABLE job_applications ADD INDEX idx_job_seeker_id (job_seeker_id);
