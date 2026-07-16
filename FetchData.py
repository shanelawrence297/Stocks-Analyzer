import matplotlib.pyplot as plt
import yfinance as yf
import requests 
def get_ticker(company_name):
   url="https://query2.finance.yahoo.com/v1/finance/search"
   user_agent="Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
   region=input("Enter your country: ").strip().lower()
   params={"q":company_name,"quotes_count":5}
   response=requests.get(url=url,params=params,headers={"User-Agent": user_agent})
   data=response.json()
   if len(data["quotes"])==0:
       return None
   if region == "india":
        matches = [q for q in data["quotes"] if q.get("symbol", "").endswith((".NS", ".BO"))and q.get("quoteType")=="EQUITY"]
   elif region == "us":
        matches = [q for q in data["quotes"] if q.get("exchange") in ("NMS", "NYQ", "NGM")and q.get("quoteType")=="EQUITY"]
   else:
        matches = data["quotes"]
   if len(matches) == 0:
        print("No matches found for the specified region. Please check the company name and try again.")
        matches=data["quotes"]
   return matches[0]["symbol"]
def getdata(ticker):
    DataFrame=yf.download(ticker, period="2y", interval="1d")
    DataFrame["SMA_20"]=DataFrame["Close"].rolling(window=20).mean()
    DataFrame["SMA_50"]=DataFrame["Close"].rolling(window=50).mean()
    difference=DataFrame["Close"].diff()
    gain=difference.where(difference>0,0)
    loss=-difference.where(difference<0,0)
    avg_gain=gain.rolling(window=14).mean()
    avg_loss=loss.rolling(window=14).mean()
    relative_strength=avg_gain/avg_loss
    DataFrame["RSI"]=100-(100/(1+relative_strength))
    latest_rsi=DataFrame["RSI"].iloc[-1]
    if DataFrame["SMA_20"].iloc[-1] > DataFrame["SMA_50"].iloc[-1] and latest_rsi<70:
        signal="BUY"
    elif DataFrame["SMA_20"].iloc[-1] < DataFrame["SMA_50"].iloc[-1] and latest_rsi>30:
        signal="SELL"
    else:
        signal="HOLD"
    print(DataFrame.head())
    plt.figure(figsize=(10,5))
    plt.plot(DataFrame.index, DataFrame['Close'], label='Close Price')
    plt.plot(DataFrame.index, DataFrame['SMA_20'], label='20-Day SMA')
    plt.plot(DataFrame.index, DataFrame['SMA_50'], label='50-Day SMA')
    print(f"Signal for {ticker}: {signal}")
    plt.title(f'{ticker} Closing Price Over 2 Years(Previous)')
    plt.xlabel("Date")
    plt.ylabel('Price')
    print(f"RSI:{latest_rsi:.2f}")
    plt.show()
    return signal,DataFrame
company_name=input("Enter the name of the company in which you have stocks:")
ticker=get_ticker(company_name)
currency_symbol="₹" if(".NS"in ticker or".BO"in ticker) else "$"
if ticker is None:
    print("Company not found. Please check the name and try again.")
    exit()
print(f"Found ticker: {ticker}")    
shares=int(input("What is the quantity of the shares you possess?"))
buy_price=float(input("What was the price at which you bought the shares?"))
signal,DataFrame= getdata(ticker)
current_price=float(DataFrame["Close"].dropna().iloc[-1].item())
profit_loss_percentage=((current_price-buy_price)/buy_price)*100
print(f"\nYou have {shares} shares in {ticker}, bought at {currency_symbol}{buy_price} each.")
print(f"Current price: {currency_symbol}{current_price:.2f}")
print(f"Profit/Loss: {profit_loss_percentage:.2f}%")
print(f"Current Signal for {ticker} is: {signal}")
if signal == "BUY":
    print("Hold or consider buying more.")
else:
    print("Consider your position — signal suggests weakness.")