#!/bin/bash

echo "Processing negative GSOD..."
for i in {0..74}
do
  python3 parallel_negative_gsod.py $i
  echo "Done part number $i..."
done
echo "Done GSOD"

