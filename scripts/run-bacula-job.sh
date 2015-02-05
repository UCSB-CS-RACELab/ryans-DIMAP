#!/bin/bash

#
# Bash script that runs the bacula job with the given name and returns the job id if the job has been scheduled. 
# Author: Ryan Halbrook
#

jobid=' '
jflag=false

while getopts "j:" opt; do
    case $opt in
    j) jflag=true; jobid=$OPTARG ;; # Handle -j
    \?) echo "Usage: $0 [-j] job-id" ; exit 1 ;;#Handle error.
    esac
done

if ! $jflag
then
    echo "-j must be included to specify a job"
    exit 1
fi

# Sanity check to avoid overwriting the file do_backup_script.
if [ -f do_backup_script ]
then
    echo 'Please remove or rename do_backup_script file before running this script'
    exit 1
fi

echo $'run job='$jobid$'\nyes\nquit\n' >> do_backup_script

qid=`/usr/sbin/bconsole < do_backup_script | grep 'Job queued. JobId='`
echo "${qid//[!0-9]}"
rm do_backup_script

