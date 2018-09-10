#!/usr/bin/env bash
mkdir -p /tmp/delete/logs
deletionTargets=$1
N_JOBS=10

echo "Using ${deletionTargets} for deletion"



i=0
for f in `cat ${deletionTargets}`
  do
    echo "Deleting ${f}"
    mkdir -p /tmp/delete/logs/$f
    nohup gfal-rm -r gsiftp://lcgse01.phy.bris.ac.uk$f &> /tmp/delete/logs/$f.log &
    let i+=1
    if (( $i % N_JOBS == 0 ))
    then
      echo "Waiting for the above to finish"
      wait;
    fi
done

wait;
echo "All done!"

