load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%Y"
set title "first edit date v. tenure"
plot 'user-alltime.csv' skip 1 using 6:8 with points title ""
