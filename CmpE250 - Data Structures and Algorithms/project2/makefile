compiler = g++
project2.exe:	DeluxePQ.o Event.o HoodiesPQ.o StickersPQ.o main.o Hacker.o
		$(compiler) DeluxePQ.o Event.o HoodiesPQ.o StickersPQ.o main.o Hacker.o -o project2.exe
DeluxePQ.o:	DeluxePQ.cpp DeluxePQ.h
		$(compiler) -c DeluxePQ.cpp -o DeluxePQ.o
Event.o:	Event.cpp Event.h
		$(compiler) -c Event.cpp -o Event.o
HoodiesPQ.o:	HoodiesPQ.cpp HoodiesPQ.h
		$(compiler) -c HoodiesPQ.cpp -o HoodiesPQ.o
StickersPQ.o:	StickersPQ.cpp StickersPQ.h
		$(compiler) -c StickersPQ.cpp -o StickersPQ.o
Hacker.o:	Hacker.cpp Hacker.h
		$(compiler) -c Hacker.cpp -o Hacker.o
main.o:	main.cpp DeluxePQ.h Hacker.h Event.h HoodiesPQ.h StickersPQ.h 
	$(compiler) -c main.cpp -o main.o
clean:
	rm *.o project2.exe
