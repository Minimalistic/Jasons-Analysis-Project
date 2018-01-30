# Jasons-Analysis-Project
Udacity Database Querying Project

## Views


<!-- Todo

`top_slugs_view`

 ```
 CREATE VIEW top_slugs_view AS SELECT path, COUNT(*) AS num_views FROM log WHERE status = '200 OK' AND NOT path = '/' GROUP BY path ORDER BY num_views DESC;
 ``` -->