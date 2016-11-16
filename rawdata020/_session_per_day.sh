cat session_sort.csv |awk -F ',' '{print $2}'|toRT.sh |awk -F '/' '{print $1}'|sort|uniq -c
