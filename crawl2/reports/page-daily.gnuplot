# NOTE: filename must be specified on the command line
set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d"
set format x "%m-%d"
set yrange [0:]
set title "Page activity (daily)"
plot \
 filename skip 1 using 1:3 with lines title "active pages", \
 filename skip 1 using 1:4 with lines title "edits", \
 filename skip 1 using 1:5 with lines title "new pages", \
 filename skip 1 using 1:6 with lines title "total pages" axes x1y2
