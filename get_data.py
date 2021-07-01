import pandas as pd

csv_path = './follows.csv'

def get_data(path=csv_path):
    duwei = 0
    dd = 0
    close = 0
    follows = pd.read_csv(path)
    list = follows.values.tolist()
    for peo in list:
        if peo[5] == 0:
            close = close + 1
        else:
            sum = 0
            for i in range(1,5):
                sum = sum + peo[i]
            if sum == 4:
                dd = dd + 1
            elif sum == 0:
                duwei = duwei + 1
    print('close: %d, dd: %d, duwei: %d' %(close, dd, duwei))

if __name__ == '__main__':
    get_data()