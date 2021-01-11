import glob
import re
import pandas as pd

files = glob.glob("*.txt")
print(files)

with open(files[0], 'r') as file:
    giant_string = file.read()
    
# print(giant_string)

ticker_symbols = re.findall('[$].{,5}[.]{1}',giant_string)
#What this regex is saying is:
    #We are looking for any instance of a literal $ followed by up to 5 characters (longest length of a ticker symbol) and then followed by one literal '.'
dates = re.findall('__.{,11}\s\d+[}]', giant_string)
#This regex says: we are looking for any instance of '__' followed by up to 11 characters (longest month (September, plus our two __) that precede a space.
    #That space must then be followed by a number and finally end with a bracket.
opening_prices = re.findall('::\d+\.\d+',giant_string)
#This regex searches for: two colons followed by any number of numbers followed by exactly one . and then any number of numbers (this could also be set to just two numbers)
company_names = re.findall('(?!-{3,})(--.+--)', giant_string)
#This regex includes any exclusion statement that says: do not include any information that is between 3 or more hyphens. If that condition is not met, then look for 
# Any characters between two sets of --

for number, (symbol, date, price, name) in enumerate(zip(ticker_symbols, dates, opening_prices, company_names)):
    print(number, symbol, date, price, name)
    
for number, (symbol, date, price, name) in enumerate(zip(ticker_symbols, dates, opening_prices, company_names)):
    ticker_symbols[number] = re.sub('\$|\.','',symbol) #Replace all literal $ or literal . with nothing
    dates[number] = re.sub('__|\}','',date) #Replace all __ or curly end brackets with nothing
    opening_prices[number] = float(re.sub('::','',price)) #You see the trend now, but this time we are casting that result as a float
    company_names[number] = re.sub('--','',name)
    
for number, (symbol, date, price, name) in enumerate(zip(ticker_symbols, dates, opening_prices, company_names)):
    print(number, symbol, date, price, name)
    
    
stock_data = pd.DataFrame([ticker_symbols, dates, opening_prices, company_names], index = ['Ticker Symbol','Date','Opening Price (USD)','Company Name'])
#First we will put our data into a dataframe to make use of a nifty Pandas demo
print(stock_data.head())
print('-'*60)
stock_data = stock_data.transpose()
#I prefer my data to expand into the rows, not the column
print(stock_data.head())

stock_data.to_excel('Stock_Data.xlsx', index = False) #Write the dataframe to excel without the index. Our index contains no unique information
