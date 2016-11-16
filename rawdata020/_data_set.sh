#_download_data.sh 1027
work='/home/ubuntu/2501/rawdata020/'
pool="${work}data_pool"
export TZ='Asia/Taipei'
cat ${work}*_020.log|grep -v '32490f0e05d0d693d0da8d518e76ae60' >${work}2501_current.log
cat ${work}*_030.log|grep -v '32490f0e05d0d693d0da8d518e76ae60'  >>${work}2501_current.log
cat ${work}*_040.log|grep -v '32490f0e05d0d693d0da8d518e76ae60'  >>${work}2501_current.log
cat ${work}*_050.log|grep -v '32490f0e05d0d693d0da8d518e76ae60'  >>${work}2501_current.log
cat ${pool}/2501_OCT.log > ${work}2501.log
cat ${work}2501_current.log >> ${work}2501.log
data_current="${work}2501_current.log"
data="${work}2501.log"
#echo 'fid,time,member,ref_cam,cur_cam,event,productid,purchase' >dataset_current.csv
echo "Parsing data to dataset." 
cat ${data_current} |/usr/bin/jq -r '"\(.session.fid),\(.general.ts),\(.gtm.member?),\(if .gtm.urlReferrer|test("utm") then "\(.gtm.urlReferrer|split("campaign=")|.[1])" else "0" end),\(if .gtm.urlCurrent|test("utm") then "\(.gtm.urlCurrent|split("campaign=")|.[1])" else "0" end),\(.gtm.event?),\(if .gtm.event == "ViewContent" then .gtm.product.id|split("&")|.[0]? else "0" end),\(if .gtm.event == "Purchase" then "2" else "1" end)"'|sort -t, -k1 -k2 -g|awk -F ',' '{if($3 == "null") printf("%s,%s,%s,%s,%s,%s,%s,%s\n",$1,$2,-1,$4,$5,$6,$7,$8); else print $0;}'|sed 's/null/-1/g'|sed 's/index/-1/g'|tr -d ' '>${work}tmp1.csv
grep '&' ${work}tmp1.csv |awk -F ',' '{if($4==0)print $0}'|awk -F '[,&]' '{print $1,$2,$3,$4,$5,$7,$8,$9}' OFS=',' >${work}v1.csv
grep '&' ${work}tmp1.csv |awk -F ',' '{if($5==0)print $0}'|awk -F '[,&]' '{print $1,$2,$3,$4,$6,$7,$8,$9}' OFS=',' >${work}v2.csv
#grep -v '&' tmp1.csv |grep -v '%'>v3.csv
grep -v '&' ${work}tmp1.csv >${work}v3.csv
cat ${work}v*.csv|sort -t, -k2 -g >${work}dataset_current.csv
rm ${work}v*.csv
cat ${pool}/dataset_OCT.csv >${work}dataset.csv
cat ${work}dataset_current.csv >>${work}dataset.csv
echo 'productid,counts'>${work}uniq_campaign_target_product.txt
cat ${work}dataset.csv |grep 'View'|grep -v '0,0,View' |awk -F ',' '{print $7}' |sort |uniq -c|awk '{print $2,$1}' OFS=","|sort -t, -k2 -g>>${work}uniq_campaign_target_product.txt
cat ${work}dataset.csv |grep 'View'|grep -v '0,0,View' |awk -F ',' '{if($4==0)print $5}' >${work}uniq_campaign_tmp.txt
cat ${work}dataset.csv |grep 'View'|grep -v '0,0,View' |awk -F ',' '{if($5==0)print $4}' >>${work}uniq_campaign_tmp.txt
cat ${work}uniq_campaign_tmp.txt|sort|uniq -c |sort>${work}uniq_campaign.txt
echo 'Finish uniq_campaign.'

#echo 'fid,time,productid,quantity,price' >Purchased_list.csv
grep 'event":"Purchase' $data_current |/usr/bin/jq -r '"\(.session.fid),\(.general.ts),\(.gtm.purchase.transactionProducts|keys[] as $k |"\(.[$k].id?),1,\(.[$k].price?|sub(",";"")?)")"' |grep -v 'null' >${work}Purchased_list_current.csv
cat ${pool}/Purchased_list_OCT.csv >${work}Purchased_list.csv
cat ${work}Purchased_list_current.csv >>${work}Purchased_list.csv
echo 'Finish Purchased_list.'

#echo 'fid,time,productid,price,recommendedPrice' >add_to_cart_list.csv
grep 'event":"AddToCart' $data_current |/usr/bin/jq -r '"\(.session.fid),\(.general.ts),\(.gtm.product|"\(.id?),\(.price?|sub(",";"")?),\(.price_recommend|sub(",";"")?)")"' |grep -v 'null'|grep -v 'index' > ${work}add_to_cart_list_current.csv
cat ${pool}/add_to_cart_list_OCT.csv >${work}add_to_cart_list.csv
cat ${work}add_to_cart_list_current.csv >>${work}add_to_cart_list.csv
echo 'Finish add_to_cart_list.'

echo 'productid,name'>${work}2501_product_list.csv
cat $data|/usr/bin/jq -r '.|select(.gtm.event == "ViewContent")'|/usr/bin/jq -r '.gtm.product|"\(.id?),(NT\(.price?|sub(",";"")?)\(.name?)"'|grep -v 'null'|sort|uniq |tr -d ' '|grep -v '(NT)'|grep ','>>${work}2501_product_list.csv
#cat $data|/usr/bin/jq -r '.|select(.gtm.event == "ViewContent")'|/usr/bin/jq -r '.gtm.product|"\(.id?),(NT\(.price?|sub(",";"")?|sub("$";"")?|sub("T";"")?)\(.name?)"'|grep -v 'null'|sort|uniq |tr -d ' '|grep -v '(NT)'|grep ','>>${work}2501_product_list.csv
#cat purchased_list.csv|awk -F ',' '{print $3}'|sort |uniq -c |awk '{print $2,$1}' OFS="," >selling_pid_counts.csv
cat $data_current|/usr/bin/jq -r '"\(.session.fid),\(.general.ts),\(.gtm.urlCurrent|split("?")|"\(.[0]),\(if .[1] then "\(if .[1]|test("utm") then .[1] else "0" end)"  else "0" end)"),\(.gtm.event)"'|sed 's/null/0/g'|sed 's/https/http/g'|sort -t, -k1 -k2 >${work}input_current.csv
cat ${pool}/input_OCT.csv >${work}tmp.csv
cat ${work}input_current.csv >>${work}tmp.csv
cat ${work}tmp.csv |sort -t, -k1 -k2 >${work}input.csv

echo 'create user_url.csv'
python ${work}urlset.py
echo 'create session input'
php ${work}session.php
echo 'Finish session calculation'
cat ${work}output.csv |sed '1d'|sort -t, -k1 -k2 -g |awk -F ',' '{print $1,$2,$3,$4}' OFS="," >${work}session_sort.csv
#rm input.csv
#rm output.csv
#cat session_sort.csv |awk -F ',' '{print $2}'|sort |toRT.sh |awk -F '/' '{print $1}' |uniq -c |awk '{print $2,$1}' OFS=",">no_sessions_by_day.txt
python ${work}gen_pv_addtocart_buy.py
echo 'Generate pv_addtocart_pbuy.json'
sed '1s/# //' ${work}../predict_keras.csv >${work}predict_keras.csv
python ${work}svm_tomorrow.py
echo 'Predict current customer behavior, to user.json'
#_analyze_today.sh
#echo 'Analyze today'
echo 'Done.'
