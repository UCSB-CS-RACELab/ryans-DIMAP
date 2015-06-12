#!/bin/bash

if [[ $# -ne 1 ]] ; then 
    echo 'Usage Error'
    exit 1
fi

IP=$1
IPD=${IP//./-}
echo $IPD

echo "euca-${IPD}.eucalyptus.race.cs.ucsb.edu ${IP}" >> /etc/hosts

echo "${IP} euca-${IPD}.eucalyptus.race.cs.ucsb.edu" >> /etc/hosts

KEY_FILE='/home/ec2-user/backup_service_0.2/backuptest.key'
res=`ssh -o 'StrictHostKeyChecking no' -t -i $KEY_FILE ec2-user@$IP sudo echo 'Connected'`
echo $res

