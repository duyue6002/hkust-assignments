import os
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))

taxi = pd.read_csv(DIR + "/taxi_train.csv", sep=',', nrows=10)
taxi.head(10)
