# generate a small sparkline graph

set datafile separator ","

set terminal pngcairo size 100,30 transparent
set output '/dev/stdout'

unset key                   # Turn off the legend
unset tics                  # Turn off the tics (axis markers)
unset border                # Turn off the border

# reduce the margins
set lmargin 0.5
set rmargin 0.5
set tmargin 0.5
set bmargin 0.5

set style line 1 lc rgb '#007700' lw 2  # Line style for the plot

stats filename skip 1 nooutput

plot filename using column skip 1 every ::(STATS_records>numpoints ? STATS_records-numpoints : 0) with lines linestyle 1

set output   # close output
