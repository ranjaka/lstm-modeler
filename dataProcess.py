import yfinance as yf
import pandas as pd
import ta_py as ta
import numpy as np


# ----------------------------------------------------------------

# Get symbolData from yahoo finance
symbolName = 'NUF.AX'
symbolData = yf.Ticker(symbolName)
# hist is a dataframe
hist = symbolData.history(period="max", interval="1d")

# RSI
data_rsi = hist['Close']
result_rsi = ta.rsi(data_rsi,14)

# MACD
slowEMA = 26
fastEMA = 12
data_macd = hist['Close']
result_macd = ta.macd(data_macd,fastEMA,slowEMA)

# Stochastic
data_stoch = []
hist_high = hist['High'].to_numpy()
hist_low = hist['Low'].to_numpy()
hist_close = hist['Close'].to_numpy()
length = 14; # default = 14
smoothd = 3; # default = 3
smoothk = 3; # default = 3

for i in range (0,len(hist_high)):
    temp = np.array([hist_high[i],hist_close[i],hist_low[i]])
    data_stoch.append(temp)

result_stoch = ta.stoch(data_stoch,length,smoothd,smoothk)

print('sizes of hist:{}, rsi:{}, macd:{}, stoch:{}'
.format(len(hist_high),len(result_rsi),len(result_macd),len(result_stoch)))

print('rsi: {}'.format(result_stoch[5592][0]))

lengthRsi = len(result_rsi)
lengthMacd = len(result_macd)
lengthStoch = len(result_stoch)
lengthHist = len(hist)

startIndex = 30
customHist = hist[startIndex:len(hist)]

temp_stoch = []
for i in range(0,lengthStoch):
    temp_stoch.append(result_stoch[i][0])

customHist['rsi'] = result_rsi[startIndex - (lengthHist-lengthRsi):lengthRsi]
customHist['macd'] = result_macd[startIndex - (lengthHist-lengthMacd):lengthMacd]
customHist['stoch'] = temp_stoch[startIndex - (lengthHist-lengthStoch):lengthStoch]
















