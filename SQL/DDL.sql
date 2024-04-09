CREATE TABLE IF NOT EXISTS Members(
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    weight VARCHAR(255),  --not sure if the metrics should be not null
    height VARCHAR(255),
    bodyfat_percent VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS exersize_routines(
    routine_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    goal_name VARCHAR(255) NOT NULL,
    goal_desciption VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Fitness_Goals(
    goal_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    goal_name VARCHAR(255) NOT NULL,
    goal_desciption VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Trainers(
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Administrators(
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS personal_training_classes(
    session_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    member_id INT REFERENCES Members(member_id)
);

CREATE TABLE IF NOT EXISTS group_training_classes(
    class_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES Trainers(trainer_id),
    member_id INT REFERENCES Members(member_id),
    theDay DATE NOT NULL
);


CREATE TABLE IF NOT EXISTS Equipment(
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255) NOT NULL,
    equipment_description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Equipment_Maintentence(
    class_id SERIAL PRIMARY KEY,
    responsible_admin_id INT REFERENCES Administrators(admin_id),
    equipment_name VARCHAR(255) NOT NULL,
    equipment_id INT REFERENCES Equipment(equipment_id),
    theDay DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS billing(
    billing_id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    amount FLOAT NOT NULL,
    billing_session_id INT REFERENCES personal_training_classes(session_id),
    member_id INT REFERENCES Members(member_id)
);



-- -- everything under this line is testing

-- -- reset table data
-- TRUNCATE  Fitness_Goals CASCADE;

-- -- Insert test data into Members table
-- INSERT INTO Members (first_name, last_name, username, phone_number)
-- VALUES 
--     ('John', 'Doe', 'johndoe', '123-456-7890'),
--     ('Jane', 'Smith', 'janesmith', '987-654-3210');

-- -- Insert test data into Fitness_Goals table
-- INSERT INTO Fitness_Goals (member_id, goal_name, goal_desciption)
-- VALUES 
--     (1, 'Weight Loss', 'Lose 10 pounds in 2 months'),
--     (1, 'Muscle Gain', 'Gain muscle mass and increase strength');


-- SELECT *
-- FROM Members 
-- INNER JOIN Fitness_Goals ON Fitness_Goals.member_id = Members.member_id;

