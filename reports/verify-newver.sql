PRAGMA busy_timeout = 30000;

-- look for cases where the version history for a page has no start marker
SELECT name
FROM vers
GROUP BY name
HAVING SUM(CASE WHEN newver = 1 THEN 1 ELSE 0 END) = 0;

-- look for pages listed in the version table don't have an entry in the relations table
SELECT name FROM vers WHERE name NOT IN (SELECT name FROM relations);

-- look for pages listed in relations not mentioned in vers table
SELECT name FROM relations WHERE name NOT IN (SELECT name FROM vers);
