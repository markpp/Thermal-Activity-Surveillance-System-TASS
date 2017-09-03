import itertools
import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sympy.strategies.core import switch

def calculate_accuracy(TP, TN, total):
    return float((TP + TN)/total)

# def calculate_precision_ver1(TP, FP): 
#     """
#     Different people calculate it different
#     1. TP / (TP + FP)
#     2. TP / prediction yes
#     """
#     return float(TP/ (TP + FP)) 
# 
# def calculate_precision_ver2(TP, FP, pred_yes): 
#     """
#     Different people calculate it different
#     1. TP / (TP + FP)
#     2. TP / prediction yes
#     """
#     return float(TP / pred_yes)    
# 
# def calculate_accuracy_relative(y, x):
#     """
#     Input:  y - being the count from our detector during a period t
#             x - being the manual count
#     """
#     return (y - x)/x


        

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


if __name__ == "__main__":
    """
    Main function for executing the confusion_matrix.py script. 
    
    Display Confusion Matrix
    
    Command: 
        -p path/to/track/csv -b  path/to/bb/csv
        -p '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/2015-09-02-12-44_log.csv' 
        -b '/home/louise/Documents/MountainBike/datasets/thermal_mtb/2015-09-02-12-44/2015-09-02-12-44_bb.csv' 
            
    """
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--log_path", type=str,
                    help="Path to track 'csv' file")
    ap.add_argument("-b", "--bb_path", type=str,
                    help="Path to bounding box 'csv' file")
    args = vars(ap.parse_args())

    log_path = args["log_path"]
    bb_path = args["bb_path"]
    
    time2frame = {"5":2700, "15":8100, "30":16200, "60":32400}
    log_data = pd.read_csv(log_path, delimiter=';',dtype=str, names = ["Frame", "Tag", "Exit"])
    log_data['df_index'] = log_data.index
    log_data[['Frame']] = log_data[['Frame']].apply(pd.to_numeric)
    log_data = log_data.sort_values(["Frame", "df_index"], ascending=[True, True])  
    log_data['Tag'].replace(["B","P"], ["MTB", "PED"],inplace=True)
      
    bb_data = pd.read_csv(bb_path, delimiter=';', dtype=str)
    bb_data['df_index'] = bb_data.index
    bb_data['Frame'] = bb_data['Filename']
    
    for index, row in bb_data.iterrows():
        bb_data.set_value(index,'Frame', float(int(row.Frame[:-4].split('_')[1].split('.')[0])))
    
    bb_data = bb_data.sort_values(["Frame", "df_index"], ascending=[True, True])
    
    y_test = []
    y_pred = []
    for index, row in bb_data.iterrows():
        bb_frame = bb_data['Frame'][index]
        bb_tag = bb_data['Annotation tag'][index]
        
        for index_pred, row_pred in log_data.iterrows():
            pred_frame = log_data['Frame'][index_pred]
            pred_tag = log_data['Tag'][index_pred]
            threshold = time2frame["5"];
            
            #True Positives (TP) - actual MTB
            #False Negatives (FN) - MTB marked as PED
            #False Positives (FP) - PED Marked as MTB
            #True Negatives (TN) - PED correctly classified            
            if (bb_frame - threshold) <= pred_frame <= (bb_frame + threshold):
                y_test.append(bb_tag)
                y_pred.append(pred_tag)
            elif pred_frame < (bb_frame + threshold):
                continue;
            elif pred_frame > (bb_frame + threshold):
                y_test.append(bb_tag)
                y_pred.append("")
                
            log_data.drop(log_data.index[index_pred])
            break;
            
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_test, y_pred, labels=["MTB", "PED"])
    np.set_printoptions(precision=2)
    
    #Display data
    #1. Create tables with data for each of the classes
    #2. Accuracy
        # - Relative Error (was calculated just to plot a nice scatter graph)  
        # - Mean Absolute Percent Error (MAPE) (getting the average percentage of the error over a period)
        # - Overall Error 
    #3. Error Rate
    #4. Precision
    #5. Recall (True Positive Rate)
    
    
    
    
    class_names = ["PED", "MTB"]
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names,
                          title='Confusion matrix')
    
    # Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')
    
    plt.show()