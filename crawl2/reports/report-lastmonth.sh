#!/bin/sh

rpttype=lastmonth
if [ "$1" -a -f tot-$1.sql ]
then
    rpttype=$1
    shift
fi

# get some numbers for the month
startmonth=`awk -F, 'NR==2 {print $1}' tot-$rpttype.csv`
endmonth=`awk -F, 'NR==2 {print $2}' tot-$rpttype.csv`
count_users=`awk -F, 'NR==2 {print $3}' tot-$rpttype.csv`
count_pages=`awk -F, 'NR==2 {print $4}' tot-$rpttype.csv`
count_edits=`awk -F, 'NR==2 {print $5}' tot-$rpttype.csv`
count_new=`awk -F, 'NR==2 {print $6}' tot-$rpttype.csv`

count_newusers=`cat user-new-$rpttype.csv | wc -l` 
newusers=`cat user-new-$rpttype.csv`

cat <<EOF

Here is the activity in WeRelate for the month ($startmonth to $endmonth):

There were $count_users active users
making $count_edits edits to $count_pages pages (Person and Family)
of those pages, $count_new of them were newly created.

There were $count_newusers people who joined WeRelate this month:

$newusers

Here is a chart of the daily activity: page-daily-$rpttype.png

EOF

