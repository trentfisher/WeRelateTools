.headers on
.mode csv
SELECT
    STRFTIME('%Y-%m', join_ts) AS month,
    COUNT(user)
FROM (select user, min(ts) as join_ts from vers group by user)
GROUP BY month
ORDER BY month;

