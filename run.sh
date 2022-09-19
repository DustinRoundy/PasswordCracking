#!/bin/bash

while $True:
do
	echo "Try a password to crack!"
	echo "Use only lowercase letters, and keep it to 7 characters max!"
	read -p "Enter a password to crack: " password
	python3 final.py $password -t 8
	sleep 5
	clear
done
