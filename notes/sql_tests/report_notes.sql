-- SQL query for getting report "Find most popular car types"

-- A report about most used models of vehicles within last year.
-- Show vehicle’s make, model, capacity, average number of persons per trip and average trip duration, number of trips, sorted by number of trips.
-- Use entities: History_Orders, Vehicle, Model
-- Filtered by: trip date (last year)
-- Sorted by: number of trips

--SELECT * FROM vehicles;

--------------------------------------------------------------------------------------------------------
-- data
-- fill history_orders
INSERT INTO history_orders (order_id, user_id, vehicle_id, start_loc, destination, passengers, end_time, distance, trip_time, price)
VALUES (111, 1, 3, 'loc1', 'dest1', 1, '2021-06-14 11:00:00', 10, '0:30:00', 30),
       (222, 2, 2, 'loc2', 'dest2', 2, '2019-06-14 12:00:00', 7, '0:20:00', 20),
       (223, 2, 2, 'loc2', 'dest2', 2, '2021-06-14 12:00:00', 7, '0:30:00', 20),
       (224, 2, 2, 'loc2', 'dest2', 2, '2021-06-14 12:00:00', 7, '0:40:00', 20),
       (333, 2, 1, 'loc2', 'dest2', 2, '2021-06-14 12:00:00', 7, '0:20:00', 20),
       (334, 3, 1, 'loc3', 'dest3', 3, '2021-06-14 13:00:00', 5, '0:10:00', 10);

--------------------------------------------------------------------------------------------------------
-- v1:
-- Show vehicle_id, number of trips per vehicle_id.
SELECT vehicle_id, COUNT(*) as trips_number
FROM history_orders
GROUP BY vehicle_id;

-- {"report results": [[1, 2], [2, 3], [3, 1]]}
--------------------------------------------------------------------------------------------------------
-- v2
-- Show vehicle_id, number of trips, average trip duration.
SELECT vehicle_id, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time
FROM history_orders
GROUP BY vehicle_id;

-- {"report results": [["1", "2", "1500.0000"], ["2", "3", "3000.0000"], ["3", "1", "3000.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v3
-- Show vehicle_id, number of trips, average trip duration, average number of persons per trip.
SELECT vehicle_id, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders
GROUP BY vehicle_id;

-- {"report results": [["1", "2", "1500.0000", "2.5000"], ["2", "3", "3000.0000", "2.0000"], ["3", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v4
-- Show vehicle_id, average number of persons per trip and average trip duration, number of trips, sorted by number of trips.
SELECT vehicle_id, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders
GROUP BY vehicle_id
ORDER BY trips_number DESC;

-- {"report results": [["2", "3", "3000.0000", "2.0000"], ["1", "2", "1500.0000", "2.5000"], ["3", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v5
-- Show vehicle’s model_id, number of trips, average trip duration, average number of persons per trip, sorted by number of trips.
SELECT m.model_id, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders AS h
JOIN vehicles AS v ON v.vehicle_id = h.vehicle_id
JOIN models AS m ON m.model_id = v.model_id
GROUP BY m.model_id
ORDER BY trips_number DESC;

-- maybe LEFT or RIGHT join in line 4 where joining models

-- {"report results": [["2", "3", "3000.0000", "2.0000"], ["1", "2", "1500.0000", "2.5000"], ["3", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v6
-- Show vehicle’s make, model, capacity, number of trips, average trip duration, average number of persons per trip, sorted by number of trips.
SELECT m.manufacturer, m.model, m.capacity, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders AS h
JOIN vehicles AS v ON v.vehicle_id = h.vehicle_id
JOIN models AS m ON m.model_id = v.model_id
GROUP BY m.manufacturer, m.model, m.capacity
ORDER BY trips_number DESC;

-- {"report results": [["man2", "man2_m1", "7", "3", "3000.0000", "2.0000"], ["man1", "man1_m1", "5", "2", "1500.0000", "2.5000"], ["man3", "man3_m1", "6", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v7
-- Show vehicle’s make, model, capacity, number of trips, average trip duration, average number of persons per trip, sorted by number of trips, filtered by date (last year).
SELECT m.manufacturer, m.model, m.capacity, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders AS h
JOIN vehicles AS v ON v.vehicle_id = h.vehicle_id
JOIN models AS m ON m.model_id = v.model_id
WHERE h.end_time > '2020-06-14 11:00:00'
GROUP BY m.manufacturer, m.model, m.capacity
ORDER BY trips_number DESC;

-- {"report results": [["man2", "man2_m1", "7", "2", "3500.0000", "2.0000"], ["man1", "man1_m1", "5", "2", "1500.0000", "2.5000"], ["man3", "man3_m1", "6", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- v8
-- Show vehicle’s make, model, capacity, number of trips, average trip duration, average number of persons per trip, sorted by number of trips, filtered by date (last year).
SELECT m.manufacturer, m.model, m.capacity, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders AS h
JOIN vehicles AS v ON v.vehicle_id = h.vehicle_id
JOIN models AS m ON m.model_id = v.model_id
WHERE h.end_time > ( SELECT CURRENT_TIMESTAMP() ) - INTERVAL 1 YEAR
GROUP BY m.manufacturer, m.model, m.capacity
ORDER BY trips_number DESC;

-- {"report results": [["man1", "man1_m1", "5", "2", "1500.0000", "2.5000"], ["man2", "man2_m1", "7", "2", "3500.0000", "2.0000"], ["man3", "man3_m1", "6", "1", "3000.0000", "1.0000"]]}
--------------------------------------------------------------------------------------------------------
-- after some modeifications of fill data and results
-- { "report results": [
-- { "manufacturer": "maker1", "model": "maker1_m1", "capacity": 5, "trips": 3, "avg_trip_time": 21, "avg_passengers": 2.7 },
-- { "manufacturer": "maker2", "model": "maker2_m1", "capacity": 7, "trips": 2, "avg_trip_time": 37, "avg_passengers": 2.5 },
-- { "manufacturer": "maker3", "model": "maker3_m1", "capacity": 6, "trips": 1, "avg_trip_time": 17, "avg_passengers": 1.0 }
-- ] }