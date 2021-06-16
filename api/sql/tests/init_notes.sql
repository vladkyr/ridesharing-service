


-- fill history_orders
INSERT INTO history_orders (order_id, user_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price)
VALUES (123, 1, 3, 'loc1', 'dest1', 1, '2021-06-14 11:00:00', 10, '0:30:00', 30),
       (234, 2, 2, 'loc2', 'dest2', 2, '2021-06-14 12:00:00', 7, '0:20:00', 20),
       (345, 3, 1, 'loc3', 'dest3', 3, '2021-06-14 13:00:00', 5, '0:10:00', 10);










-- fill models
INSERT INTO models (manufacturer, model, capacity)
VALUES ('Tesla', 'Model 3', 5),
       ('Tesla', 'Model Y', 5),
       ('Tesla', 'Cybertruck', 6);

-- fill vehicles
INSERT INTO vehicles (model_id, status, number_plate)
VALUES (1, 'available', 'AAA 1234'),
       (2, 'busy', 'BBB 1234'),
       (3, 'available', 'CCC 1234');

-- fill users
INSERT INTO users (name, email, password, balance)
VALUES ('Bob Tall', 'bobtall@email.com', 'password1', 100),
       ('Fred Smith', 'fredsmith@email.com', 'password2', 100),
       ('Brian Black', 'brianblack@email.com', 'password3', 100);





-- Drop any existing data and create empty tables
-- Initialize the database

--DROP DATABASE if exists knights;

--CREATE DATABASE knights;
--use knights;

CREATE TABLE favorite_colors (
  name VARCHAR(20),
  color VARCHAR(10)
);

INSERT INTO favorite_colors (name, color) VALUES ('Lancelot', 'blue');

INSERT INTO
  favorite_colors (name, color)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');

INSERT INTO favorite_colors (name, color) VALUES ('Lancelot', 'blue');
INSERT INTO favorite_colors (name, color) VALUES ('Galahad', 'yellow');
INSERT INTO favorite_colors (name, color)
VALUES ('Bob', 'black'),
       ('Sam', 'white');




#cursor.execute('SELECT TABLE_NAME FROM information_schema.TABLES')
#cursor.execute('SELECT DISTINCT TABLE_SCHEMA FROM information_schema.TABLES')

