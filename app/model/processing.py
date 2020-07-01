import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def readFile():

    data = pd.read_excel('data.xlsx')
    data = data.drop(columns=['NOART', 'ENROUTE'])

    new_data = data.pivot_table(index='Month', columns='PRODUCT', values='Sale')
    new_data.columns.name = None

    date = new_data.index.values

    return new_data, date


def plot_product(name):

    new_data, date = readFile()

    plt.figure(figsize=(16,4))
    
    plt.plot(date, new_data[name])
    plt.xlabel('Time')
    plt.ylabel('Sale')
    plt.title(f'Sales for {name}')
    plt.show()