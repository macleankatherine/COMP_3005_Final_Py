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

INSERT INTO fitness_goals (member_id, goal_name, goal_description) VALUES
    (1, 'Weight Loss', 'To lose 10 pounds by the end of the month through a combination of diet and exercise.'),
    (1, 'Muscle Gain', 'To increase muscle mass and strength by following a structured weightlifting program.'),
    (2, 'Flexibility Improvement', 'To improve flexibility and mobility through regular stretching and yoga sessions.'),
    (3, 'Cardio Endurance', 'To improve cardiovascular endurance by running 5 kilometers without stopping.'),
    (2, 'Body Composition Change', 'To decrease body fat percentage and increase lean muscle mass.'),
    (3, 'Overall Health and Wellness', 'To adopt a healthier lifestyle by incorporating regular exercise and balanced nutrition.');

INSERT INTO fitness_achievements (member_id, achievement_name, achievement_description) VALUES
(1, '5K Run', 'Completed a 5-kilometer run in under 30 minutes.'),
(1, 'Weight Loss Milestone', 'Lost 10 pounds and reached the first weight loss milestone.'),
(2, 'Muscle Gain Progress', 'Increased muscle mass and strength by 10% over the past three months.'),
(3, 'Improved Flexibility', 'Achieved full splits and improved overall flexibility by attending regular yoga classes.'),
(2, 'Fitness Competition Win', 'Won first place in a local fitness competition.'),
(1, 'Consistent Gym Attendance', 'Maintained consistent gym attendance for six months straight.');

INSERT INTO Trainers (first_name, last_name, password, phone_number)
VALUES
    ('John', 'Doe', 'password123', '123-456-7890'),
    ('Alice', 'Smith', 'securepass', '987-654-3210'),
    ('Mike', 'Johnson', 'mypassword', '555-555-5555');


INSERT INTO room_bookings (room_id, day_of_week, start_time, end_time, recurrence)
VALUES
    (1, 'Monday', '09:00:00', '10:00:00', 'Weekly'),
    (2, 'Tuesday', '14:00:00', '15:00:00', 'Bi-weekly'),
    (3, 'Wednesday', '10:30:00', '11:30:00', 'Monthly');


INSERT INTO group_training_classes (trainer_id, name, booking_id, details)
VALUES
    (1, 'Yoga Class', 1, 'Beginner-friendly yoga session'),
    (2, 'HIIT Workout', 2, 'High-intensity interval training for advanced fitness enthusiasts'),
    (3, 'Zumba Dance Party', 3, 'Fun and energetic dance workout');

INSERT INTO group_training_class_members (class_id, member_id)
VALUES
    (1, 1), -- Yoga Class with member_id 1
    (2, 2), -- HIIT Workout with member_id 2
    (3, 3); -- Zumba Dance Party with member_id 3

INSERT INTO trainer_availability (trainer_id, day_of_week, start_time, end_time) VALUES
    (1, 'Monday', '08:00', '22:00'),
    (1, 'Tuesday', '08:00', '22:00'),
    (1, 'Wednesday', '08:00', '22:00'),
    (1, 'Thursday', '08:00', '22:00'),
    (1, 'Friday', '08:00', '22:00'),
    (1, 'Saturday', '08:00', '22:00'),
    (1, 'Sunday', '08:00', '22:00'),
    (2, 'Tuesday', '13:00', '17:00'),
    (3, 'Friday', '11:00', '15:00');

INSERT INTO exercise_routines (member_id, routine_name, routine_description) VALUES
    (1, 'Morning Workout', 'A routine focused on cardio and stretching to start the day.'),
    (1, 'Strength Training', 'A routine consisting of weightlifting exercises to build muscle.'),
    (2, 'Yoga Flow', 'A routine of yoga poses and stretches for flexibility and relaxation.'),
    (3, 'High-Intensity Interval Training (HIIT)', 'A routine that alternates between intense bursts of exercise and short recovery periods.'),
    (3, 'Endurance Running', 'A routine for building endurance through long-distance running.'),
    (2, 'Bodyweight Circuit', 'A routine using only bodyweight exercises for a full-body workout.'),
    (3, 'Flexibility Routine', 'A routine focused on stretching and mobility exercises.');

