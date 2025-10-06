load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y"
set format x "%Y"
# TODO: increase this as the line nears the top
set y2range [0:5000000]
set y2tics
set ytics nomirror
set xtics nomirror
set format y "%.1s%c"
set format y2 "%.1s%c"
set yrange [0:]
set key top left
set title "Person and Family Page Activity (annual)"
plot \
 'tot-annually.csv' skip 1 using 1:3 with lines linewidth 2 title "active pages" , \
 'tot-annually.csv' skip 1 using 1:4 with lines linewidth 2 title "edits", \
 'tot-annually.csv' skip 1 using 1:5 with lines linewidth 2 title "new pages", \
 'tot-annually.csv' skip 1 using 1:6 with lines linewidth 2 title "total pages" axes x1y2
