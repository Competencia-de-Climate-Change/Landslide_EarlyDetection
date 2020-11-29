#!/bin/bash
echo "Creating positive data..."
for i in {0..50} 
do
  python3 parallel_positive_chirps.py $i
  python3 parallel_positive_cfs.py $i
  python3 parallel_positive_gsod.py $i
  echo "Done part number $i..."
done
echo "Done"

