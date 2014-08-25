#!/bin/bash

declare -a memories
declare -a cpus
memories=(1024m 2048m 3072m 4096m)
cpus=(1 2 3 4)
command=$1
matrix_size=$2
image="ubuntu_python"
echo "Creating random matrix for test"
cd ../application;python matrix.py $matrix_size
echo "Matrix generated"
cd ../learning/

for i in {1};
do

    for memory in "${memories[@]}";
    do
      for cpu in "${cpus[@]}";
      do
        # put process number to script
        #process=$cpu

        for process in {1..4};
        do
          echo calculate memory: $memory cpu: $cpu process: $process
          echo time timeout 5m $command $matrix_size $process >../application/script
          #echo time $command $matrix_size $process > ../application/script

          cd ../application
          (docker run -i -v `pwd`:/Final --rm -m $memory --cpuset=0-$(($cpu-1)) -w /Final  $image bash script) 2> tmp
          #(bash script)  2> tmp #for host running

          real_time_str=`cat tmp| head -n 2| tail -n 1`
          cd ../learning

          echo $cpu $memory $process $real_time_str >> statistics
        done;
      done;

    done;
done;

# run python script to parse the statistics file and generate the table
echo "learning is finished"
#python parse.py "$command $matrix_size"

rm -f ../application/tmp
rm -f ../application/script
#rm -f statistics


