CC=g++
CFLAGS+=-Wall -I/usr/local/include/
#CFLAGS+=`- opencv -l boost_filesystem`
#CFLAGS+='pkg-config --cflags opencv'
CFLAGS+=-L opencv -L ../boost_1_65_1/stage/lib/ -lboost_filesystem -lboost_system
#LDFLAGS+=`pkg-config --libs opencv -l boost_filesystem` 
LDFLAGS+=`pkg-config --libs opencv boost` 
#LDFLAGS+=-L opencv boost_filesystem
PROG=database_generation
OBJS=$(PROG).o

.PHONY: all clean

$(PROG): $(OBJS)
	$(CC) -o $(PROG) $(OBJS) $(LDFLAGS)

%.o: %.cpp
	$(CC) -c $(CFLAGS) $<

all: $(PROG)

clean:
	rm -f $(OBJS) $(PROG)
