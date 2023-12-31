-- 5). Which manufactures planes had covered most distance? And how much distance?
SELECT
    p.manufacturer,
    SUM(f.distance) AS total_distance
FROM
    planes p
JOIN
    flights f ON p.tailnum = f.tailnum
GROUP BY
    p.manufacturer
ORDER BY
    total_distance DESC
LIMIT 1;