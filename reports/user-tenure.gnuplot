load "gnuplot-common"

set datafile separator ","

bin(x,s) = s*int(x/s)

binwidth = 1
set boxwidth binwidth
set style fill solid border -1

# hide the huge 0 bar
#set yrange [0:300]
set logscale y

# TBD increase this in a few years
set xrange[-1:20]

set title "user tenure (years)"
plot 'user-alltime.csv' skip 1 using (bin($8,binwidth)) smooth freq with boxes title ""
