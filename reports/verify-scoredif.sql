WITH ranked_versions AS (
  SELECT name, id, score, scoredif,
         LAG(score) OVER (PARTITION BY name ORDER BY id) AS prev_score
  FROM vers
)
SELECT name, id, score, scoredif, prev_score
FROM ranked_versions
WHERE prev_score IS NOT NULL AND scoredif != score - prev_score;


/*
 * this can be used to fix the cases found by the query above
 
UPDATE vers
SET scoredif = (
  SELECT score - prev_score
  FROM (
    SELECT name, id, score,
           LAG(score) OVER (PARTITION BY name ORDER BY id) AS prev_score
    FROM vers
  ) AS ranked_versions
  WHERE ranked_versions.name = vers.name AND ranked_versions.id = vers.id
)
WHERE EXISTS (
  SELECT 1
  FROM (
    SELECT name, id, score,
           LAG(score) OVER (PARTITION BY name ORDER BY id) AS prev_score
    FROM vers
  ) AS ranked_versions
  WHERE ranked_versions.name = vers.name AND ranked_versions.id = vers.id AND ranked_versions.prev_score IS NOT NULL
);

*/
