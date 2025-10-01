set datafile separator ","
set xdata time
set timefmt "%d %b %Y"
set format x "%Y"
set yrange [0:4000]
set y2range[0:3500000]
set y2tics
set ytics nomirror
set xtics nomirror
set format y "%.0f"
set format y2 "%.0f"
set title "Person activity (annually)"
plot \
 'tot-persons-old.csv' skip 1 using 1:6 with lines title "growth per day", \
 'tot-persons-old.csv' skip 1 using 1:2 with lines title "total person pages" axes x1y2
