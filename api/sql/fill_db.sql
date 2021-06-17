-- fill models
INSERT INTO models (manufacturer, model, capacity)
VALUES ('maker1', 'maker1_m1', 5),
       ('maker2', 'maker2_m1', 7),
       ('maker3', 'maker3_m1', 6);

-- fill vehicles
INSERT INTO vehicles (model_id, status, number_plate)
VALUES (1, 'available', 'AAA 1234'),
       (2, 'busy', 'BBB 1234'),
       (3, 'available', 'CCC 1234');

-- fill users
INSERT INTO users (name, email, password, balance)
VALUES ('user1', 'user1@email.com', 'password1', 100),
       ('user2', 'user2@email.com', 'password2', 50),
       ('user3', 'user3@email.com', 'password3', 225),
       ('user4', 'em4', 'pass4', 25);

-- fill orders
INSERT INTO orders (user_id, vehicle_id, start_loc, destination, status, passengers)
VALUES (1, 3, 'loc1', 'dest1', 'in progress', 1),
       (2, 2, 'loc2', 'dest2', 'new', 3),
       (3, 1, 'loc3', 'dest3', 'at start_loc', 5);

-- fill history_orders
INSERT INTO history_orders (order_id, user_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price)
VALUES (101, 1, 3, 'loc1', 'dest1', 1, '2021-06-14 11:00:00', 10, 17, 30),
       (201, 2, 2, 'loc2', 'dest2', 2, '2019-06-18 12:00:00', 7, 18, 20),
       (202, 1, 2, 'loc2', 'dest3', 4, '2021-06-14 19:00:00', 15, 31, 23),
       (203, 2, 2, 'loc1', 'dest2', 1, '2021-03-07 20:00:00', 27, 44, 25),
       (301, 3, 1, 'loc2', 'dest2', 2, '2021-05-28 08:00:00', 7, 20, 20),
       (302, 2, 1, 'loc3', 'dest3', 1, '2021-02-03 13:00:00', 6, 12, 9),
       (303, 1, 1, 'loc4', 'dest1', 3, '2018-04-09 15:00:00', 5, 10, 10),
       (304, 3, 1, 'loc4', 'dest4', 5, '2020-08-14 10:00:00', 20, 33, 25);