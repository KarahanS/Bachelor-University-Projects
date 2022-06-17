#### Folder Structure

When you open our project, you'll encounter with a folder structure like this:

```
inputFile                        -
horadrimLog.csv                  +
outputFile                       +

2019400132_2018400174
│   2019400132_2018400174.pdf  
└───src
|    │  horadrimSoftware.py
|    |  CatalogHandler.py
|    |  FileHandler.py
|    |  bplustree.py
|    │  utils.py
|    |  settings.py
|    └───Loader
|    |    │   __init__.py
|    |    │   InputLoader.py
|    |    └─────────────────
|    |
|    └───Writer
|    |    |   __init__.py
|    |    |   LogWriter.py
|    |    |   OutputWriter.py
|    |    └─────────────────
|    |
|    └───Trees
|    |    |   type1.json        +
|    |    |   type2.json        + 
|    |    |    ...
|    |    └─────────────────
|    |
|    └───Files
|    |    │   _catalog.bin      +
|    |    │   type1.bin         +
|    |    │   type2.bin         +
|    |    |    ...
|    |    └─────────────────
|    └──────────────────────
└───────────────────────────
```

Files marked with a ```+``` are generated after running the ```horadrimSoftware.py```. Name of the ```outputFile``` is provided by you in the command below. File marked with a ```-``` is provided by you in order to run the program.


#### To run the program: 

We have implemented our own binary file manipulation and B+ Tree for indexing. Therefore there is no external library used in the project. 
So you do not have to install any package. Technically, you don't have to create a virtual environment to run the program as well. To run the program, 
* Navigate to the directory in which the folder ```2019400132_2018400174``` is located. Put your ```inputFile``` to the same directory and run the following command:
```
python 2019400132_2018400174/src/horadrimSoftware.py inputFile outputFile
```
An ```outputFile``` and the ```horadrimLog.csv``` will be generated in your working directory.

You can use ```clear.sh``` to remove all the binary files, catalog, output and log after running the program with an input:
```
./clear.sh
```
