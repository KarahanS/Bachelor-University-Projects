import pickle

def predict(model, testset):
    predictions = {}
    for doc in testset:
        predictions[doc] = model.predict(doc)
    return predictions

def evaluate(model, validation, gtopics, predictions):
    matrix = {}
    for topic in model.topics:
        matrix[topic] = [0.0, 0.0, 0.0]
    # matrix[topic][0] --> tp
    # matrix[topic][1] --> fp
    # matrix[topic][2] --> fn
    
    """
    You can un-comment this section to use scikit-learn's metrics for comparison

    actuals = {}
    for doc in validation:
        targets = model.documents[doc]['topics']
        targets = [t for t in targets if t in gtopics]
        actuals[doc] = targets

    from sklearn.metrics import f1_score, precision_score, recall_score
    from sklearn.preprocessing import MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    true_labels_bin = mlb.fit_transform(actuals.values())
    predicted_labels_bin = mlb.transform([[p] for p in predictions.values()])

    scikitF1Micro = f1_score(true_labels_bin, predicted_labels_bin, average='micro')
    scikitF1Macro = f1_score(true_labels_bin, predicted_labels_bin, average='macro')
    scikitPrecisionMacro = precision_score(true_labels_bin, predicted_labels_bin, average='macro')
    scikitPrecisionMicro = precision_score(true_labels_bin, predicted_labels_bin, average='micro')
    scikitRecallMacro = recall_score(true_labels_bin, predicted_labels_bin, average='macro')
    scikitRecallMicro = recall_score(true_labels_bin, predicted_labels_bin, average='micro')

    print("Scikit Precision micro:", scikitPrecisionMicro)
    print("Scikit Precision macro:", scikitPrecisionMacro)
    print("Scikit Recall micro:", scikitRecallMicro)
    print("Scikit Recall macro:", scikitRecallMacro)
    print("Scikit F1 micro:", scikitF1Micro)
    print("Scikit F1 macro:", scikitF1Macro)
    """
   
    false = 0
    correct = 0
    actuals = {}
    for doc in validation:
        targets = model.documents[doc]['topics']
        targets = [t for t in targets if t in gtopics]
        actuals[doc] = targets

        prediction = predictions[doc]
        if prediction in targets: correct += 1
        else: false += 1

        #           for topic t:
        # true positive= target: t + prediction: t
        # false positive= target: x  + prediction: t
        # false negative= target: t + prediction: x
        # true negative= target: x + prediction: x [this is not used]

        if prediction in targets: matrix[prediction][0] += 1.0
        else: matrix[prediction][1] += 1.0

        for target in targets:
            if target == prediction: continue
            else:
                matrix[target][2] += 1.0 # false negative

    return correct, (correct+false), _f1(matrix, average = 'micro'), _f1(matrix, average = 'macro'), _average_precision(matrix, average = 'micro'), _average_precision(matrix, average = 'macro'), _average_recall(matrix, average = 'micro'), _average_recall(matrix, average = 'macro')

def _precision(metrics):
    if(metrics[0] == 0): return 0.0
    return (metrics[0] / (metrics[0] + metrics[1]))

def _recall(metrics):
    if(metrics[0] == 0): return 0.0
    return (metrics[0] / (metrics[0] + metrics[2]))

"""
F1 score is a metric which is calculated per class, which means 
that if you want to calculate the overall F1 score for a dataset 
with more than one class you will need to aggregate in some way. 
Micro and macro F1 score are two ways of doing this aggregation.

F1 = TP / (TP + (1/2) * (FP + FN))
"""
def _f1(matrix, average):
    if average == 'macro':
        f1s = {}
        for topic in matrix:
            f1s[topic] = matrix[topic][0] / (matrix[topic][0] + (0.5) * (matrix[topic][1] + matrix[topic][2]))
        return sum(f1s.values()) / len(f1s)
    elif average == 'micro':
        tp = 0.0
        fp = 0.0
        fn = 0.0
        for topic in matrix:
            tp += matrix[topic][0]
            fp += matrix[topic][1]
            fn += matrix[topic][2]
        return tp / (tp + (0.5) * (fp + fn))  
    else:
        raise ValueError("Average should be either 'macro' or 'micro'.")

def _average_precision(matrix, average):
    if average == 'macro':
        precisions = {}
        for topic in matrix:
            precisions[topic] = _precision(matrix[topic])
        return sum(precisions.values()) / len(precisions)
    elif average == 'micro':
        tp = 0.0
        fp = 0.0
        for topic in matrix:
            tp += matrix[topic][0]
            fp += matrix[topic][1]
        return tp / (tp + fp)
    else:
        raise ValueError("Average should be either 'macro' or 'micro'.")

def _average_recall(matrix, average):
    if average == 'macro':
        recalls = {}
        for topic in matrix:
            recalls[topic] = _recall(matrix[topic])
        return sum(recalls.values()) / len(recalls)
    elif average == 'micro':
        tp = 0.0
        fn = 0.0
        for topic in matrix:
            tp += matrix[topic][0]
            fn += matrix[topic][2]
        return tp / (tp + fn)
    else:
        raise ValueError("Average should be either 'macro' or 'micro'.")
    
def dump(data, dumpfile):
    # dump the vocabulary
    # open a file, where you ant to store the data
    with open(dumpfile, 'wb') as f:
        pickle.dump(data, f)

def load(dumpfile):
    with open(dumpfile, 'rb') as f:
        model = pickle.load(f)
    return model


if __name__ == "__main__":
    matrix = {}
    # matrix[topic][0] --> tp
    # matrix[topic][1] --> fp
    # matrix[topic][2] --> fn

    matrix['A'] = [15, 11, 2]
    matrix['B'] = [10, 90, 7]
    matrix['C'] = [5, 2, 1]

    print("micro f1:", _f1(matrix, average = 'micro'))
    print("macro f1:", _f1(matrix, average = 'macro'))
    print("micro average precision:", _average_precision(matrix, average = 'micro'))
    print("macro average precision:", _average_precision(matrix, average = 'macro'))
    print("micro average recall:",_average_recall(matrix, average = 'micro'))
    print("macro average recall:", _average_recall(matrix, average = 'macro'))

    matrix2 = {}

    matrix2['0'] = [10, 2, 3]
    matrix2['1'] = [20, 10, 12]
    matrix2['2'] = [5, 1, 1]
    print("-"*50)
    print("micro f1:", _f1(matrix2, average = 'micro'))
    print("macro f1:", _f1(matrix2, average = 'macro'))
    print("micro average precision:", _average_precision(matrix2, average = 'micro'))
    print("macro average precision:", _average_precision(matrix2, average = 'macro'))
    print("micro average recall:",_average_recall(matrix2, average = 'micro'))
    print("macro average recall:", _average_recall(matrix2, average = 'macro'))
