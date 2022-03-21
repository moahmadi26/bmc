#!/bin/bash

rm -f constraintst.smt
rm -f graph.g

for ((i=0; i<=$1; i++));
do
	python3 bmc_6_prob.py six_rn_prob.py $i 1

done
