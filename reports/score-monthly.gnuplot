load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set format y "%.1s%c"
set format y2 "%.1s%c"
set y2tics
set ytics nomirror
set xtics nomirror
set yrange [0:*]
set title "Page Scores (monthly)"
plot \
 'tot-monthly.csv' skip 1 using 1:9 with lines linewidth 2 title "score diff/edit", \
 'tot-monthly.csv' skip 1 using 1:8 smooth cumulative with lines linewidth 2 title "total score" axis x1y2
 