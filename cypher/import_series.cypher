// loops through local CSVs whose names equal MacroSeries ids
LOAD CSV WITH HEADERS FROM $url AS row
WITH row, $seriesId AS sid, $column AS col
WHERE row.observation_date <> '' AND row[col] <> '.'
WITH date(row.observation_date) AS d, toFloat(row[col]) AS v, sid
MATCH (s:MacroSeries {id:sid})
MERGE (p:MacroPoint {date:d})
SET   p.value = v
MERGE (s)-[:RECORDED_ON]->(p);
