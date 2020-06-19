import pyodbc
import pandas as pd

def readFile():
    #needs own button
    try:

        conn = pyodbc.connect('Driver={SQL Server};Server=40.69.217.124,1455;Database=LaborexDB;Trusted_Connection=no;UID=Lab;PWD=Lab@2019;')
        cursor = conn.cursor()

        df = pd.read_sql_query(
        '''select * FROM LaborexDB.dbo.View_DataToForecast''', conn, parse_dates=['Date'], index_col='Date')

        df = df.rename(columns={'ProductName':'PRODUCT', 'OrderedQTY':'Sale'})
        df.index.names=['Month']
        df = df.dropna()

    except:

        df = pd.read_excel('data.xlsx')
        df = df.rename(columns={'Product Type':'Category'})
        df.index.names=['Month']

    return df


