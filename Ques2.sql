-- 2). Which manufacturer's planes had most no of flying hours? And how many hours?

SELECT
    p.manufacturer,
    SUM(CAST(f.air_time AS DECIMAL(10,2))) AS total_flying_hours
FROM
    flights f
JOIN
    planes p ON f.tailnum = p.tailnum
GROUP BY
    p.manufacturer
ORDER BY
    total_flying_hours DESC
LIMIT 1;