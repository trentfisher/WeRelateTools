# generate a small sparkline graph

set datafile separator ","
filename='tot-thismonth-daily.csv'
column=2

set terminal pngcairo size 100,30
set output '/dev/stdout'

unset key                   # Turn off the legend
unset tics                  # Turn off the tics (axis markers)
unset border                # Turn off the border

set style line 1 lc rgb '#007700' lw 2  # Line style for the plot

plot filename using column with lines linestyle 1

set output   # close output
