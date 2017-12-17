#!/bin/bash

#if [ ! -d ./images ]
#then
#	mkdir ./images
#	cd ./images
#fi

ROOT=$PWD

mkdir -p ./images/Cross
mkdir -p ./images/Diamond
mkdir -p ./images/Disc
mkdir -p ./images/Square
mkdir -p ./images/Triangle
mkdir -p ./images/Octogon
mkdir -p ./images/Background

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
		c ) 	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Cross/cross$LADATE
			convert ./images/Cross/cross$LADATE -resize 28x28 ./images/Cross/cross$LADATE
			echo "\033[1Asnap cross$LADATE";;
		l )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Diamond/diamond$LADATE
			convert ./images/Diamond/diamond$LADATE -resize 28x28 ./images/Diamond/diamond$LADATE
			echo "\033[1Asnap diamond$LADATE";;
		d )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Disc/disc$LADATE
			convert ./images/Disc/disc$LADATE -resize 28x28 ./images/Disc/disc$LADATE
			echo "\033[1Asnap disc$LADATE";;
		s )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Square/square$LADATE
			convert ./images/Square/square$LADATE -resize 28x28 ./images/Square/square$LADATE
			echo "\033[1Asnap square$LADATE";;
		t )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Triangle/triangle$LADATE
			convert ./images/Triangle/triangle$LADATE -resize 28x28 ./images/Triangle/triangle$LADATE
			echo "\033[1Asnap triangle$LADATE";;
		o )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Octogon/octogon$LADATE
			convert ./images/Octogon/octogon$LADATE -resize 28x28 ./images/Octogon/octogon$LADATE
			echo "\033[1Asnap octogon$LADATE";;
		b )	raspistill -t 900 -e png -h 720 -w 720 -ex auto -awb auto -o ./images/Background/background$LADATE
			convert ./images/Background/background$LADATE -resize 28x28 ./images/Background/background$LADATE
			echo "\033[1Asnap background$LADATE";;
	esac
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

cd ../
