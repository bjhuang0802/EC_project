#scp -i ~/.ssh/masterdskey20160202.pem ec2-user@aws:/home/ec2-user/front/wuz/* .
name=`date +%m%d`
workdir=/home/ubuntu/2501/rawdata020
scp -i ~/.ssh/masterdskey20160202.pem ec2-user@aws:/home/ec2-user/tracker/data/www_25-01_com/www_25-01_com_2016${name}_040.log ${workdir}
scp -i ~/.ssh/masterdskey20160202.pem ec2-user@aws:/home/ec2-user/tracker/data/www_25-01_com/www_25-01_com_2016${name}_050.log ${workdir}
#scp -i ~/.ssh/masterdskey20160202.pem ec2-user@aws:/home/ec2-user/front/25-01/* .
