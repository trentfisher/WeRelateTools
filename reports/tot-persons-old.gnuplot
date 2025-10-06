load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%d %b %Y"
set format x "%Y"
set yrange [0:4000]
set y2range[0:4000000]
set y2tics
set ytics nomirror
set xtics nomirror
set format y "%.0f"
set format y2 "%.1s%c"
set title "Person page activity (annual)"
plot \
 'tot-persons-old.csv' skip 1 using 1:6 with lines linewidth 2 title "growth per day", \
 'tot-persons-old.csv' skip 1 using 1:2 with linespoints linewidth 2 title "total person pages" axes x1y2
