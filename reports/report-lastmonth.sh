#!/bin/sh
#
# this script is for generating the monthly activity report for WeRelate
# by default it uses the numbers from the last complete month,
# but give it the parameter "thismonth" and it will show the information
# for the current (in-progress) month
#
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

sparkline_users=`gnuplot -e "filename='tot-$rpttype-daily.csv'; column=3" sparkline.gp  | base64 -w 0`

cat <<EOF1
---
title: WeRelate Monthly Activity Report
---

Here is the activity in WeRelate for the month ($startmonth to $endmonth):

There were $count_users active users
making $count_edits edits to $count_pages pages (Person and Family)
of those pages, $count_new ($count_new_persons Person) of them were newly created.

There were $count_newusers people who joined WeRelate this month:

Active users: <img src="data:image/png;base64,$sparkline_users" alt="sparkline"/> $count_users

EOF1

cat user-new-$rpttype.csv | while read u
do
    ec=`awk -F, '/'"$u"'/ {print $2}' user-$rpttype.csv`
    echo '* ['$u']('https://www.werelate.org/wiki/User:$u')' -- '['$ec edits']('https://www.werelate.org/wiki/Special:Contributions/$u')'
done

cat <<EOF2

Here is a chart of the daily activity:

![daily activity chart](page-daily-$rpttype.png)

EOF2

