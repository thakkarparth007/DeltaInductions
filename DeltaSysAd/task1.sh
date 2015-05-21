#!/bin/bash

if [ "$#" -ne 1 ]; then
cat <<-EOF
	*******************************************************
	Delta Task 1:
	*******************************************************
	This script expects exactly 1 parameter - the directory
	in which the 100 folders must be created. Note that the 
	script will give an error in case the directory given
	as the parameter doesn't exist. You must create the directory
	first.
	EOF
else
	cd $1
	mkdir ./folder{1..100}
	for i in {1..10}; do
		touch "./folder"$i"/folder"$i".txt"
		chmod 700 "./folder"$i"/folder"$i".txt"
	done
fi
