#!/bin/bash
echo "Creating negative data..."
for i in {0..36}
do
  python3 parallel_negative_chirps.py $i
  python3 parallel_negative_cfs.py $i
  python3 parallel_negative_gsod.py $i
  echo "Done part number $i..."
done
echo "Done"

