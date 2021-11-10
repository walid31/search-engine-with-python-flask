import pandas as pd

# Ponctuations
ponctuation_list = ['?', '.', '!', '<', '>', '}', '{', ':', '(', ')', '[', ']', '\"', ',', '-', "»", "«", '\'', '’',
                    '#', '+', '_', '-', '*', '/', '=']

# stop words
stopWords_list = open('stopwords_fr.txt', 'r', encoding = "utf-8").read().splitlines()

# number of documents
NBR_DOC = 4 

# elimination of stop words and ponctuations of a document
def stopWord_elimination(document):
	words = []

	for char in ponctuation_list:
		document = document.replace(char, " ")

	# create a list of words from the document
	document = document.lower().split()

	# eliminate stop words
	for word in document:
		if word not in stopWords_list :
			words.append(word)
	return words		

# frenquency calculation
def frequency(document):
	data = []

	for word in document:
		if word not in data:
			data.append([word, document.count(word)])

	return pd.DataFrame(data, columns=['Term', 'Frequency'])

# calculate all frequencies
def all_frequencies(nbr_documents):
	i = 1
	while i <= nbr_documents:
		path = 'D' + str(i) + '.txt'
		document = open(path, 'r', encoding = "utf-8").read()
		freq = frequency(stopWord_elimination(document))				
		print('Document N' + str(i) + ': \n' ,freq)
		i += 1

# all_frequencies(4)

# merge all documents
def merge():
	i = 1
	merge = ''
	while i <= NBR_DOC:
		path = 'D' + str(i) + '.txt'
		document = open(path, 'r', encoding = "utf-8").read()
		merge += document 
		i += 1 
	words = stopWord_elimination(merge)

	merge = []
	for item in words:
		if item not in merge:
			merge.append(item)
	return merge	

# calculate frequency of one term in a document
def term_frequency(term, document):
	
	return document.count(term)


# construction du fichier inverse
def inverse_file():
	words = merge()
	inverse_file = []
	for word in words:
		i = 1
		instance = [word]
		while i <= NBR_DOC:

			path = 'D' + str(i) + '.txt'
			document = open(path, 'r', encoding = "utf-8").read()
			document = stopWord_elimination(document)
			instance.append(term_frequency(word, document))
			i += 1
		inverse_file.append(instance)
	
	return pd.DataFrame(inverse_file, columns=['Term', 'D1', 'D2', 'D3', 'D4'])
print(inverse_file())

