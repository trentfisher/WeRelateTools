# NOTE: filename must be specified on the command line
load "gnuplot-common"
set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d"
set format x "%m-%d"
set yrange [0:]
set y2tics
set ytics nomirror
set xtics nomirror
set ylabel "pages"
set y2label "users"
set title "Person/Family page activity (daily)"
plot \
 filename skip 1 using 1:3 with lines linewidth 2 title "active pages", \
 filename skip 1 using 1:4 with lines linewidth 2 title "edits", \
 filename skip 1 using 1:5 with lines linewidth 2 title "new pages", \
 filename skip 1 using 1:2 with fsteps title "active users" axis x1y2
