sed '1d' predict_current.csv |sort -t, -k5 -r|head -${1}|awk -F ',' '{print $1}'|xargs -I xx grep xx user_url.csv|grep 'Add'|awk -F ',' '{print $1,$3}' OFS=","|sort|uniq -c

