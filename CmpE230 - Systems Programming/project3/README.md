The list of the crypto currencies that will be displayed should be read from a file. The name of the file should be obtained from an environment variable called  <b> MYCRYPTOCONVERT </b>. Details as to the format of the file can be found in the report.
#### To set a temporary environment variable:
* Windows command line:
```cmd
set MYCRYPTOCONVERT=path_of_the_file
```
* Linux terminal:
```bash
export MYCRYPTOCONVERT=path_of_the_file
```
#### To compile and run the program: 
```bash
qmake -project
qmake CoinExchange.pro
./CoinExchange
```

