-- 4). Which destination had most delay in flights?
SELECT
    dest,
    SUM(CAST(arr_delay AS DECIMAL(10,2))) AS total_delay_time
FROM
    flights
WHERE
    arr_delay IS NOT NULL
GROUP BY
    dest
ORDER BY
    total_delay_time DESC
LIMIT 1;