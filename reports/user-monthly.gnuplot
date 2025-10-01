load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set title "Active Users (monthly)"
set style fill transparent solid 0.8
plot 'tot-monthly.csv' skip 1 using 1:2 with fillsteps title ""