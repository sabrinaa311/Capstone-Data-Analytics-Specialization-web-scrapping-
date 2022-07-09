from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
data = soup.find('div',attrs={'class':'table-responsive'} )
rowdata= data.find_all('tr')

row_length = len(rowdata)

temp = [] #initiating a list 

for i in range(0, 130):
    exchange = data.find_all('tr')[i] #1 take data from all rows completely
    
    date = exchange.find_all('td')[0].text #2 take data that contain date from all rows
    
    price = exchange.find_all('td')[2].text #3 take data that contain price from all rows
    
    temp.append((date,price))
temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns=('Date', 'Price (IDR)'))

#insert data wrangling here
df['Date'] = df['Date'].astype('datetime64')
df['Price (IDR)'] = df['Price (IDR)'].str.replace('IDR', '')
df['Price (IDR)'] = df['Price (IDR)'].str.replace(',', '')
df['Price (IDR)'] = df['Price (IDR)'].astype('float64')
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Price (IDR)"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)