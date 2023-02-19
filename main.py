import matplotlib.pyplot as plt
import requests
import datetime


def print_list(l):
    for i in range(0, len(l)-1):
        if i == (len(l)-1):
            print(l[i], end='')
        else:
            print(f"{l[i]}, ", end='')


comp = input("What company would you like to search for?")
# Financial growth data
urlFin = f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{comp}?modules=financialData'
# Info about past five days
urlPast = f'https://query1.finance.yahoo.com/v8/finance/chart/{comp}?metrics=high?&interval=1d&range=5d'
r1 = requests.get(urlFin, headers={'User-agent': 'Mozilla/5.0'})
r2 = requests.get(urlPast, headers={'User-agent': 'Mozilla/5.0'})
req_dict1 = r1.json()
req_dict2 = r2.json()

# Graph interval info
closes,low,opens,high,dates, volumes = [], [],[],[],[], []

for price in req_dict2['chart']['result'][0]['indicators']['quote'][0]:
    for i in range(0, len(req_dict2['chart']['result'][0]['indicators']['quote'][0][price])):
        thisOption = req_dict2['chart']['result'][0]['indicators']['quote'][0][price][i]
        if price == "high":
            high.append(thisOption)
        elif price == "low":
            low.append(thisOption)
        elif price == "volume":
            volumes.append(thisOption)
        elif price == "close":
            closes.append(thisOption)
        elif price == "open":
            opens.append(thisOption)

option = input("What would you like to plot? (close, high, volume, low, open)")
if option == "high":
    yValues = high
elif option == "low":
    yValues = low
elif option == "volume":
    yValues = volumes
elif option == "close":
    yValues = closes
elif option == "open":
    yValues = opens

for unix in req_dict2['chart']['result'][0]['timestamp']:
    date = datetime.datetime.fromtimestamp(unix)
    dates.append(date)

xValues = dates
# Styling and plotting the desired info
fig, ax = plt.subplots()
ax.plot(xValues, yValues)

ax.set_xlabel("Dates")
ax.set_ylabel(f"Prices for {option} (If volume then in million)")
fig.autofmt_xdate()
ax.tick_params(axis='both', which='major', labelsize=16)
plt.show()


def toUnix(day, month, year):
    date = datetime.datetime(year, month, day)
    unix_timestamp = datetime.datetime.timestamp(date)
    return(str(int(unix_timestamp)))

year1 = int(input('What is the starting year?'))
month1 = int(input('What is the starting month?'))
day1 = int(input('What is the starting day of the month?'))

year2 = int(input('\nWhat is the ending year?'))
month2 = int(input('What is the ending month?'))
day2 = int(input('What is the ending day of the month?'))

period1 = toUnix(day1, month1, year1)
period2 = toUnix(day2, month2, year2)
interval = '1mo'
includeAdjustedClose = 'false'

url = f'https://query1.finance.yahoo.com/v8/finance/chart/{comp.lower()}?period1=' + period1 + '&period2=' + period2 + '&interval=' + interval + '&includeAdjustedClose=' + includeAdjustedClose
r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
req_dict = r.json()

closes,low,opens,high,dates, volumes = [], [],[],[],[], []
for price in req_dict['chart']['result'][0]['indicators']['quote'][0]:
    for i in range(0, len(req_dict['chart']['result'][0]['indicators']['quote'][0][price])):
        thisOption = req_dict['chart']['result'][0]['indicators']['quote'][0][price][i]
        if price == "high":
                 high.append(thisOption)
        elif price == "low":
            low.append(thisOption)
        elif price == "volume":
            volumes.append(thisOption)
        elif price == "close":
            closes.append(thisOption)
        elif price == "open":
            opens.append(thisOption)

for unix in req_dict['chart']['result'][0]['timestamp']:
     date = datetime.datetime.fromtimestamp(unix)
     dates.append(date)

option = input("What would you like to plot? (close, high, volume, low, open)")

if option == "high":
    yValues = high
elif option == "low":
     yValues = low
elif option == "volume":
     yValues = volumes
elif option == "close":
     yValues = closes
elif option == "open":
     yValues = opens


# Styling and plotting the desired info
fig, ax = plt.subplots()
ax.plot(dates, yValues)

ax.set_xlabel("Dates")
ax.set_ylabel(f"Prices for {option} (If volume then in million)")
fig.autofmt_xdate()
ax.tick_params(axis='both', which='major', labelsize=16)
plt.show()


# Beginning of advising

portfolio = []
riskyOrNot = []
priceyOrNot = []

while len(portfolio) != 10:
    portfolio.append(input("Enter company that you're interested in tickers now").upper())

cap = int(input("What is the limit for your portfolio spending?"))
risk = input("Do you prefer risky trades? (Yes or no)")
isRisky = (risk.lower() == "yes")
nToInvest = int(input("How many of these companies do you PREFERABLY want to invest in?"))


stockToShare = {}
# Get the amount of shares the user wants for each stock, check if the prices are adequate to invest
for comp in portfolio:
    stockToShare[comp] = int(input(f"How many shares of {comp} would you like to buy?"))
    # Fetch information for the closing price of each company
    req_dict = r =requests.get(f'https://api.polygon.io/v2/aggs/ticker/{comp}/prev?adjusted=true&apiKey=VFSwKNWbH7pv7Yp98ayguccA6KVAJYjr').json()
    thisClose = req_dict['results'][0]
    if float(cap/thisClose*stockToShare[comp]) > cap/nToInvest:
        priceyOrNot.append(comp)
        portfolio.remove(comp)
# Separate loop for risk factor: Needs a separate api call
for comp in portfolio:
    req_dict = r = requests.get(
        f'https://query1.finance.yahoo.com/v11/finance/quoteSummary/{comp.upper()}?modules=assetProfile').json()
    risk = req_dict['quoteSummary']['result'][0]['overallRisk']
    if risk > 4 and not isRisky or (risk <=4 and isRisky):
        portfolio.remove(comp)
        riskyOrNot.append(comp)

print("After some through analysis, we've concluded the following:")
print(f"The most pricey stocks are {print_list(priceyOrNot)}")
print(f"Based on your lack of, or desire for risk, and portfolio budget, we suggest you invest in {print_list(portfolio)}")
