DROP DATABASE IF EXISTS face_attendance;
CREATE DATABASE face_attendance;
USE face_attendance;

CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE teacher_subjects (
    teacher_id INT,
    subject_id INT,
    PRIMARY KEY (teacher_id, subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    roll_number VARCHAR(255) NOT NULL UNIQUE,
    photo_dir VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE face_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    teacher_id INT,
    subject_id INT,
    attendance_date DATE,
    status ENUM('Present', 'Absent'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

INSERT INTO teachers (email, password, name)
VALUES ('teacher@example.com', 'password123', 'John Doe');

select * from teacher_subjects;
select * from face_images;
select * from teachers;
select * from subjects;
select * from teacher_subjects;
select * from attendance;


TRUNCATE TABLE teacher_subjects;
TRUNCATE TABLE teachers;



INSERT INTO subjects (name)
VALUES
('Numerical Methods and Probability Models (EE41)'),
('Electrical Measurements and Instrumentation (EE42)'),
('Field Theory (EE43)'),
('Microcontroller Programming and Interfacing (EE44)'),
('Electric Networks (EE45)'),
('Microcontrollers and Applications Lab (EEL46)'),
('Electrical AC Machine Lab (EEL47)'),
('Electrical Measurements and Instrumentation (Integrated) (EE42)'),
('Introduction to Product Design Lab(EEL48)'),
('Ability Enhancement Course IV (EEAEC49)'),
('Additional Mathematics II* (AM41)');

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE teachers;
SET FOREIGN_KEY_CHECKS = 1;

update teachers set password = '$2b$12$s/yIQLLpSNEfGeJ9w9KhyOT83xON61IQ4a06x11Mhs/biyFcbIQUG' where id = 1 ;
commit;