compiler = g++

project1.exe:	main.o Character.o
	        $(compiler)  main.o Character.o -o project1.exe
main.o:	main.cpp Character.h
	$(compiler) -c main.cpp
Character.o:	Character.cpp Character.h
		$(compiler) -c Character.cpp
clean:
	rm *.o project1.exe
