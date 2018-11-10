import pandas as pd

test = pd.read_csv("test.csv")
train = pd.read_csv("train.csv")

print("Dimensions of train: {}".format(train.shape))
print("Dimensions of test: {}".format(test.shape))