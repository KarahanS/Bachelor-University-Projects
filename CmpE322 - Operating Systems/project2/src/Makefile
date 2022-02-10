CC = g++

TARGETS = abstractor.out
OBJECTS = abstractor.o
SOURCES = abstractor.cpp

all: $(TARGETS)

$(TARGETS): $(OBJECTS)
	$(CC) -pthread $(OBJECTS) -o $(TARGETS)

$(OBJECTS):
	$(CC) -c $(SOURCES) -o $(OBJECTS)
clean:
	rm -f $(OBJECTS) $(TARGETS)