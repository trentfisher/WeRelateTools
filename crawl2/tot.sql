.headers on
.mode csv
SELECT 
    month,
    total_score,
    count_users,
    count_pages,
    count_edits,
    sum_newver,
    SUM(sum_newver) OVER (ORDER BY month) AS cumulative_newver
FROM (
    SELECT 
        STRFTIME('%Y-%m', ts) AS month,
        SUM(CAST(score AS INTEGER)) AS total_score,
        COUNT(DISTINCT user) as count_users,
        COUNT(DISTINCT name) as count_pages,
        COUNT(*) as count_edits,
        SUM(CAST(newver AS INTEGER)) as sum_newver
    FROM 
        vers
    GROUP BY 
        STRFTIME('%Y-%m', ts)
)
ORDER BY 
    month;
