compiler = nvcc
file := pagerank
ext := cu

$(file).exe: $(file).$(ext)
			$(compiler) $(file).$(ext) 

clean:
	rm *.exp *.exe *.lib

# run with: MinGW32-make
# clean: MinGW32-make clean