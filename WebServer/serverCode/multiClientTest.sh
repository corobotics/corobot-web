#!/bin/bash

if [ "$#" -ne 1 ]
then
echo "Usage: $0 '<number of robots>'"
exit 1
fi

for (( i=1 ;i <= $1 ; i++ ))
do
	python client.py "ROBOT$i" &
done
