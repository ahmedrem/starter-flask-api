import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import scale, StandardScaler, MinMaxScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
#from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error, r2_score, roc_auc_score, roc_curve, classification_report, precision_recall_fscore_support
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from keras.layers import Dropout
from keras import regularizers
from keras import models
import joblib
import warnings
warnings.simplefilter(action = "ignore")

def prepare_dataset(path):
    df = pd.read_csv(path, encoding='ISO-8859-1')
    dataset = df.loc[:,['O','C','E','A','N','BL','TM','LS','SL','WS','genre','droitier/guacher']]
    #dataset["O"] = np.where(dataset["O"] >= np.median(dataset["O"]), 1, 0)
    #dataset["C"] = np.where(dataset["C"] >= np.median(dataset["C"]), 1, 0)
    #dataset["E"] = np.where(dataset["E"] >= np.median(dataset["E"]), 1, 0)
    #dataset["A"] = np.where(dataset["A"] >= np.median(dataset["A"]), 1, 0)
    #dataset["N"] = np.where(dataset["N"] >= np.median(dataset["N"]), 1, 0)
    X = dataset.loc[:,'BL':'WS']
    Y = dataset.loc[:,'O':'N']
    X_array = np.asarray(X).astype(np.float32)
    Y_array = np.asarray(Y).astype(np.float32)
    transformer = RobustScaler().fit(X_array)
    X_data = transformer.transform(X_array)
    Y_data = Y_array
    #Y_scale = Y_array[:,2]
    #X_train, X_test, Y_train, Y_test = train_test_split(X_scale, Y_scale, train_size=0.9, random_state=12345, shuffle=True)
    #print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)
    #print(X_train[0])
    #return X_train, X_test, Y_train, Y_test 
    return X_data, Y_data 


def build_ann_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(512, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(1024))
    model.add(Dropout(0.3))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(n_outputs))
    model.compile(loss='mae', optimizer='adam', metrics=['accuracy'])
    return model

def fit_ann_model(load):
    X_data, Y_data = prepare_dataset('questionnaire_VF.csv')
    if load==False:
        n_inputs, n_outputs = X_data.shape[1], Y_data.shape[1]
        model = build_ann_model(n_inputs, n_outputs)
        model.fit(X_data, Y_data, verbose=1, epochs=1000)
        model.save("ann_model")
    else:
        model = models.load_model("ann_model") 
    
    score = model.evaluate(X_data, Y_data, verbose=1)
    return model, score    

def evaluate_ann_model(model, x_values):
    x_values = np.asarray(x_values).astype(np.float32)
    x_values = x_values.reshape(1,-1) 
    transformer = RobustScaler().fit(x_values)
    x_values = transformer.transform(x_values)
    y_values = model.predict(x_values)
    return y_values










#2,1,2.5,3,4.5,-0.66,0,191.11,49.69,51.09
#3,3,2.5,3,4,-1.06,24,172.86,42.77,15.98

'''
model, score = fit_ann_model(True)
print('Model Loss     :', score[0])
print('Model Accuracy :', score[1])
predictions = evaluate_ann_model(model, [-1.06,24,172.86,42.77,15.98])
print('Predicted BigFive Traits : %s' % predictions[0])
'''




'''

MLP CLassifier

def train_model(X_train, X_test, Y_train, Y_test):
    mlp = MLPClassifier(max_iter=5000, alpha=0, random_state=0, learning_rate="invscaling", verbose=0)
    mlp.fit(X_train, Y_train)
    print("Accuracy on training set: {:.3f}".format(mlp.score(X_train, Y_train)))
    print("Accuracy on test set: {:.3f}".format(mlp.score(X_test, Y_test)))
    joblib.dump(mlp,'mlp_model.pkl.pkl')
    #mlp_loaded = joblib.load('mlp_model.pkl.pkl')


def predict(bl, tm, ls, sl, ws):
    mlp = joblib.load('mlp_model.pkl.pkl')
    x_values = [bl, tm, ls, sl, ws]
    x_values = np.asarray(x_values).astype(np.float32)
    x_values = x_values.reshape(1,-1) 
    transformer = RobustScaler().fit(x_values)
    x_values = transformer.transform(x_values)
    return mlp.predict(x_values)[0]
    

#X_train, X_test, Y_train, Y_test = prepare_dataset('questionnaire_VF.csv')
#train_model(X_train, X_test, Y_train, Y_test)
#2,1,2.5,3,4.5,-0.66,0,191.11,49.69,51.09
#3,3,2.5,3,4,-1.06,24,172.86,42.77,15.98
#print("Prdicted Big five Trait X : {}".format(predict(-0.66, 0, 191.11, 49.69, 51.09)))

'''
