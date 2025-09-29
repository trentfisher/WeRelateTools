.headers on
.mode csv
SELECT
        user,
        count(*) as edit_count,
        sum(newver) as new_count,
        sum(scoredif) as tot_scoredif,
  	sum(scoredif)/CAST(count(*) as REAL) AS scoredif_per_edit,
        min(ts) as first_edit,
        max(ts) as latest_edit
FROM vers
WHERE ts >= date('now', '-14 days')
GROUP BY user
ORDER BY user;
