import os
import pandas as pd
import numpy as np
import glob


def data_cleanup():
    if os.path.exists(os.path.join('Data', 'clean_files.txt')):
        with open(os.path.join('Data', 'clean_files.txt')) as f:
            return f.read().split('\n')
    # Read all files and remove the ones that are empty or contain only 1 line and the header
    all_files = glob.glob(os.path.join('Data', 'Stocks', '*.txt'))
    li = []
    for filename in all_files:
        if os.stat(filename).st_size == 0:
            print(filename)
            li.append(filename)
            continue
        with open(filename) as f:
            i = 0
            for i, _ in enumerate(f):
                if i >= 2:
                    break
            if i < 2:
                print(filename)
                li.append(filename)
    for f in li:
        all_files.remove(f)

    with open(os.path.join('Data', 'clean_files.txt'), 'w') as f:
        f.write("\n".join(all_files))
    return all_files


def read_dataset():
    if os.path.exists(os.path.join('data', 'stocks.csv')):
        stocks = pd.read_csv(os.path.join('data', 'stocks.csv'), parse_dates=['Date'])
        print(stocks.head(5))
    else:
        all_files = data_cleanup()
        li = []
        for f in all_files:
            print(f)
            # Get the company id from the file path
            company_id = os.path.split(f)[1].split('.')[0].upper()
            # Read the CSV and parse the dates as datetime
            temp = pd.read_csv(f, parse_dates=['Date'])
            # Add column which contains the company id
            temp['Company_Id'] = company_id
            li.append(temp)
        # Concatenate list as a single dataframe
        stocks = pd.concat(li)
        stocks.to_csv(path_or_buf=os.path.join('data', 'stocks.csv'), index=False)
    return stocks


if __name__ == '__main__':
    stocks = read_dataset()
