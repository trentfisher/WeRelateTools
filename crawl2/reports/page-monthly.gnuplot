set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set yrange [0:]
set title "Page activity (monthly)"
plot \
 'tot-monthly.csv' skip 1 using 1:3 with lines title "active pages", \
 'tot-monthly.csv' skip 1 using 1:4 with lines title "edits", \
 'tot-monthly.csv' skip 1 using 1:5 with lines title "new pages", \
 'tot-monthly.csv' skip 1 using 1:6 with lines title "total pages" axes x1y2
