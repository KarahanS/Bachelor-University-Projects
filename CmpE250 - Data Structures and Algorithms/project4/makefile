compiler = g++

project4.exe:	main.o
		$(compiler) main.o -o project4.exe
main.o:	main.cpp
	$(compiler) -c main.cpp -o main.o
clean:
	rm *.o project4.exe
