#!/bin/sh
alpgexe="alpg/profilegenerator.py"
if [ -f $alpgexe ]
then
	cd alpg
	python3 profilegenerator.py -c example -o demo --force 
else
	git clone https://github.com/GENETX/alpg.git
	cd alpg
	python3 profilegenerator.py -c example -o demo --force 
fi
