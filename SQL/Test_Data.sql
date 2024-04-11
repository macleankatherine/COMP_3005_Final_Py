--Test Data
INSERT INTO Rooms (room_name, capacity)
VALUES
    ('Room 1', 20),
    ('Room 2', 15),
    ('Room 3', 30);

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

INSERT INTO Room_Bookings (room_id, start_datetime, end_datetime, recurrence)
VALUES
    (1, '2024-04-15 09:00:00', '2024-04-15 10:00:00', 'Weekly'),
    (2, '2024-04-16 14:00:00', '2024-04-16 15:00:00', 'Bi-weekly'),
    (3, '2024-04-17 10:30:00', '2024-04-17 11:30:00', 'Monthly');

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
