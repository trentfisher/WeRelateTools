load "gnuplot-common"
set datafile separator ","
set xdata time
set title "Person Pages old v. new"
set format x "%Y"
set format y "%.1s%c"
plot \
     'tot-persons-old.csv' skip 1 using (strptime("%d %b %Y", strcol(1))):2 with linespoints linewidth 2 pointtype 5 title "old values", \
     'tot-annually.csv'    skip 1 using (strptime("%Y", strcol(1))):6       with linespoints linewidth 2 pointtype 5 title "new values"

