SELECT m.manufacturer, m.model, m.capacity, COUNT(*) as trips_number, AVG(trip_time) as avg_trip_time, AVG(passengers) as avg_passengers
FROM history_orders AS h
JOIN vehicles AS v ON v.vehicle_id = h.vehicle_id
JOIN models AS m ON m.model_id = v.model_id
WHERE h.end_time > ( SELECT CURRENT_TIMESTAMP() ) - INTERVAL 1 YEAR
GROUP BY m.manufacturer, m.model, m.capacity
ORDER BY trips_number DESC;