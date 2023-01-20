compiler = g++
file := mpi
ext := cpp

MPI_DIR = C:\Users\karab\Desktop\MPI

FOLD1 = -I $(MPI_DIR)\Include
FOLD2 = -L $(MPI_DIR)\Lib\x86
FOLD3 = -I $(MPI_DIR)\inc
MPI = -lmsmpi

$(file).exe: $(file).o 
		$(compiler) $(file).o $(FOLD1) $(FOLD2) $(FOLD3) $(MPI)   -o $(file).exe 
$(file).o:  $(file).$(ext)
		$(compiler) -c $(file).$(ext) $(FOLD1) $(FOLD2) $(FOLD3) $(MPI)  -o $(file).o  

clean:
	rm *.o *.exe