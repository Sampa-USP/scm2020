# Submit jobs from n directories

n=20
for i in `seq -f "%05g" $n`
do
  cd $i
    if [ -e 01.out ]
	then
		echo $i		
	else
		source job.sh
		sleep 15
		echo $i
	fi
  cd ..
done
