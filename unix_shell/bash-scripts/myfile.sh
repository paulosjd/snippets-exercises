#!/bin/bash
# A simple demonstration of using backticks

echo The number of lines in the file $1 is $(cat $1 | wc -l)