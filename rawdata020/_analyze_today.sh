#_download_data.sh 1009
#cat www*_020.log >2501.log
#cat www*_030.log >>2501.log
wc -l www_25-01_com_2016*_*.log
cat 2501.log |jq -r '"\(.session.fid),\(.gtm.urlCurrent)"'|grep 'utm' >utm_landing.csv
echo 'No of clicks:'
wc -l utm_landing.csv
#cat utm_landing.csv
echo ''
echo 'statistics:'
echo '1. unique campaign'
cat utm_landing.csv|awk -F '=' '{print $NF}'|sort|uniq -c|awk '{if($1>2)print $0}'
echo ''
echo '2. unique user'
cat utm_landing.csv|awk -F ',' '{print $1}'|sort|uniq |nl|tail -1|awk '{print $1}'
echo ''
echo '3. purchase'
cat 2501.log|jq -rc '.|select(.gtm.event == "Purchase")'|jq -rc '"\(.session.fid),\(.gtm.purchase.transactionProducts)"'|wc -l
#cat purchased_list.csv
