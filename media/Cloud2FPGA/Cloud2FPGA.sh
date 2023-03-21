#!/bin/bash
JOB_ID=$(head -n 1 job_id.txt)
if (($JOB_ID == 0)) ; then
    python sync.py &
    job_id=$!
    echo $job_id > job_id.txt
    echo 'Running sync.py'
else 
    echo 'Shutting down sync.py'
    kill -9 $JOB_ID
    echo '0' > job_id.txt
fi