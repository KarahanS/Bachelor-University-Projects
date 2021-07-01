CXX = g++ -std=c++14

mylang2ir:	Main.o Writer.o Parser.o
				$(CXX) Main.o Writer.o Parser.o -o mylang2ir -lm

Main.o:			Main.cpp Parser.h
				$(CXX) -c Main.cpp

Parser.o:		Parser.cpp Parser.h
				$(CXX) -c Parser.cpp

Writer.o:		Writer.cpp Writer.h
				$(CXX) -c Writer.cpp
