load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set yrange [0:]
set y2tics
set ytics nomirror
set xtics nomirror
set format y "%.0f"
set format y2 "%.0f"
set key top left
set title "Person and Family Page activity (monthly)"
plot \
 'tot-monthly.csv' skip 1 using 1:3 with lines linewidth 2 title "active pages", \
 'tot-monthly.csv' skip 1 using 1:4 with lines linewidth 2 title "edits", \
 'tot-monthly.csv' skip 1 using 1:5 with lines linewidth 2 title "new pages", \
 'tot-monthly.csv' skip 1 using 1:6 with lines linewidth 2 title "total pages" axes x1y2
