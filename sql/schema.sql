CREATE DATABASE IF NOT EXISTS munkaDB;

USE munkaDB;

CREATE TABLE IF NOT EXISTS employers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    salt VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS employers_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employers_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    FOREIGN KEY (employers_id) REFERENCES employers(id)
);
