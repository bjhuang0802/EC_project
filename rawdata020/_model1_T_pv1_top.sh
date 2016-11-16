sed '1d' predict_current.csv |sort -t, -k15 -r|head -${1}|awk -F ',' '{print $1}'|xargs -I xx _user_page.sh xx|sort
