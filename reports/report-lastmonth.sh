#!/bin/sh

rpttype=lastmonth
if [ "$1" ]
then
    rpttype=$1
    shift
fi

# get some numbers for the month
startmonth=`awk -F, '/TOTAL/ {print $2}' tot-$rpttype.csv`
endmonth=`awk -F, '/TOTAL/ {print $3}' tot-$rpttype.csv`
count_users=`awk -F, '/TOTAL/ {print $4}' tot-$rpttype.csv`
count_pages=`awk -F, '/TOTAL/ {print $5}' tot-$rpttype.csv`
count_edits=`awk -F, '/TOTAL/ {print $6}' tot-$rpttype.csv`
count_new=`awk -F, '/TOTAL/ {print $7}' tot-$rpttype.csv`
count_new_persons=`awk -F, '/Person/ {print $7}' tot-$rpttype.csv`

count_newusers=`cat user-new-$rpttype.csv | wc -l` 
newusers=`cat user-new-$rpttype.csv`

cat <<EOF

Here is the activity in WeRelate for the month ($startmonth to $endmonth):

There were $count_users active users
making $count_edits edits to $count_pages pages (Person and Family)
of those pages, $count_new ($count_new_persons Person) of them were newly created.

There were $count_newusers people who joined WeRelate this month:

$newusers

Here is a chart of the daily activity: page-daily-$rpttype.png

EOF

