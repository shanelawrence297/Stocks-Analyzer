import matplotlib.pyplot as plt
import yfinance as yf
ticker=input("What is the name of the company that you have your stocks in?")
shares=int(input("What is the quantity of the shares you possess?"))
buy_price=float(input("What was the price at which you bought the shares?"))
def getdata(ticker):
    DataFrame=yf.download(ticker, period="2y", interval="1d")
    DataFrame["SMA_20"]=DataFrame["Close"].rolling(window=20).mean()
    DataFrame["SMA_50"]=DataFrame["Close"].rolling(window=50).mean()
    if DataFrame["SMA_20"].iloc[-1] > DataFrame["SMA_50"].iloc[-1]:
        signal="BUY"
    else:
        signal="SELL"
    print(DataFrame.head())
    plt.figure(figsize=(10,5))
    plt.plot(DataFrame.index, DataFrame['Close'], label='Close Price')
    plt.plot(DataFrame.index, DataFrame['SMA_20'], label='20-Day SMA')
    plt.plot(DataFrame.index, DataFrame['SMA_50'], label='50-Day SMA')
    print(f"Signal for {ticker}: {signal}")
    plt.title(f'{ticker} Closing Price Over 2 Years(Previous)')
    plt.xlabel("Date")
    plt.ylabel('Price')
    plt.show()
    return signal
signal = getdata(ticker)
print(f"\n You have {shares} in {ticker} and you bought them at {buy_price} each.")
print(f"Current Signal for {ticker} is: {signal}")
if signal=="BUY":
    print(f"Hold or risk Buying.")
else:
    print(f"Consider your position...According to signal, its quite unpredictable.")