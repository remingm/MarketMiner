import random
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.utils import check_array
from sklearn.cross_validation import train_test_split
from sklearn import datasets, cross_validation, metrics
from sklearn import preprocessing
from sklearn.preprocessing import Imputer

import tensorflow as tf

import skflow


train = pandas.read_csv('sp66yrsNewCols.csv')
#y = train['percent_change_next_weeks_price']


predictFor = 'TomorrowDif'


y = train[predictFor]
#X = train[['open', 'high', 'low', 'close', 'volume', 'percent_change_volume_over_last_wk', 'previous_weeks_volume', 'percent_change_price']].fillna(0)
X= train[['Open','High','Low','Close','Volume','RSI','BBandUpper','BBandLower','CMOData','DMIData','MFI','MA','STDDEV']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# imp = Imputer(strategy='mean', verbose=1, axis=0)
# imp.fit(X_train)
# X_train = imp.transform(X_train)
# imp.fit(y_)

# scale data (training set) to 0 mean and unit Std. dev
scaler = preprocessing.StandardScaler()
X_train = scaler.fit_transform(X_train)


# Build 2 layer fully connected DNN with 10, 10 units respecitvely.
regressor = skflow.TensorFlowDNNRegressor(hidden_units=[10, 10],
    steps=2000, learning_rate=0.01, batch_size=30,
    verbose = 1)
# Fit
regressor.fit(X_train, y_train, logdir='/tmp/tf_examples/mm/')

# Predict and score
score = metrics.mean_squared_error(regressor.predict(scaler.fit_transform(X_test)), y_test)
#baseline_score = metrics.mean_squared_error(X_train['close'],  y_test)

print('MSE: {0:f}'.format(score))

# def dnn_tanh(X, y):
#     layers = skflow.ops.dnn(X, [10, 20, 10], tf.tanh)
#     return skflow.models.logistic_regression(layers, y)

# random.seed(42)
# classifier = skflow.TensorFlowEstimator(model_fn=dnn_tanh,
#     n_classes=2, batch_size=128, steps=500, learning_rate=0.05)
# classifier.fit(X_train, y_train)
# print accuracy_score(classifier.predict(X_test), y_test)

#Output vector of predictions for entire X

#Scale X
X = scaler.fit_transform(X)

predicted_y = regressor.predict(X, batch_size=30)

train['PRED:'+predictFor] = predicted_y

train.to_csv('sp66yrsNewCols.csv')

#print train
# outFile = open("predicted_y", 'w')
# for line in predicted_y:
#     outFile.write(str(line[0]))
#     outFile.write('\n')
