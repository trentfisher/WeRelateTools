load "gnuplot-common"

set datafile separator ","

stats 'user-thismonth.csv' using 2 skip 1

binwidth = STATS_max/20
set boxwidth (binwidth*.95)
bin(x,width)=width*floor(x/width) + width/2.0

set style fill solid
set title "Page edits per user"
set ylabel "users"
set xlabel "edits"
plot 'user-thismonth.csv' skip 1 using (bin($2,binwidth)):(1.0) smooth freq with boxes title ""