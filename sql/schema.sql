CREATE DATABASE IF NOT EXISTS munkaDB;

USE munkaDB;

CREATE TABLE IF NOT EXISTS employers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    employers_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employers_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    employers_info_full_name VARCHAR(255) NOT NULL,
    employers_info_address VARCHAR(255),
    employers_info_phone VARCHAR(20),
    employers_info_city VARCHAR(255),
    employers_info_verification BOOLEAN DEFAULT FALSE,
    employers_info_profile_image_path VARCHAR(255),
    employers_info_description TEXT,
    employers_info_website_url VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_seekers (
    job_seeker_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_seeker_tgid BIGINT,
    job_seeker_tgname VARCHAR(32) DEFAULT NULL,
    job_seeker_tgfullname VARCHAR(255) DEFAULT NULL,
    job_seeker_fio VARCHAR(100) DEFAULT NULL,
    job_seeker_age INT DEFAULT NULL,
    job_seeker_employment ENUM('FULL','PARTIAL','ONEDAY','UNCLEAR') DEFAULT NULL,
    job_seeker_location VARCHAR(255) DEFAULT NULL,
    job_seeker_location_text VARCHAR(255) DEFAULT NULL,
    job_seeker_citizenship VARCHAR(255) DEFAULT NULL,
    job_seeker_desired_position VARCHAR(255) DEFAULT NULL,
    job_seeker_employment_type VARCHAR(255) DEFAULT NULL,
    job_seeker_profession VARCHAR(255) DEFAULT NULL,
    job_seeker_desired_salary_level VARCHAR(255) DEFAULT NULL,
    job_seeker_experience JSON,
    job_seeker_additional_info TEXT DEFAULT NULL,
    job_seeker_photo_path VARCHAR(255) DEFAULT NULL,
    job_seeker_language VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS vacancies (
    vacancy_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    vacancy_title VARCHAR(255) NOT NULL,
    vacancy_description TEXT,
    vacancy_employment_type ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'TEMPORARY', 'INTERN') DEFAULT 'FULL_TIME',
    vacancy_location VARCHAR(255),
    vacancy_working_time_modes TEXT DEFAULT NULL,
    vacancy_created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vacancy_updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    vacancy_views INT DEFAULT 0,
    vacancy_photo_path VARCHAR(255) DEFAULT NULL,
    vacancy_is_active BOOLEAN DEFAULT TRUE,
    vacancy_salary DECIMAL(10, 2),
    vacancy_requirements TEXT,
    vacancy_responsibilities TEXT,
    vacancy_benefits TEXT,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_applications (
    application_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    job_seeker_id INT NOT NULL,
    vacancy_id INT NOT NULL,
    status ENUM('PENDING','REJECTED','ACCEPTED') DEFAULT 'PENDING',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_seeker_id) REFERENCES job_seekers(job_seeker_id) ON DELETE CASCADE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE
);

DELIMITER //
CREATE TRIGGER vacancy_updated_date
BEFORE UPDATE ON vacancies
FOR EACH ROW
BEGIN
  IF NEW.vacancy_description != OLD.vacancy_description OR NEW.vacancy_title != OLD.vacancy_title THEN
    SET NEW.vacancy_updated_date = NOW();
  END IF;
END//
DELIMITER ;

CREATE TABLE IF NOT EXISTS employer_balance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
);
DELIMITER $$
CREATE TRIGGER trg_update_employer_balance
AFTER UPDATE ON employer_balance
FOR EACH ROW
BEGIN
    UPDATE employer_balance
    SET last_updated = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_update_vacancy_updated_date
BEFORE UPDATE ON vacancies
FOR EACH ROW
BEGIN
    IF NEW.vacancy_description != OLD.vacancy_description OR NEW.vacancy_title != OLD.vacancy_title THEN
        SET NEW.vacancy_updated_date = NOW();
    END IF;
END$$
DELIMITER ;

ALTER TABLE job_seekers ADD INDEX job_seeker_tgid_index (job_seeker_tgid);
ALTER TABLE job_seekers ADD INDEX job_seeker_desired_position_index (job_seeker_desired_position);

ALTER TABLE employers ADD INDEX employer_tgid_index (employer_tgid);
ALTER TABLE employers ADD INDEX employer_desired_position_index (employer_desired_position);

ALTER TABLE vacancies ADD INDEX employer_id_index (employer_id);
ALTER TABLE vacancies ADD INDEX vacancy_created_date_index (vacancy_created_date);

ALTER TABLE applications ADD INDEX application_vacancy_id_index (vacancy_id);
ALTER TABLE applications ADD INDEX application_job_seeker_id_index (job_seeker_id);

ALTER TABLE viewed_vacancies ADD INDEX viewed_vacancies_job_seeker_id_index (job_seeker_id);
ALTER TABLE viewed_vacancies ADD INDEX viewed_vacancies_vacancy_id_index (vacancy_id);