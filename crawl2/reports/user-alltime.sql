.headers on
.mode csv
SELECT
        user,
        COUNT(*) as edit_count,
        SUM(newver) as new_count,
        SUM(scoredif) as tot_scoredif,
        SUM(scoredif)/CAST(count(*) as REAL) AS scoredif_per_edit,
        MIN(ts) as first_edit,
        MAX(ts) as latest_edit,
        (julianday(MAX(ts)) - julianday(MIN(ts)))/365 as lifetime
FROM vers
GROUP BY user
ORDER BY user;
