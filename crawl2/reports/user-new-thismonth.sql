SELECT
	user
FROM (SELECT user, MIN(ts) AS first_ts FROM vers GROUP BY user)
WHERE first_ts >= date('now', '-1 month')
