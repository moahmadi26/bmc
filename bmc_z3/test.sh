#!/bin/bash

rm -f constraintst.smt
rm -f graph.g

for ((i=0; i<=$1; i++));
do
	#python3 bmc_yeast.py examples/yeast_polarization.py $i 1
	python3 bmc_tandem_scaf.py examples/tandem.py $i 1

done
