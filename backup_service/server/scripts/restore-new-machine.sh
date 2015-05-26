#!/bin/bash
# 
# Bash script that takes the job id of a Bacula backup and the IP address of a new machine with
# Bacula installed (but otherwise no Bacula setup) and restores all files from the backup job to the 
# 'new' machine. Right now they will go to the directory /tmp/bacula-restores (this is specified in my
# bacula-dir.conf).
# 
# Author: Ryan Halbrook
# Date:  2/17/2015
#

SERVICE_HOME='/home/ec2-user/backup_service'

CLIENT_IP=' '
KEY_FILE=$SERVICE_HOME/KEY_NAME.key
PWD=TEST_PWD

jobid=' '
jflag=false
mflag=false
while getopts "j:m:" opt; do
    case $opt in
    j) jflag=true; jobid=$OPTARG ;; # Handle -j
    m) mflag=true; CLIENT_IP=$OPTARG ;; # Handle -m
    \?) echo "Usage: $0 [-j] job-id [-m] ip-address" ; exit 1 ;;#Handle error.
    esac
done

if ! $jflag
then
    echo "-j must be included to specify a job"
    exit 1
fi

if ! $mflag
then
    echo "-m flag must be included to specify a machine"
        exit 1
fi

# Check if the Bacula Configuration file already exists on the client
# machine.
#ssh -i $KEY_FILE ec2-user@$CLIENT_IP ls /etc/bacula/

echo 'Setting up host information'
$SERVICE_HOME/server/scripts/updateHosts.sh $CLIENT_IP

echo -n 'Checking Pre-Existing Config File'

res=`ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo grep FD_PASSWORD /etc/bacula/bacula-fd.conf 2> /dev/null`
if [[ $res =~ .*FD_PASSWORD*. ]] 
then
	echo -e ' ... \x1b[32;01mDONE\x1b[39;49;00m'
else
	echo 'FAILED: A non-default Bacula configuration file exists on the client.'
	exit 1
fi

echo -n 'Making Config File               '
PWD=`openssl rand -base64 32 | sed -e 's:\/:-:g'`
cp $SERVICE_HOME/conf/bacula-fd.conf bacula-fd-temp.conf
sed -i -e 's/DIRECTOR_PASSWORD/'$PWD'/g' bacula-fd-temp.conf
sed -i -e 's/FD_NAME/'$CLIENT_IP'-fd/g' bacula-fd-temp.conf
echo -e ' ... \x1b[32;01mDONE\x1b[39;49;00m'


echo -n 'Copying Config File to Client    ' 
scp -q -i $KEY_FILE bacula-fd-temp.conf ec2-user@$CLIENT_IP:~/
ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo mv /home/ec2-user/bacula-fd-temp.conf /etc/bacula/bacula-fd.conf 2> /dev/null
echo -e ' ... \x1b[32;01mDONE\x1b[39;49;00m'


echo 'Restarting Bacula on Client      '
ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo service bacula-fd stop 2> /dev/null    # Should fail, but included just to be sure.
ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sleep 1 2> /dev/null
ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo service bacula-fd start 2> /dev/null


# Sanity check to avoid overwriting file do_restore_script.
if [ -f do_restore_script ]
then
    echo 'Please remove or rename do_restore_script file before running this script'
    exit 1
fi

echo 'Restarting Bacula Director'

# Stop Bacula
sudo service bacula-dir stop

# Add new client to Bacula's configuration
echo $'Client {\n\tName = '$CLIENT_IP$'-fd\n\tAddress = '$CLIENT_IP$'\n\tFDPort = 9102\n\tCatalog = MyCatalog\n\tPassword = "'$PWD$'"\n\tFile Retention = 30 days\n\tJob Retention = 6 months\n\tAutoPrune = yes\n}' >> /etc/bacula/bacula-dir.conf

# Start Bacula
sudo service bacula-dir start
sleep 1

echo    'Attempting Restore to '$CLIENT_IP  

# Run Bacula restore job.
echo $'restore all client='$CLIENT_IP$'-fd jobid='$jobid$'\ndone\nyes\nquit\n' >> do_restore_script



qid=`/usr/sbin/bconsole < do_restore_script | grep 'Job queued. JobId='`
echo "Restore Job ID = ${qid//[!0-9]}"
rm do_restore_script

sleep 3

ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo cp /home/ec2-user/home/ec2-user/* /home/ec2-user/
ssh -t -i $KEY_FILE ec2-user@$CLIENT_IP sudo rm -rf /home/ec2-user/home


