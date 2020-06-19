from dbase import readFile
import pandas as pd
import numpy as np
import itertools
import time
from sklearn.preprocessing import RobustScaler()


def DataProcessing(self):

    data = readFile()

    data = data.dropna()

    product_dictionary = {}

    products = list(data.PRODUCT.unique())

    for product in products:
        product_dictionary["df_{}".format(product)] = data[data['PRODUCT']==product]

    return product_dictionary


def DataPreparation(self):
    #might want to use self keyword to access dictionary
    data = self.DataProcessing()

    feature_columns = ['AV3MT01', 'AV6MT01']

    feature_transformer = RobustScaler()
    sales_transformer = RobustScaler()

    for item in data:
        data["{}".format(item)]['Month'] = data["{}".format(item)].index.month
        #
        #For Data Split
        #
        train_size = int(len(data["{}".format(item)].drop(columns=['PRODUCT'], axis=1)) * 0.75)
        test_size = len(data["{}".format(item)]) - train_size
        train, test = data["{}".format(item)].iloc[0:train_size], data["{}".format(item)].iloc[train_size:len(data["{}".format(item)])]
        train, test = train.drop(columns='PRODUCT'), test.drop(columns='PRODUCT')

        # 
        # For Data transformation and scaling
        # 
        try:
            
            feature_transformer = feature_transformer.fit(train[feature_columns].to_numpy())
            sales_transformer = sales_transformer.fit(train[['Sale']])
            
            train.loc[:, feature_columns] = feature_transformer.transform(train[feature_columns].to_numpy())
            train['Sale'] = sales_transformer.transform(train[['Sale']])

            test.loc[:, feature_columns] = feature_transformer.transform(test[feature_columns].to_numpy())
            test['Sale'] = sales_transformer.transform(test[['Sale']])
        except:
            print('ValueError: Found array with 0 sample(s)')

        TIME_STEPS = 3
        
        if train.shape[0] < 20 and test.shape[0] < 9:
            pass
        elif train.shape[0] >= 20 and test.shape[0] >= 9:
            X_train, y_train = self.create_data(train, train.Sale, time_steps=TIME_STEPS)
            X_test, y_test = self.create_data(test, test.Sale, time_steps=TIME_STEPS)

    return #some list or dictionary

        

        
def create_data(self, X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i: (i + time_steps)].to_numpy()
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])

    return np.array(Xs), np.array(ys)

    

