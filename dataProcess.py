import yfinance as yf
import pandas as pd
import ta_py as ta
import numpy as np

from sklearn.preprocessing import MinMaxScaler

# Keras importors
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM


# ----------------------------------------------------------------

# Get symbolData from yahoo finance
symbolName = 'NUF.AX'
symbolData = yf.Ticker(symbolName)
# hist is a dataframe
hist = symbolData.history(period="max", interval="1d")

# Reset date index so all aligned
hist.reset_index(inplace=True)


# RSI
data_rsi = np.array(hist['Close'])
result_rsi = ta.rsi(data_rsi,14)

# MACD
slowEMA = 26
fastEMA = 12
data_macd = np.array(hist['Close'])
result_macd = ta.macd(data_macd,fastEMA,slowEMA)

# Stochastic
data_stoch = []
hist_high = np.array(hist['High'])
hist_low = np.array(hist['Low'])
hist_close = np.array(hist['Close'])
length = 14; # default = 14
smoothd = 3; # default = 3
smoothk = 3; # default = 3

for i in range (0,len(hist_high)):
    temp = np.array([hist_high[i],hist_close[i],hist_low[i]])
    data_stoch.append(temp)

result_stoch = ta.stoch(data_stoch,length,smoothd,smoothk)

print('sizes of hist:{}, rsi:{}, macd:{}, stoch:{}'
.format(len(hist_high),len(result_rsi),len(result_macd),len(result_stoch)))

# Size of each TA results
lengthRsi = len(result_rsi)
lengthMacd = len(result_macd)
lengthStoch = len(result_stoch)
lengthHist = len(hist)

# Starting index for sample data (any value before this index is not used in
# training or validating)
startIndex = 30
customHist = hist[startIndex:len(hist)]

temp_stoch = []
for i in range(0,lengthStoch):
    temp_stoch.append(result_stoch[i][0])

customHist['rsi'] = result_rsi[startIndex - (lengthHist-lengthRsi):lengthRsi]
customHist['macd'] = result_macd[startIndex - (lengthHist-lengthMacd):lengthMacd]
customHist['stoch'] = temp_stoch[startIndex - (lengthHist-lengthStoch):lengthStoch]

# print('length of customHist:{}'.format(customHist))


# Normalising Close data

datasetClose = pd.DataFrame(index=range(0,len(customHist)), columns=['Date','Close'])
for i in range(0,len(customHist)):
    datasetClose['Date'][i] = customHist['Date'][i+startIndex]
    datasetClose['Close'][i] = customHist['Close'][i+startIndex]

datasetClose.index = datasetClose.Date
datasetClose.drop('Date',axis=1,inplace=True)

model_close = datasetClose.values
scaler_close = MinMaxScaler(feature_range=(0,1))
scaled_data_close = scaler_close.fit_transform(model_close)

print(scaled_data_close)




















