from exercice1 import inverse_file
import numpy as np
import pandas as pd

# get the inverse file
df = inverse_file()

# set the terms as index
df.set_index("Term", inplace = True)


# number of documents
N = 4


# get the frequency of a term in a document
def freq(term, document):
	return int(df.loc[term][document])

# get the max frequency of a document 
def Max(document):
	return df[document].max()

# get number of documents which contain a term
def n(term):

	return (df.loc[term] != 0).astype(int).sum() 

# calculate the weight of a term in a document
def weight(term, document):
	return "%.2f" % (freq(term, document) / Max(document) * np.log10((N / n(term) + 1)))

# print(weight('représentation', 'D3'))	

# calculate inverse weighted file
def inverse_weighted_file():
	inverse_weighted_file = df.astype(float)
	for col in list(df.columns):
		for row in list(df.index):
			inverse_weighted_file.at[row, col] = weight(row, col)
	return inverse_weighted_file
	
# print(inverse_weighted_file())