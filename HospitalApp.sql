CREATE DATABASE HospitalApp;

USE HospitalApp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('doctor', 'patient') NOT NULL
);

CREATE TABLE medical_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    appointment_details TEXT,
    appointment_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);