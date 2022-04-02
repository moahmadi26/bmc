#!/bin/bash

rm -f constraintst.smt
rm -f graph.g

for ((i=0; i<=$1; i++));
do
	#python3 bmc_yeast.py examples/yeast_polarization.py $i 1
	time python3 bmc_yeast_2.py examples/yeast_polarization_2.py $i 1

done
