from processing import readFile
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import matplotlib
import matplotlib.pyplot as plt
import itertools

new_data, date = readFile()

p = d = q = range(0, 2)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
param_search = {}

def parameter_search(name):
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(new_data[name].resample('MS').mean(),
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
    #             param_search['ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal)] = results.aic
#                 print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                key = 'ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic)
                param_search[key] = results.aic
            except:
                continue
    return param_search

def min_AIC(dictionary):
    key_min = min(param_search.keys(), key=(lambda k: param_search[k]))
    orders = tuple(map(int, key_min[6:13].split(', ')))
    season = tuple(map(int, key_min[16:27].split(', ')))
    
    return orders, season

def fit_model(name):
    param_search = parameter_search(name)
    orders, season = min_AIC(param_search)
    mod = sm.tsa.statespace.SARIMAX(new_data[name].resample('MS').mean(),
                                order=orders,
                                seasonal_order=season,
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()
    
    return results

def validate_forecast(name):
    results = fit_model(name)
    pred = results.get_prediction(start=pd.to_datetime('2018-01-01'), dynamic=False)
    pred_ci = pred.conf_int()
    y=new_data[name].resample('MS').mean()
    ax = y['2015':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Drug Sales')
    plt.legend()
    plt.show()
    y_forecasted = pred.predicted_mean
    y_truth = y['2017-01-01':]

    # Compute the mean square error
    mse = ((y_forecasted - y_truth) ** 2).mean()
    rmse = round(np.sqrt(mse), 2)
    
    return mse, rmse

def predictions(name):
    results = fit_model(name)
    pred_uc = results.get_forecast(steps=10)
    pred_ci = pred_uc.conf_int()
    
    y = new_data[name]
    # ax = y.plot(label='observed', figsize=(14, 7))
    # pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    # ax.fill_between(pred_ci.index,
    #                 pred_ci.iloc[:, 0],
    #                 pred_ci.iloc[:, 1], color='k', alpha=.25)
    # ax.set_xlabel('Date')
    # ax.set_ylabel('Drug Sales')

    # plt.legend()
    # # plt.show()
    
    pred_values = pred_uc.predicted_mean
    predict_df = pd.DataFrame(pred_values)
    predict_df.columns = ['Prediction']
    
    return predict_df