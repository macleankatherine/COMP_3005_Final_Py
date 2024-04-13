CREATE TABLE IF NOT EXISTS Members(
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    weight VARCHAR(255), 
    height VARCHAR(255),
    bodyfat_percent VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fitness_goals(
    goal_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    goal_name VARCHAR(255) NOT NULL,
    goal_description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS fitness_achievements(
    achievement_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    achievement_name VARCHAR(255) NOT NULL,
    achievement_description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS exercise_routines(
    routine_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    routine_name VARCHAR(255) NOT NULL,
    routine_description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Trainers(
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS trainer_availability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Administrators(
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) UNIQUE NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS room_bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES Rooms(room_id),
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    recurrence VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS personal_training_classes(
    class_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    member_id INT REFERENCES Members(member_id),
    booking_id INT UNIQUE REFERENCES room_bookings(booking_id),
    details VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS group_training_classes(
    class_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    name VARCHAR(255) NOT NULL,
    booking_id INT UNIQUE REFERENCES room_bookings(booking_id),
    details VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS group_training_class_members (
    class_id INT REFERENCES group_training_classes(class_id),
    member_id INT REFERENCES Members(member_id),
    PRIMARY KEY (class_id, member_id)
);

CREATE TABLE IF NOT EXISTS Equipment(
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255) NOT NULL,
    equipment_description VARCHAR(255) NOT NULL,
    room_id INT REFERENCES Rooms(room_id)
);

CREATE TABLE IF NOT EXISTS equipment_maintentence(
    request_id SERIAL PRIMARY KEY,
    request_name VARCHAR(255) NOT NULL,
    request_details VARCHAR(255) NOT NULL,
    equipment_id INT REFERENCES Equipment(equipment_id),
    request_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Billing(
    billing_id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    amount FLOAT NOT NULL,
    billing_room_id INT REFERENCES room_bookings(booking_id),
    billing_session_id INT REFERENCES personal_training_classes(class_id),
    member_id INT REFERENCES Members(member_id)
);
