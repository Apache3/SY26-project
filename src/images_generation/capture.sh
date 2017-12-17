#!/bin/bash

BASEFOLDER=$PWD
cd ../../
ROOT=$PWD
cd BASEFOLDER

mkdir -p $ROOT/images/Cross
mkdir -p $ROOT/images/Diamond
mkdir -p $ROOT/images/Disc
mkdir -p $ROOT/images/Square
mkdir -p $ROOT/images/Triangle
mkdir -p $ROOT/images/Octogon
mkdir -p $ROOT/images/Background

clean()
{
	rm -f $ROOT/images/Cross/*
	rm -f $ROOT/images/Diamond/*
	rm -f $ROOT/images/Disc/*
	rm -f $ROOT/images/Square/*
	rm -f $ROOT/images/Triangle/*
	rm -f $ROOT/images/Octogon/*
	rm -f $ROOT/images/Background/*
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
	LADATE=$(date +_%m%d%H%M%S)
	case $1 in
		c ) 	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Cross/cross$LADATE
			convert $ROOT/images/Cross/cross$LADATE -resize 28x28 $ROOT/images/Cross/cross$LADATE
			echo "\033[1Asnap cross$LADATE";;
		l )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Diamond/diamond$LADATE
			convert $ROOT/images/Diamond/diamond$LADATE -resize 28x28 $ROOT/images/Diamond/diamond$LADATE
			echo "\033[1Asnap diamond$LADATE";;
		d )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Disc/disc$LADATE
			convert $ROOT/images/Disc/disc$LADATE -resize 28x28 $ROOT/images/Disc/disc$LADATE
			echo "\033[1Asnap disc$LADATE";;
		s )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Square/square$LADATE
			convert $ROOT/images/Square/square$LADATE -resize 28x28 $ROOT/images/Square/square$LADATE
			echo "\033[1Asnap square$LADATE";;
		t )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Triangle/triangle$LADATE
			convert $ROOT/images/Triangle/triangle$LADATE -resize 28x28 $ROOT/images/Triangle/triangle$LADATE
			echo "\033[1Asnap triangle$LADATE";;
		o )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Octogon/octogon$LADATE
			convert $ROOT/images/Octogon/octogon$LADATE -resize 28x28 $ROOT/images/Octogon/octogon$LADATE
			echo "\033[1Asnap octogon$LADATE";;
		b )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o $ROOT/images/Background/background$LADATE
			convert $ROOT/images/Background/background$LADATE -resize 28x28 $ROOT/images/Background/background$LADATE
			echo "\033[1Asnap background$LADATE";;
	esac
}

addBaseImages()
{
	cp ../../old_image_data/images/* ../../images/*
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
