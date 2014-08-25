#!/bin/bash

declare -a memories
declare -a cpus
memories=(4g 8g 16g)
#memories=(30m 40m 75m 150m 300m)
dfes=(1 2 3 4)
command=$1  # ./Adp_dfe
problem_size=$2  #1000
image="ubuntu_ib"

for i in {1..3};
do

    for memory in "${memories[@]}";
    do
      for cpu in "${dfes[@]}";
      do
        # put process number to script
        process=$cpu
        echo calculate memory: $memory cpu: $cpu
        echo docker run --rm -v /opt/maxeler:/opt/maxeler -v /dev/infiniband/:/dev/infiniband -v /mnt/data/cccad3/jgfc:/mnt/data/cccad3/jgfc --cpuset=0 --privileged=true -w /mnt/data/cccad3/jgfc/liang/AdPredictorDFE-MAIA/build/  $image  /bin/bash -c \'source /setmaia\;$command \"-n\" $cpu $problem_size\' > script
        chmod 777 script
        ./script 2>tmp 1>/dev/null 

        real_time_str=`cat tmp| head -n 1`

        echo $cpu $memory $real_time_str >> statistics

      done;

    done;
done;

# run python script to parse the statistics file and generate the table
echo "learning is finished"
python dfe_parse.py "$command $problem_size"

rm tmp
rm -f script
rm -f statistics


