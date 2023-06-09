## Description
* Open the project folder in terminal. 
* Please put the `dataset` folder in the same directory as other `.py` files. Your folder structure should be as follows:
   ```bash
  Assignment2
   ├── dataset
   │   ├── reut2-000.sgm
   │   ├── reut2-001.sgm
   │   ├── ...
   │   ├── reut2-021.sgm
   |   └─────────────────
   ├── models
   │   ├── multinomial.py
   │   ├── bernoulli.py
   |   └───────────────── 
   ├── dataprocessor.py
   ├── tokenizer.py
   ├── splitter.py
   ├── utils.py
   ├── train.py
   ├── test.py
   └── README.md
   ```
* You do not have to install any additional libraries since all the libraries used are built-in Python libraries. If you do not have Python installed, you can download it from [here](https://www.python.org/downloads/). I used Python `3.9.13`.
* Flow of the program is as follows:
   1. `dataprocessor.py` preprocesses the data and dumps the necessary data structures as a picke file (`dataset.pkl`).
   2. `splitter.py` splits the data into training (training + validation) and test sets. The default split ratio is 80:20. Splitted datasets are stored as a pickle file (`splits.pkl`).
   3. `train.py` trains the model on training set and evaluates it on the validation set. You can test different alpha values on training set.
   4. `test.py` trains the model on the training + validation set and evaluates it on the test set.

* First, run `dataprocessor.py` to preprocess the data. The default dataset folder is `dataset`. The default output file is `dataset.pkl`. You can change the output file name by passing the argument `--output` to the script. 
   ```bash
   python dataprocessor.py --dataset dataset --output dataset.pkl
   ```
* Then, run `splitter.py` to split the data into training and test sets. The default split ratio is 80:20. The default input file is `dataset.pkl`. The default output file is `splits.pkl`. You can change the output file name by passing the argument `--output` to the script. You can set the split ratio by passing the argument `--ratio` to the script. Also you can change the number of most common topics to be considered by passing the argument `--topics` to the script.
   ```bash
   python splitter.py --ratio 0.8 --topics 10 --input dataset.pkl --output splits.pkl
   ```
* Then, run `train.py` to train the model on the training set and evaluate it on the validation set with any alpha value. The default input file is `splits.pkl`. You can provide more than one alpha value for hyperparameter tuning.
   ```bash
   python train.py --input dataset.pkl --splits splits.pkl --model m --alpha 0.5
   ```
   You can choose the model by passing the argument `--model` to the script. The default model is `m` (Multinomial Naive Bayes). You can choose `b` (Bernoulli Naive Bayes) as the model. 
* Finally, run `test.py` to train the model on the training + validation set and evaluate it on the test set. The default input file is `splits.pkl`.
   ```bash
   python test.py --input dataset.pkl --splits splits.pkl --model m --alpha 0.5
   ```
* You can run a randomization test using `randomization_test.py` as follows:
   ```bash
   python randomization_test.py --input dataset.pkl --splits splits.pkl  --alpha 0.5 -r 100
   ```
   where `r` is the number of iterations to be run. The default value is 1000. You can change it by passing the argument `--randomization` to the script.

## How to Run? (Quick)
* Open the project folder in terminal.
* Run the following commands to train <b>Multinomial NB</b> model and evaluate it on the test set:
   ```bash
   python dataprocessor.py 
   python splitter.py 
   python train.py --model m --alpha X
   python test.py --model m --alpha X
   ```
   where `X` is the best alpha value obtained from the validation set. You should provide it as a command line argument. Its default value is 0.5 as we get the best evaluation results with $\alpha=0.5$.
* Run the following commands to train <b>Bernoulli NB</b> model and evaluate it on the test set:
   ```bash
   python dataprocessor.py 
   python splitter.py 
   python train.py --model b --alpha X
   python test.py --model b --alpha X 
   ```
   where `X` is the best alpha value obtained from the validation set. You should provide it as a command line argument. Its default value is 0.5 as we get the best evaluation results with $\alpha=0.5$.
* Run the randomization test as follows:
   ```bash
   python randomization_test.py -ma 0.5 -ba 0.5
   ```