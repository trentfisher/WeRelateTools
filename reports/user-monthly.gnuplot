set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set title "Active Users (monthly)"
plot 'tot-monthly.csv' skip 1 using 1:2 with lines title "active users"