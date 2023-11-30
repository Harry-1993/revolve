-- 3).Which plane flew the most number of hours? And how many hours?

SELECT
    f.tailnum,
    p.manufacturer,
    SUM(CAST(f.air_time AS DECIMAL(10,2))) AS total_flying_hours
FROM
    flights f
JOIN
    planes p ON f.tailnum = p.tailnum
GROUP BY
    f.tailnum, p.manufacturer
ORDER BY
    total_flying_hours DESC
LIMIT 1;