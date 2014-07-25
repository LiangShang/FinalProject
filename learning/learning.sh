#!/bin/bash

declare -a memories
declare -a cpus
memories=(512k 1024k 2048k 4096k)
cpus=(1 2 3 4)
command=$@
image="stackbrew/hipache"

echo time $command >script
for i in {1..10};
do

    for memory in "${memories[@]}";
    do
      for cpu in "${cpus[@]}";
      do
        #echo $memory, $cpu

        (sudo docker run -i -v `pwd`:/Final --rm -m $memory --cpuset=$cpu -w /Final  $image bash script) 2> tmp
        #(time $command)  2> tmp
        echo calculate memory: $memory cpu: $cpu
        #sys_time_str=`cat tmp|tail -1`
        #user_time_str=`cat tmp|tail -n 2| head -n 1`
        real_time_str=`cat tmp|tail -n 3| head -n 1`

        echo $cpu $memory $real_time_str >> statistics

      done;

    done;
done;

#TODO run python script to parse the statistics file and generate the table
python parse.py $command

rm -f tmp
rm -f script
rm -f statistics

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

