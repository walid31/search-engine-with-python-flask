from exercice3 import inverse_weighted_file

df = inverse_weighted_file()
print(df)

# get weights by document number
def access_by_doc_number(doc_number):
	document = 'D' + str(doc_number)
	return df.loc[:,[document]]

# get weights by term
def access_by_term(term):

	return df.loc[term]
doc_numbers = ['1','2','3','4']
doc_number = '1'

print("======= Do you want to search by Document or Term ? =======")
print("======= 1: Document =======")
print("======= 2: Term =======")
choice = input()
if choice in ['1','2']:
	if choice == '1':
		while doc_number in doc_numbers:
			print("======= Which document you want to see its weights ? =======")
			doc_number = input()
			if doc_number in doc_numbers:
				print(access_by_doc_number(doc_number))	
			else:
				print("======= There's not such document =======")
	else:
		while True:
			print("======= Which term you want to see its weights ? =======")	
			term = input()
			if term in df.index:
				print(access_by_term(term))
			else:
				print("======= There's not such term =======")			
else:
	print("======= Wrong choice =======")	
