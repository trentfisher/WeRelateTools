.headers on
.mode csv
SELECT
        STRFTIME('%Y-%m', ts) AS month,
        count(*) as edit_count,
        sum(newver) as new_count,
        sum(scoredif) as sum_scoredif,
        sum(scoredif)/CAST(count(*) as REAL),
        min(ts) as first_edit,
        max(ts) as latest_edit
FROM vers
GROUP BY STRFTIME('%Y-%m', ts)
ORDER BY month;
