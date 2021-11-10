# ouverture du fichier stopwords_fr
stopwordsfile = "stopwords_fr.txt"
# Récupération de la liste des mots vides
stopwords_list = open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

ponctuation_list = ['?', '.', '!', '<', '>', '}', '{', ':', '(', ')', '[', ']', '\"', ',', '-', "»", "«", '\'', '’',
                    '#', '+', '_', '-', '*', '/', '=']


# Eliminer les mots vides et la ponctuation

def Stopword_elimination(text):
    word_list = []
    # Eliminer la punctuation
    for character in ponctuation_list:
        text = text.replace(character, ' ')

    # str -> list
    words = text.split()
    for word in words:
        if word.lower() not in stopwords_list:
            word_list.append(word.lower())
    return word_list


# Dictionnaire des fréquences

def dict_freq(word_list):
    frequence_dict = {}
    for word in word_list:
        if word not in frequence_dict:
            frequence_dict[word] = word_list.count(word)
    return frequence_dict


def all_freq(n):  # n est le nombre des documents txt
    i = 1
    frequences = {}
    while (i <= n):
        with open('D' + str(i) + '.txt', 'r', encoding='utf-8') as file:
            lines = file.read()
            data = Stopword_elimination(lines)
            frequences[i] = dict_freq(data)
        file.close()
        print(i, ":", frequences[i])
        i = i + 1


# Création des dictionnaires ( pour 4 documents )
all_freq(4)
