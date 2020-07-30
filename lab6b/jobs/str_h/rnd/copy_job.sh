# Copy job.sh files to each FP directory

n=20
for i in `seq -f "%05g" $n`
do
  cd $i
    scp ../job.sh .
  cd ..
done
