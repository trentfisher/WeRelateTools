.headers on
.mode csv
SELECT
    first_edit_month,
    COUNT(*) AS users_this_month,
    COUNT(CASE WHEN lifetime > 1 THEN 1 END) AS users_retained,
    (COUNT(CASE WHEN lifetime > 1 THEN 1 END)*1.0 / COUNT(*)) * 100 AS retention_percent
FROM
    (SELECT
        user,
        MIN(ts) as first_edit,
        STRFTIME('%Y-%m', MIN(ts)) as first_edit_month,
        MAX(ts) as latest_edit,
        (julianday(MAX(ts)) - julianday(MIN(ts)))/365 as lifetime
     FROM vers
     WHERE ts < date('now', 'start of month', '-12 month')
     GROUP BY user)
GROUP BY first_edit_month
ORDER BY first_edit_month

