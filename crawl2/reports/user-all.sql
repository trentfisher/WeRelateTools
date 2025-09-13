.headers on
.mode csv
SELECT
        user,
        count(*) as edit_count,
        sum(newver) as new_count,
        sum(scoredif) as tot_scoredif,
        cAST(count(*) as REAL)/sum(scoredif),
        min(ts) as first_edit,
        max(ts) as latest_edit
FROM vers
GROUP BY user
ORDER BY user;
