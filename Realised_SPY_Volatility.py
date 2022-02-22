import pandas as pd
import math
import matplotlib.pyplot as plt


def create_dataframes():
	return [pd.read_csv("SPY_RealVol.csv", usecols=["S&P 500 1-Month Realized Volatility Index"]), pd.read_csv("VIX.csv", usecols=["Adj Close"])]


def edge_per_IV(df1, df2) -> list[float]:
	avg_edges = []
	for min_tradable_IV in range(0, 40, 2):
		VIX, thirty_day_vol = [], []
		for i, vol in enumerate(df2["Adj Close"]):
			if vol > min_tradable_IV:
				VIX.append(vol)
				thirty_day_vol.append(df1.loc[i,"S&P 500 1-Month Realized Volatility Index"])

		edge = [(VIX[i] - thirty_day_vol[i]) for i in range(len(VIX))]
		avg_edge = sum(edge) / len(edge)
		avg_edges.append((min_tradable_IV, avg_edge))

	return avg_edges


def format_data(df1, df2, min_tradable_IV: int) -> list[list]:

	VIX, thirty_day_vol = [], []
	for i, vol in enumerate(df2["Adj Close"]):
		if vol > min_tradable_IV:
			VIX.append(vol)
			thirty_day_vol.append(df1.loc[i,"S&P 500 1-Month Realized Volatility Index"])


	edge = [(VIX[i] - thirty_day_vol[i]) for i in range(len(VIX))]
	avg_edge = sum(edge) / len(edge)

	return [VIX, thirty_day_vol, edge, avg_edge]

	
def plot(VIX, thirty_day_vol, edge, avg_edge):
	plt.style.use('ggplot')

	plt.subplot(2, 1, 1)
	plt.plot(thirty_day_vol, label="SPY Realized Volatility")
	plt.plot(VIX, label="SPY Implied Volatility")

	plt.legend()
	plt.xlabel('Days') 
	plt.ylabel('30 Day Implied/Realized Volatility') 
	plt.title("S&P 500 1-Month Implied vs Realized Volatility (1/31/2012 - 2/17/2022)")

	plt.subplot(2, 1, 2)
	days = list(range(1, len(edge) + 1))
	plt.bar(days, edge)
	plt.axhline(y=avg_edge, color='b', linestyle=':', label=f"Average edge: {round(avg_edge, 4)}")

	plt.legend()
	plt.xlabel('Days') 
	plt.ylabel('30 Day Implied Vol - Realized Vol') 

	plt.show()

df1, df2 = create_dataframes()

edges = edge_per_IV(df1, df2)
for i in edges:
	print(f"IV: {i[0]}, Edge: {round(i[1], 4)}\n")

VIX, thirty_day_vol, edge, avg_edge = format_data(df1, df2, min_tradable_IV=10)
plot(VIX, thirty_day_vol, edge, avg_edge)