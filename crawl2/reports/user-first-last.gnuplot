set datafile separator ","
set xdata time
set ydata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%Y"
set format y "%Y"
set title "first v. last edit dates"
plot 'user-alltime.csv' skip 1 using 6:7 with points title ""
