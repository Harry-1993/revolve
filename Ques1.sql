-- 1). Which manufacturer's planes had most no of flights? And how many flights?

SELECT
    p.manufacturer,
    COUNT(*) AS num_flights
FROM
    flights f
JOIN
    planes p ON f.tailnum = p.tailnum
GROUP BY
    p.manufacturer
ORDER BY
    num_flights DESC
LIMIT 1;