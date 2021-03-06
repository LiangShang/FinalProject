#!/bin/bash

declare -a memories
declare -a cpus
memories=(2048m 3096m)
cpus=(2 4 6 8)
command="time python matrix_mul_random" 
image="ubuntu_python"

    for memory in "${memories[@]}";
    do
      for cpu in "${cpus[@]}";
      do
        # put process number to script
        process=$cpu
        echo calculate memory: $memory cpu: $cpu
        #echo time $command $matrix_size $process > ../application/script

        cd ../application
        echo \( time python matrix_mul_random $cpu  \)
        docker run -v `pwd`:/Final --rm -m $memory --cpuset=0-$(($cpu-1)) -w /Final  $image bash online_application.sh $cpu


        real_time_str=`cat tmp| head -n 2| tail -n 1`
        cd ../learning

        echo $cpu $memory $real_time_str >> statistics

      done;

    done;

# run python script to parse the statistics file and generate the table
echo "learning is finished"
#rm -f statistics


