import yfinance as yf


#----------------------------------------------------------------

# Get symbol from yahoo finance 
nuf = yf.Ticker("NUF.AX")
# hist is a dataframe
hist = nuf.history(period="max", interval="1d")



print("info: {}, and type is: {}".format(hist, type(hist)))