#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "Please insert — rebuild or— render [categoryId]"
else
	if [ $1 = "--rebuild" ]; 
	then exec python db.py
	elif [ $1 = "--render" ]; 
		then exec python html.py $2
	fi
fi


