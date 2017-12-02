CC=g++
CFLAGS+=-Wall -I/usr/local/include/
#CFLAGS+=`- opencv -l boost_filesystem`
#CFLAGS+='pkg-config --cflags opencv'
CFLAGS+=-L boost
#LDFLAGS+=`pkg-config --libs opencv -l boost_filesystem` 
#LDFLAGS+=#`pkg-config --libs opencv boos` 
#LDFLAGS+=-L opencv boost_filesystem
PROG=boost_test
OBJS=$(PROG).o

.PHONY: all clean

$(PROG): $(OBJS)
	$(CC) -o $(PROG) $(OBJS) 
	#$(LDFLAGS)

%.o: %.cpp
	$(CC) -c $(CFLAGS) $<

all: $(PROG)

clean:
	rm -f $(OBJS) $(PROG)
