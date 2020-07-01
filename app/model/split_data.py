from processing import readFile

import matplotlib.pyplot as plt


new_data, date = readFile()

def split_set():

    train_date = date[:int(len(new_data)*0.75)]
    train = new_data[:int(len(new_data)*0.75)].copy()

    test_date = date[int(len(new_data)*0.75):]
    test = new_data[int(len(new_data)*0.75):].copy()

    print(f'Train shape {train.shape}, Test shape {test.shape}')

    return train_date, train, test_date, test

def plot_split_set(name):

    train_date, train, test_date, test = split_set()    
    
    plt.figure(figsize=(16,4))

    plt.plot(train_date, train[name], label='train')
    plt.plot(test_date, test[name], label='test')
    plt.ylabel(name); plt.legend()
    plt.show()
