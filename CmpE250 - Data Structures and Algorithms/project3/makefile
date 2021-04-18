compiler = g++

project3.exe:	main.o Graph.o
		$(compiler) main.o Graph.o -o project3.exe
main.o:	main.cpp Graph.h
	$(compiler) -c main.cpp -o main.o
Graph.o:	Graph.cpp Graph.h
		$(compiler) -c Graph.cpp -o Graph.o
clean:
	rm *.o project3.exe
