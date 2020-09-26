#@author: John Bumgardner

import pandas
import numpy as np



def compute_gains(asset1, asset2, h1, h2):
	prev_price_asset_1 = float(asset1[0])
	prev_price_asset_2 = float(asset2[0])
	x1 = []
	x2 = []
	for i in range(1, len(asset1)):
		curr_price_asset_1 = float(asset1[i])
		curr_price_asset_2 = float(asset2[i])
		gain_1 = curr_price_asset_1 - prev_price_asset_1
		gain_2 = curr_price_asset_2 - prev_price_asset_2
		x1.append(gain_1)
		x2.append(gain_2)
		prev_price_asset_1 = curr_price_asset_1
		prev_price_asset_2 = curr_price_asset_2
	r1 = 0
	r2 = 0
	for x_n in x1:
		r1 += x_n * h1
	for x_n in x2:
		r2 += x_n * h2

	return r1 + r2



def max_for_2_companies(name1, name2):
	asset_1 = company[name1]
	asset_2 = company[name2]
	asset_1_prices = []
	asset_2_prices = []
	for i in range(0, len(asset_1)):
		if i % 2 == 1:
			asset_1_prices.append(asset_1[i])
	for i in range(0, len(asset_2)):
		if i % 2 == 1:
			asset_2_prices.append(asset_2[i])
	max_return = 0
	max_h = 0
	for h in np.linspace(0,1,101): 
		h1 = h
		h2 = 1 - h
		returns = compute_gains(asset_1_prices, asset_2_prices, h1, h2)
		if returns > max_return:
			max_return = returns
			max_h = h1

	# For two assets, Microsoft and Goldman Sachs
	print("Max return: " + str(max_return) + " at h1 = " + str(max_h) + " and h2 = " + str(1-max_h))
	return [max_return, h1, h2, name1, name2]


df = pandas.read_csv('asset_prices.csv')
company = {}
for i in df:
	company[i] = df[i]

max_return = 0
h1 = 0
h2 = 0
name1 = ""
name2 = ""
names = list(company.keys())
for i in range(0, len(names) - 1):
	for j in range(i, len(names)):
		if names[i] != names[j]:
			vals = max_for_2_companies(names[i], names[j])
			if vals[0] > max_return:
				max_return = vals[0]
				h1 = vals[1]
				h2 = vals[2]
				name1 = vals[3]
				name2 = vals[4]

print("---------For D = 2---------")
print("Invest " + str(h1) + " in "+ name1)
print("Invest " + str(h2) + " in "+ name2)
print("Max return of $" + str(max_return))

