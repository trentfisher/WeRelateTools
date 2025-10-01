-- This generates a summary of activity over a given time period
-- the start and end dates are specified in the temporary table "params"
-- the default is for all time
.headers on
.mode csv

-- set up the temporary table with the defaults
CREATE TEMP TABLE IF NOT EXISTS params (k TEXT, v TEXT, PRIMARY KEY(k));
INSERT OR IGNORE INTO params VALUES ('startdate', '01-01-2000');
INSERT OR IGNORE INTO params VALUES ('enddate',   date('now'));

SELECT
	CASE
		WHEN name LIKE 'Person:%' THEN 'Person'
		WHEN name LIKE 'Family:%' THEN 'Family'
		ELSE 'Unknown'
	END AS prefix,
    STRFTIME('%Y-%m-%d', MIN(ts)) AS first_edit,
    STRFTIME('%Y-%m-%d', MAX(ts)) AS last_edit,
	COUNT(DISTINCT user) as count_users,
    COUNT(DISTINCT name) as count_pages,
    COUNT(*) as count_edits,
    SUM(CAST(newver AS INTEGER)) as sum_newver,
    SUM(CAST(score AS INTEGER)) AS sum_score,
    SUM(CAST(scoredif AS INTEGER)) as sum_scoredif,
    SUM(scoredif)/CAST(count(*) as REAL) as scoredif_per_edit
FROM 
	vers
WHERE ts >= (SELECT v FROM params WHERE k = 'startdate') AND
      ts <  (SELECT v FROM params WHERE k = 'enddate')
GROUP BY
    prefix;
-- This could be done with UNION ALL, but it seems faster as a separate query
.headers off
SELECT
	"TOTAL",
    STRFTIME('%Y-%m-%d', MIN(ts)) AS first_edit,
    STRFTIME('%Y-%m-%d', MAX(ts)) AS last_edit,
	COUNT(DISTINCT user) as count_users,
	COUNT(DISTINCT name) as count_pages,
 	COUNT(*) as count_edits,
	SUM(CAST(newver AS INTEGER)) as sum_newver,
	SUM(CAST(score AS INTEGER)) AS total_score,
	SUM(CAST(scoredif AS INTEGER)) as sum_scoredif
FROM 
	vers
WHERE ts >= (SELECT v FROM params WHERE k = 'startdate') AND
      ts <  (SELECT v FROM params WHERE k = 'enddate');
