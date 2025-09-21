set datafile separator ","
set xdata time
set timefmt "%Y-%m"
set format x "%Y"
set yrange [0:20000]
set title "Active Users (monthly)"
plot 'tot-monthly.csv' skip 1 using 1:2 with lines title "active users", \
 'tot-monthly.csv' skip 1 using 1:3 with lines title "active pages", \
 'tot-monthly.csv' skip 1 using 1:4 with lines title "edits", \
 'tot-monthly.csv' skip 1 using 1:5 with lines title "new pages", \
 'tot-monthly.csv' skip 1 using 1:8 with lines title "score diff"