compiler = g++
file := erdos
ext := cpp
CFLAGS :=  
XPRE :=
FOLD1 :=
FOLD2 :=

ifeq ($(OS),Windows_NT) 
    detected_OS := Windows
else
	UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Darwin)
		detected_OS := Darwin
	else
		detected_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
    endif
    
endif

ifeq ($(detected_OS),Windows)
	CFLAGS += -std=c++11
else
	ifeq ($(detected_OS),Darwin)
		compiler = clang++
		XPRE += -Xpreprocessor
		FOLD1 += -I/opt/homebrew/Cellar/libomp/15.0.5/include -L/usr/local/lib -L/opt/homebrew/Cellar/libomp/15.0.5/lib -lomp
		FOLD2 += -I/opt/homebrew/Cellar/libomp/15.0.5/include
		CFLAGS +=  -g -Wall -std=c++17 -arch arm64
	else
		CFLAGS += -std=c++11	
	endif
endif

$(file).exe: $(file).o
			$(compiler) $(file).o -o $(file).exe $(XPRE)  -fopenmp $(FOLD1) $(CFLAGS) 
$(file).o:  $(file).$(ext)
			$(compiler) -c $(file).$(ext) -o $(file).o $(XPRE) -fopenmp $(FOLD2) $(CFLAGS)

clean:
	rm *.o *.exe

# on windows:
# run with: MinGW32-make
# clean: MinGW32-make clean

# on mac/linux:
# run with: make
# clean: make clean
