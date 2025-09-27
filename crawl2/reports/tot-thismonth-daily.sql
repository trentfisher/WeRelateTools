.headers on
.mode csv
SELECT
        STRFTIME('%Y-%m-%d', ts) AS day,
	COUNT(DISTINCT user) as count_users,
        COUNT(DISTINCT name) as count_pages,
        COUNT(*) as count_edits,
        SUM(CAST(newver AS INTEGER)) as count_newver,
        SUM(CAST(score AS INTEGER)) AS sum_score,
        SUM(CAST(scoredif AS INTEGER)) as sum_scoredif,
        sum(scoredif)/CAST(count(*) as REAL) as scoredif_per_edit
FROM
	vers
WHERE ts >= date('now', '-1 month')
GROUP BY
        STRFTIME('%Y-%m-%d', ts)
ORDER BY
        STRFTIME('%Y-%m-%d', ts)
