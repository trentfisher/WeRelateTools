SELECT
	user
FROM (SELECT user, MIN(ts) AS first_ts FROM vers GROUP BY user)
WHERE first_ts >= date('now', 'start of month', '-1 month') AND first_ts < date('now', 'start of month')
