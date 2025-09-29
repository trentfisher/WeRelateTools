.headers on
.mode csv
SELECT name, score, ts
FROM (
    SELECT name, score, ts,
    ROW_NUMBER() OVER (PARTITION BY name ORDER BY ts DESC) AS row_num
    FROM vers
)
WHERE row_num = 1 ORDER BY score DESC LIMIT 100;
