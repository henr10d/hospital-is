CREATE DATABASE HospitalApp;

USE HospitalApp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('doctor', 'patient') NOT NULL,
);

CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    image_path VARCHAR(255),
    FOREIGN KEY (doctor_id) REFERENCES users(id)
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    doctor_id INT,
    image_path VARCHAR(255),
    age INT,
    FOREIGN KEY (patient_id) REFERENCES users(id)
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE medical_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    details TEXT,
    appointment_time DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_details TEXT,
    appointment_time DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);