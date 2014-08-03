#!/bin/bash

declare -a memories
declare -a cpus
memories=(10m 20m 30m 40m 75m 150m)
cpus=(1 2 3 4)
command=$1
matrix_size=$2
image="ubuntu_python"
echo "Creating random matrix for test"
python matrix.py $matrix_size
echo "Matrix generated"

for i in {1};
do

    for memory in "${memories[@]}";
    do
      for cpu in "${cpus[@]}";
      do
        # put process number to script
        process=$cpu
        echo calculate memory: $memory cpu: $cpu
        echo time timeout 1m $command $matrix_size $process >script
        #echo time $command $matrix_size $process >script
        (docker run -i -v `pwd`:/Final --rm -m $memory --cpuset=0-$(($cpu-1)) -w /Final  $image bash script) 2> tmp
        #(bash script)  2> tmp #for host running
        real_time_str=`cat tmp| head -n 2| tail -n 1`

        echo $cpu $memory $real_time_str >> statistics

      done;

    done;
done;

# run python script to parse the statistics file and generate the table
echo "learning is finished"
python parse.py "$command $matrix_size"

rm -f tmp
rm -f script
rm -f statistics


