set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set yrange [0:*]
set title "Page Scores (monthly)"
plot \
 'tot-monthly.csv' skip 1 using 1:8 with lines title "score diff", \
 'tot-monthly.csv' skip 1 using 1:8 smooth cumulative with lines title "total score" axis x1y2
 