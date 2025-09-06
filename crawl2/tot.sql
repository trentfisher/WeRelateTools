.headers on
.mode csv
SELECT 
        COUNT(DISTINCT user) as count_users,
        COUNT(DISTINCT name) as count_pages,
        COUNT(*) as count_edits,
        SUM(CAST(newver AS INTEGER)) as sum_newver,
        SUM(CAST(score AS INTEGER)) AS total_score,
        SUM(CAST(scoredif AS INTEGER)) as sum_scoredif
    FROM 
        vers
ORDER BY 
    user;
