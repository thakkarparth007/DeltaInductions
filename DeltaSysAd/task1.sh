#!/bin/bash

cd $1
mkdir ./folder{1..100}
for i in {1..10}; do
	touch "./folder"$i"/folder"$i".txt"
	chmod 600 "./folder"$i"/folder"$i".txt"
done
