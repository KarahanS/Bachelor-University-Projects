## Introduction
* This is the second homework of the course. It is about parallelizing the PageRank algorithm using MPI and CUDA. The program is written in C++ and Python.
* Similar to the first project, you have to have `graph.txt` located in this folder (`CmpE478 - Parallel Processing`). You can install it from [here](https://web.archive.org/web/20220310125510/http://web-graph.org/index.php/download).

## 1) MPI

* First of all, we have to install some components to run our MPI codes successfully: Download `Microsoft MPI v10.1.2` from [here](https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi) if you are using Windows. At the end, it will prompt you to mark two components: Binary files and SDK to run C/C++ files. Although SDK is not necessary to run `mpi4py`, you should install it as well for the next stages.
* Add binaries to the PATH environment variables, in my case they were located in `C:\Program Files\Microsoft MPI\Bin\`.
* Following folders should be included in the makefile (paths will be different in your case):
    * `C:\Program Files (x86)\Microsoft SDKs\MPI\Include\`
    * `C:\Users\karab\Desktop\MPI\Lib\x86`: I used `MinGW32` therefore I added `x86` version, but you may add `x64` depending on your compiler and the architecture.
    * `C:\Users\karab\Desktop\MPI\inc`
* In the previous step, we added `Bin` folder to the PATH. Now we should be able to use commands. You can list all of the MPI related folders by writing `set msmpi` to the console. 

## Metis
* We used `metis` wrapper library to use Metis on Python. In order to use Metis, we have to install the core of the Metis. To do so, follow the steps below (we will be building it from source using Visual Studio Community):
   * Firstly, download `cmake` for Windows: https://cmake.org/download/
   * Then download the `conda-metis` folder from here: https://github.com/guglielmosanchini/conda-metis
   * Open the folder and a terminal. Run `cmake --help` to list available generators. After finding one (in my case it was Visual Studio Community 2019), run the following command in the `conda-metis-master` folder:
      ```cmd
      .\vsgen -G "Visual Studio 16 2019" -A x64
      ```
   * Then go to the `conda-metis-master\build\windows` folder and click on the `metis.sln` file. It will open the project in Visual Studio. Build the project (Build Solution above). After building, you can find the `metis.dll` file in the `conda-metis-master\build\windows\libmetis\Release` folder. (In my case, it didn't successfully build all the components but `metis.dll` was built anyways.)
   * Add the path of the `metis.dll` file to the `PATH` environment variable. (It should be a separate environment variable called `METIS_DLL`. Our `metis` wrapper directly looks for it.)
* After successfully configuring the `metis`, proceed with installing necessary Python libraries: `metis` and `networkx`.
* Try running `partition.py` to see if `metis` is working properly:
   ```cmd
   python partition.py
   ```
* `partition.py` is used to create METIS partitions on the given graph. They are stored in a folder called `partitions`. It's important that you prepare necessary partitions before running the `mpi.cpp`.
* You can run `mpi` using C++ with the commands below:
   ```cmd
   MinGW32-make 
   mpiexec -n 5 ./mpi.exe
   ```

## 2) NVIDIA CUDA Thrust
* First, you must have the [Cuda Developer Kit](https://developer.nvidia.com/cuda-toolkit) installed. 
* After installing it, add the binaries to path. In my case, it is located in `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin`.
* Run `nvcc --version` on command line to see if `nvcc` is working correctly.
* To run program, you can use the makefile. Or you can the following command directly:
   ```cmd
   nvcc pagerank.cu
   ```
* Run the executable:
   ```cmd
   ./a.exe
