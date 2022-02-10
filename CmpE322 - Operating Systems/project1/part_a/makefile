CC = g++

TARGETS = part_a.out
OBJECTS = main_a.o
SOURCES = main_a.cpp

all: $(TARGETS)

$(TARGETS): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGETS)

$(OBJECTS):
	$(CC) -c $(SOURCES) -o $(OBJECTS)
clean:
	rm -f $(OBJECTS) $(TARGETS)