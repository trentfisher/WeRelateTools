load "gnuplot-common"

set datafile separator ","

set xdata time
set timefmt "%Y-%m"

set format x "%Y"
set y2tics
set ytics nomirror
set xtics nomirror
set ylabel "percent"
set y2label "new users"

set title "User Retention (one year after first edit)"
plot \
     'user-retention-monthly.csv' skip 1 using 1:4 with linespoints pointtype 7 title "", \
     'user-retention-monthly.csv' skip 1 using 1:2 with steps axis x1y2 title ""
