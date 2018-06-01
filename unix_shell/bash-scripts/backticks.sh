#!/bin/bash
# A simple demonstration of using backticks
# Ryan 17/3/2018
 
lines=`cat $1 | wc -l`
echo The number of lines in the file $1 is $lines