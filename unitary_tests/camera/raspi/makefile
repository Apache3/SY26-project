CC=g++
CFLAGS+=-Wall -I/usr/local/include/
CFLAGS+=`pkg-config --cflags opencv`
LDFLAGS+=`pkg-config --libs opencv` -lraspicam -lraspicam_cv
PROG=camera
OBJS=$(PROG).o

.PHONY: all clean

$(PROG): $(OBJS)
	$(CC) -o $(PROG) $(OBJS) $(LDFLAGS)

%.o: %.cpp
	$(CC) -c $(CFLAGS) $<

all: $(PROG)

clean:
	rm -f $(OBJS) $(PROG)
