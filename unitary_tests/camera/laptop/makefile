CC=g++
CFLAGS+=-Wall
#CFLAGS+=`pkg-config --cflags opencv`
LDFLAGS=`pkg-config --libs opencv`
PROG=camera
OBJS=$(PROG).o

.PHONY: all clean

$(PROG): $(OBJS)
	$(CC) -o $(PROG) $(OBJS) $(LDFLAGS)

%.o: %.cpp
	$(CC) -c $(CFLAGS) $<

all: $(PROG)

clean:
	rm -f *.o $(PROG)
