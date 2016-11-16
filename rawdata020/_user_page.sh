grep $1 user_url.csv |awk -F ',' '{print $3,$4}' OFS=","|sort|uniq -c|sort
