-- 6). Which airport had most flights on weekends?

SELECT
    a.AIRPORT,
    COUNT(*) AS num_flights
FROM
    flights f
JOIN
    airports a ON f.origin = a.IATA_CODE
WHERE
    DAYOFWEEK(CONCAT(f.year, '-', LPAD(f.month, 2, '0'), '-', LPAD(f.day, 2, '0'))) IN (1, 7)
GROUP BY
    a.AIRPORT
ORDER BY
    num_flights DESC
LIMIT 1;