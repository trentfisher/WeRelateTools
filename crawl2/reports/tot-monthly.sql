-- A report of monthly changes
.headers on
.mode csv
SELECT 
    month,
    count_users,
    count_pages,
    count_edits,
    count_newver,
    SUM(count_newver) OVER (ORDER BY month) AS cumulative_newver,
    sum_score,
    sum_scoredif,
    scoredif_per_edit
FROM (
    SELECT 
        STRFTIME('%Y-%m', ts) AS month,
	COUNT(DISTINCT user) as count_users,
        COUNT(DISTINCT name) as count_pages,
        COUNT(*) as count_edits,
        SUM(CAST(newver AS INTEGER)) as count_newver,
        SUM(CAST(score AS INTEGER)) AS sum_score,
        SUM(CAST(scoredif AS INTEGER)) as sum_scoredif,
        sum(scoredif)/CAST(count(*) as REAL) as scoredif_per_edit
    FROM
        vers
    GROUP BY 
        STRFTIME('%Y-%m', ts)
)
ORDER BY 
    month;
