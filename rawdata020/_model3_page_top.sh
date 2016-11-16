sed '1d' predict_current.csv |sort -t, -k15 -r|awk -F ',' '{if($15>24)print $1}'|xargs -I xx grep xx user_url.csv|grep 'Add'|awk -F ',' '{print $1,$3}' OFS=","|sort|uniq -c

