## How to Run?
* Open the project folder in terminal. 
* Please put the `dataset` folder in the same directory as the `dataprocessor.py` and `queryprocessor.py` files. Your folder structure should be as follows:
   ```bash
  Assignment1
   ├── dataset
   │   ├── reut2-000.sgm
   │   ├── reut2-001.sgm
   │   ├── ...
   │   ├── reut2-021.sgm
   |   └─────────────────
   ├── dataprocessor.py
   ├── queryprocessor.py
   ├── tokenizer.py
   ├── trie.py
   └── README.md
   ```
* You do not have to install any additional libraries since all the libraries used are built-in Python libraries. If you do not have Python installed, you can download it from [here](https://www.python.org/downloads/). I used Python `3.9.13`.
* Firstly, we have to run the `dataprocessor.py` to preprocess the data and create the inverted indexing schema. To do so, run the following command in the terminal:
   ```bash
   python dataprocessor.py
   ```
   As a result, indexing schema will be dumped as a pickle file in the working directory (`vocab.pickle`).
* After the data is processed, we can run the `queryprocessor.py` to run the program. You can provide either a phrase query or a proximity query. To run a proximity query, run the following command in the terminal:
   ```bash
   python queryprocessor.py w1 k w2
   ```
* To run a phrase query, run the following command in the terminal:
   ```bash
   python queryprocessor.py "w1 w2 ... wn"
   ```

   Please observe that you have to provide phrase query within the quotation marks. Also, you have to provide the query in the same order as it appears in the document. For example, if you want to search for the phrase "the quick brown fox", you have to provide the query as `"the quick brown fox"`. If you provide the query as `"quick brown fox the"`, it will not work.

* The program will print the results in the terminal. 

