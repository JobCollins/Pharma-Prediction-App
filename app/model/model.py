from processing import readFile

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf 
from statsmodels.tsa.seasonal import seasonal_decompose 
from pmdarima import auto_arima                        
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse

new_data = readFile()

def plot_seasonality(name):
    a = seasonal_decompose(new_data[name], model = "add")
    plt.figure(figsize = (16,7))
    a.seasonal.plot();

def build_model(name):
    auto_arima(new_data[name], seasonal=True, m=12,max_p=7, max_d=5,max_q=7, max_P=4, max_D=4,max_Q=4).summary()
    arima_model = SARIMAX(train[name], order = (2,1,1), seasonal_order = (4,0,3,12))
    arima_result = arima_model.fit()
#     arima_result.summary()
    
    arima_pred = arima_result.predict(start = len(train), end = len(new_data)-1, typ="levels").rename("ARIMA Predictions")
    
    test[name].plot(figsize = (16,5), legend=True)
    arima_pred.plot(legend = True);
    
    return arima_pred

def model_performance(name):
    
    arima_pred = build_model(name)
    
    arima_rmse_error = rmse(test[name], arima_pred)
    arima_mse_error = arima_rmse_error**2
    mean_value = new_data[name].mean()

    print(f'MSE Error: {arima_mse_error}\nRMSE Error: {arima_rmse_error}\nMean: {mean_value}')
    
    model_df = pd.DataFrame(arima_pred)
    model_df['Actual'] = test[name]
    model_df['ActualvsARIMA'] = model_df['ARIMA Predictions'] - model_df['Actual']
    
    return model_df

