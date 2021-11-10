from exercice1 import inverse_file

df = inverse_file()
df.set_index("Term", inplace = True)
df.sort_index(axis = 0)
print(df)
def access_by_doc_number(doc_number):
	document = 'D' + str(doc_number)
	return df.loc[:,['Term', document]]

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
			print("======= Which document you want to see its frequencies ? =======")
			doc_number = input()
			if doc_number in doc_numbers:
				print(access_by_doc_number(doc_number))	
			else:
				print("======= There's not such document =======")
	else:
		while True:
			print("======= Which term you want to see its frequencies ? =======")	
			term = input()
			if term in df.index:
				print(access_by_term(term))
			else:
				print("======= There's not such term =======")			
else:
	print("======= Wrong choice =======")	
