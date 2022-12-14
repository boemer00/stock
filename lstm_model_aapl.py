# -*- coding: utf-8 -*-
"""LSTM model -AAPL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mkvX3ZNe6cDGdimMUY3I0xpfG_AsT8cW
"""

import math
import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

df = web.DataReader('AAPL',
                    data_source='yahoo',
                    start='2012-01-01',
                    end='2019-12-17')

df

plt.figure(figsize=(16,8))
plt.title('Close Price History')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD')
plt.show();

# create a new df with only close column
data = df[['Close']]

# convert df to np.array
dataset = data.values

# get number of rows to the train model
training_data_len = math.ceil(len(dataset) * 0.8)
training_data_len

# Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

# create training dataset
train_data = scaled_data[:training_data_len, :]

# split data
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])

  if i <= 60:
    print(x_train)
    print(y_train)
    print()

# convert to np.arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# reshape data expects 3D
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape

# build model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# compile
model.compile(optimizer='adam', loss='mean_squared_error')

# train
model.fit(x_train, y_train, batch_size=1, epochs=1)

# create testing dataset
# create a new array containing values from index 1543 to 2003
test_data = scaled_data[training_data_len-60:,:]

# create the datasets x_test and y_test
# split data
x_test = []
y_test = dataset[training_data_len:,:]

for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i,0])

# convert data to np.array (to use it in lstm model)
x_test = np.array(x_test)

# reshape data
# number of rows/samples, time steps (cols), number of features = close price
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# predict values
# predictions to contain the same values as our y_test
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# evaluate model (rmse - std of the residuals)
rmse = np.sqrt(np.mean(predictions - y_test)**2)
rmse

# plot data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title('Model')
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']], )
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD')
plt.legend(['train', 'validation', 'predictions'], loc='lower right')
plt.show();

# valid vs predict prices
valid

# get quote
apple_quote = web.DataReader('AAPL',
                    data_source='yahoo',
                    start='2012-01-01',
                    end='2019-12-17')

# create new df
new_df = apple_quote[['Close']]

# get last 60 day closing price and convert the df to np.array
last_60d = new_df[-60:].values

# scale data
last_60d_scaled = scaler.transform(last_60d)

# create list
X_test = []

# append the past 60d
X_test.append(last_60d_scaled)

# convert
X_test = np.array(X_test)

# reshape
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# get predicted scaled price
pred_price = model.predict(X_test)

# undo scaling
pred_price = scaler.inverse_transform(pred_price)
pred_price

# get quote
apple_quote2 = web.DataReader('AAPL',
                    data_source='yahoo',
                    start='2019-12-18',
                    end='2019-12-18')

apple_quote2['Close']

