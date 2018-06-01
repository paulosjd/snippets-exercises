#!/bin/bash
if [ $1 = 1 ]
then
	echo "$1st"
fi
if [ $1 = 2 ]
then	
	echo "$1nd"
fi
if [ $1 -gt 2 ] && [ $1 -lt 10 ]
then	
	echo "$1rd"
fi
if [ $1 = 0 ] || [ $1 -gt 10 ]
then	
	echo "please enter number between 1 and 9"
fi