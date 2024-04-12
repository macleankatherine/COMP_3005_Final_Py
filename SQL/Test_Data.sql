--Test Data
INSERT INTO Rooms (room_name, capacity)
VALUES
    ('Room 1', 20),
    ('Room 2', 15),
    ('Room 3', 30),
    ('Room 4', 20);

INSERT INTO Members (first_name, last_name, email, password, phone_number, weight, height, bodyfat_percent)
VALUES
    ('Emily', 'Jones', 'emily@example.com', 'password123', '123-456-7890', '150', '65', '20'),
    ('Michael', 'Brown', 'michael@example.com', 'securepass', '987-654-3210', '180', '72', '15'),
    ('Sarah', 'Davis', 'sarah@example.com', 'mypassword', '555-555-5555', '130', '60', '25');

INSERT INTO Trainers (first_name, last_name, password, phone_number)
VALUES
    ('John', 'Doe', 'password123', '123-456-7890'),
    ('Alice', 'Smith', 'securepass', '987-654-3210'),
    ('Mike', 'Johnson', 'mypassword', '555-555-5555');


INSERT INTO Room_Bookings (room_id, day_of_week, start_time, end_time, recurrence)
VALUES
    (1, 'Monday', '09:00:00', '10:00:00', 'Weekly'),
    (2, 'Tuesday', '14:00:00', '15:00:00', 'Bi-weekly'),
    (3, 'Wednesday', '10:30:00', '11:30:00', 'Monthly'),
    (4, 'Sunday', '09:00:00', '10:00:00', 'Yearly');


INSERT INTO Group_training_classes (trainer_id, name, booking_id, details)
VALUES
    (1, 'Yoga Class', 1, 'Beginner-friendly yoga session'),
    (2, 'HIIT Workout', 2, 'High-intensity interval training for advanced fitness enthusiasts'),
    (3, 'Zumba Dance Party', 3, 'Fun and energetic dance workout');

INSERT INTO Group_training_class_members (class_id, member_id)
VALUES
    (1, 1), -- Yoga Class with member_id 1
    (2, 2), -- HIIT Workout with member_id 2
    (3, 3); -- Zumba Dance Party with member_id 3

INSERT INTO Trainer_Availability (trainer_id, day_of_week, start_time, end_time) VALUES
    (1, 'Monday', '08:00', '22:00'),
    (1, 'Tuesday', '08:00', '22:00'),
    (1, 'Wednesday', '08:00', '22:00'),
    (1, 'Thursday', '08:00', '22:00'),
    (1, 'Friday', '08:00', '22:00'),
    (1, 'Saturday', '08:00', '22:00'),
    (1, 'Sunday', '08:00', '22:00'),
    (2, 'Tuesday', '13:00', '17:00'),
    (3, 'Friday', '11:00', '15:00');


-- TEST DATA FOR TRAINER FUNCTIONALITIES
INSERT INTO Personal_training_classes (trainer_id, member_id, booking_id, details) VALUES
    (1, 1, 1, 'Personal training session for strength and conditioning'),
    (2, 2, 2, 'Customized workout plan focusing on weight loss goals'),
    (3, 3, 3, 'Functional training session to improve mobility and flexibility'),
    (1, 2, 4, 'Power Lifting Training BSD');

INSERT INTO Trainer_Availability (trainer_id, day_of_week, start_time, end_time)
VALUES
    (1, 'Monday', '09:00:00', '12:00:00'),
    (1, 'Wednesday', '13:00:00', '17:00:00'),
    (1, 'Friday', '10:00:00', '14:00:00'),
    (2, 'Tuesday', '08:00:00', '11:00:00'),
    (3, 'Thursday', '14:00:00', '18:00:00');

