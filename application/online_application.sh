

for line in {1..100}
do
  a=$(((RANDOM%4)*2+2))  #$1
  b=$(((RANDOM%500)+1001))
  echo $a $b >> throughput
  echo $line
  echo ./mandelbrot_set $a $b >> online_record
  (time ./mandelbrot_set $a $b) 2>tmp   
  head -n 2 tmp | tail -n 1 >> throughput
done
