#!/bin/bash

declare -a memories
declare -a cpus
memories=(10m 20m 30m 40m)
#memories=(200 250 300 350)  #for host statistics, memory stands for matrix size
cpus=(1 2 3 4)
command=$1
matrix_size=$2
image="stackbrew/hipache"
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
        #if [ $process -lt 1 ];then 
         #    process=1 
        #fi
        echo calculate memory: $memory cpu: $cpu
        echo time timeout 1m $command matrix_$matrix_size matrix_$matrix_size $process >script
        #echo time $command $memory $process >script #for host running
        (sudo docker run -i -v `pwd`:/Final --rm -m $memory --cpuset=0-$(($cpu-1)) -w /Final  $image bash script) 2> tmp
        #(bash script)  2> tmp #for host running
        #sys_time_str=`cat tmp|tail -1`
        #user_time_str=`cat tmp|tail -n 2| head -n 1`
        real_time_str=`cat tmp| head -n 2| tail -n 1`

        echo $cpu $memory $real_time_str >> statistics

      done;

    done;
done;

# run python script to parse the statistics file and generate the table
echo $command
python parse.py $command$matrix_size

rm -f tmp
rm -f script
#rm -f statistics

    #parse xxmxxxxs to time(seconds)
    #sys_time_str=`echo $sys_time_str | cut -d ' ' -f 2`
    #sys_time_minute=`echo $sys_time_str | cut -d 'm' -f 1`
    #echo $sys_time_minute
    #sys_time_second=`echo $sys_time_str | cut -d 'm' -f 2`
    #sys_time_second=`echo $sys_time_second | cut -d 's' -f 1`
    #echo $sys_time_second

    #user_time_str=`echo $user_time_str | cut -d ' ' -f 2`
    #user_time_minute=`echo $user_time_str | cut -d 'm' -f 1`
    #echo $sys_time_minute
    #user_time_second=`echo $user_time_str | cut -d 'm' -f 2`
    #user_time_second=`echo $user_time_second | cut -d 's' -f 1`
    #echo $user_time_second

