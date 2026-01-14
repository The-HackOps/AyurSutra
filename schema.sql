-- This file can be used when Database is needed
CREATE DATABASE IF NOT EXISTS ayursutra_db;

USE ayursutra_db;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('patient', 'practitioner') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Patients (
    user_id INT PRIMARY KEY,
    phone VARCHAR(20),
    dob DATE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Practitioners (
    user_id INT PRIMARY KEY,
    specialty VARCHAR(100),
    title VARCHAR(50) COMMENT 'e.g., Dr., Vaidya',
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Therapies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    duration_minutes INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    practitioner_id INT NOT NULL,
    therapy_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Users(id),
    FOREIGN KEY (practitioner_id) REFERENCES Users(id),
    FOREIGN KEY (therapy_id) REFERENCES Therapies(id)
);

CREATE TABLE IF NOT EXISTS Precautions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type ENUM('pre', 'post') NOT NULL
);

CREATE TABLE IF NOT EXISTS Therapy_Precautions (
    therapy_id INT NOT NULL,
    precaution_id INT NOT NULL,
    PRIMARY KEY (therapy_id, precaution_id),
    FOREIGN KEY (therapy_id) REFERENCES Therapies(id) ON DELETE CASCADE,
    FOREIGN KEY (precaution_id) REFERENCES Precautions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT UNIQUE NOT NULL,
    patient_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    symptoms TEXT,
    side_effects TEXT,
    improvements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES Appointments(id),
    FOREIGN KEY (patient_id) REFERENCES Users(id)
);

-- 9. Notifications Table
-- Logs all notifications sent (in-app, email, sms)
CREATE TABLE IF NOT EXISTS Notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    channel ENUM('in_app', 'email', 'sms') NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
