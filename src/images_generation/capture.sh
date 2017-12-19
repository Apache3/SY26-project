#!/bin/bash

BASEFOLDER=$PWD
cd ../../
ROOT=$PWD

mkdir -p $ROOT/images/Cross
mkdir -p $ROOT/images/Diamond
mkdir -p $ROOT/images/Disc
mkdir -p $ROOT/images/Square
mkdir -p $ROOT/images/Triangle
mkdir -p $ROOT/images/Octogon
mkdir -p $ROOT/images/Background

clean()
{
	rm $ROOT/images/Cross/*
	rm $ROOT/images/Diamond/*
	rm $ROOT/images/Disc/*
	rm $ROOT/images/Square/*
	rm $ROOT/images/Triangle/*
	rm $ROOT/images/Octogon/*
	rm $ROOT/images/Background/*
	echo "folders are now empty"
}

instructions()
{
	echo "\"c\" for Cross"
	echo "\"d\" for Disc"
	echo "\"l\" for Diamond (losange)"
	echo "\"s\" for Square"
	echo "\"t\" for Triangle"
	echo "\"o\" for Octogon"
	echo "\"b\" for Background"
	echo ""
	echo "\"clean\" to clean all"
	echo "\"x\" to quit"
}

snap()
{
	LADATE=$(date +_%m%d%H%M%S).png
	case $1 in
		c ) python $BASEFOLDER/sale.py $ROOT/images/Cross/Cross$LADATE
			#convert $ROOT/images/Cross/Cross$LADATE -resize 96x54 $ROOT/images/Cross/Cross$LADATE
			echo "\033[1Asnap cross$LADATE";;
		l )	python $BASEFOLDER/sale.py $ROOT/images/Diamond/Diamond$LADATE
			#convert $ROOT/images/Diamond/Diamond$LADATE -resize 96x54 $ROOT/images/Diamond/Diamond$LADATE
			echo "\033[1Asnap diamond$LADATE";;
		d )	python $BASEFOLDER/sale.py $ROOT/images/Disc/Disc$LADATE
			#convert $ROOT/images/Disc/Disc$LADATE -resize 96x54 $ROOT/images/Disc/Disc$LADATE
			echo "\033[1Asnap disc$LADATE";;
		s )	python $BASEFOLDER/sale.py $ROOT/images/Square/Square$LADATE
			#convert $ROOT/images/Square/Square$LADATE -resize 96x54 $ROOT/images/Square/Square$LADATE
			echo "\033[1Asnap square$LADATE";;
		t )	python $BASEFOLDER/sale.py $ROOT/images/Triangle/Triangle$LADATE
			#convert $ROOT/images/Triangle/Triangle$LADATE -resize 96x54 $ROOT/images/Triangle/Triangle$LADATE
			echo "\033[1Asnap triangle$LADATE";;
		o )	python $BASEFOLDER/sale.py $ROOT/images/Octogon/Octogon$LADATE
			#convert $ROOT/images/Octogon/Octogon$LADATE -resize 96x54 $ROOT/images/Octogon/Octogon$LADATE
			echo "\033[1Asnap octogon$LADATE";;
		b )	python $BASEFOLDER/sale.py $ROOT/images/Background/Background$LADATE
			#convert $ROOT/images/Background/Background$LADATE -resize 96x54 $ROOT/images/Background/Background$LADATE
			echo "\033[1Asnap background$LADATE";;
	esac
	#raspistill -t 900 -e png -h 1080 -w 1920 -ex auto -awb auto -o $ROOT/images/Background/background$LADATE
}

addBaseImages()
{
	cp -r $ROOT/old_image_data/images/* $ROOT/images
}

instructions

while(true)
do
	read input
	case $input in
		x ) break  ;;
		c ) snap c ;;
		l ) snap l ;;
		d ) snap d ;;
		s ) snap s ;;
		t ) snap t ;;
		o ) snap o ;;
		b ) snap b ;;
		clean ) clean;;
		* ) instructions;;
	esac
done

addBaseImages

cd ../
