#! /bin/bash

for infile in */*.asm; do
    cmpfile=$(echo $infile | sed s/'.asm'/'.hack'/)
    
    if [ -s $cmpfile ]; then

	outfile=$(basename $infile .asm).hack

	./Assembler.py $infile $outfile
	foo=$(diff $cmpfile $outfile)
	if [ ! -z $foo ]; then
	    echo "input/output files differ! $infile"
	else
	    echo "Success for $infile"
	fi
    fi
done
