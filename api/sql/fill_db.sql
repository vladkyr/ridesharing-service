-- fill models
INSERT INTO models (manufacturer, model, capacity)
VALUES ('man1', 'man1_m1', 5),
       ('man2', 'man2_m1', 7),
       ('man3', 'man3_m1', 6);

-- fill vehicles
INSERT INTO vehicles (model_id, status, number_plate)
VALUES (1, 'available', 'AAA 1234'),
       (2, 'busy', 'BBB 1234'),
       (3, 'available', 'CCC 1234');

-- fill users
INSERT INTO users (name, email, password, balance)
VALUES ('user1', 'user1@email.com', 'password1', 100),
       ('user2', 'user2@email.com', 'password2', 50),
       ('user3', 'user3@email.com', 'password3', 225);

-- fill orders
INSERT INTO orders (user_id, vehicle_id, start_loc, destination, status, passengers)
VALUES (1, 3, 'loc1', 'dest1', 'in progress', 1),
       (2, 2, 'loc2', 'dest2', 'new', 3),
       (3, 1, 'loc3', 'dest3', 'at start_loc', 5);

-- fill history_orders
INSERT INTO history_orders (order_id, user_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price)
VALUES (123, 1, 3, 'loc1', 'dest1', 1, '2021-06-14 11:00:00', 10, '0:30:00', 30),
       (234, 2, 2, 'loc2', 'dest2', 2, '2021-06-14 12:00:00', 7, '0:20:00', 20),
       (345, 3, 1, 'loc3', 'dest3', 3, '2021-06-14 13:00:00', 5, '0:10:00', 10);