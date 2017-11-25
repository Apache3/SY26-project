CC=g++
USER_LIB_PATH=../libs
LIBS=DatabaseGenerator
PROG=database_generation
CFLAGS=-I$(USER_LIB_PATH)
LDFLAGS+=`pkg-config --libs opencv boost` 

all:
	$(CC) -Wall -c $(USER_LIB_PATH)/$(LIBS).cpp
	$(CC) -Wall $(PROG).cpp -c $(CFLAGS)
	$(CC) -Wall -o $(PROG) $(PROG).o $(USER_LIB_PATH)/$(LIBS).cpp $(LDFLAGS)


clean:
	rm -f $(PROG) *.o
