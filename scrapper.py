import requests
from bs4 import BeautifulSoup
import re
import csv
import nltk
from nltk.tokenize.regexp import WhitespaceTokenizer
import pandas as pd
import os

def stop_words_file_creator():
    print("Creating stop words master file:")
    superset = set()
    file_name = 'Data\\stop_words_maser_file.txt'
    filelocations = ["C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_Auditor.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_Currencies.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_DatesandNumbers.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_Generic.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_GenericLong.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_Geographic.txt",
    "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Webscrapper1\\Data\\StopWords\\StopWords_Names.txt"]
    for _ in filelocations:
        with open(_) as file_obj:
            for line in file_obj.readlines():
                superset.add(line.strip().split(' |')[0])

    with open(file_name, 'w') as f:
        for _ in sorted(superset):
            f.write(f'{_}\n')
    print("Stop word Master file created successfully:")
    print(f"file name is:{file_name}")
    return file_name

def negative_positive_polarity_checker(article_file_address, stop_word_file_address):
    positive_score = 0
    negative_score = 0
    polarity_score = 0
    subjectivity_score = 0
    positivewords = set() 
    negativewords = set()
    newwords = []
    removedwords = []
    negativedict = "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Data\\MasterDictionary\\negative-words.txt"
    positivedict = "C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Data\\MasterDictionary\\positive-words.txt"
    with open(negativedict) as f:
        for _ in f:
            negativewords.add(_.strip())
    with open(positivedict) as f:
        for _ in f:
            positivewords.add(_.strip())

    with open(article_file_address) as file_obj:
        articles_tokens = WhitespaceTokenizer().tokenize(file_obj.read())

    with open(stop_word_file_address) as file_obj:
        stop_word_tokens = WhitespaceTokenizer().tokenize(file_obj.read())

    for t in articles_tokens:
        if t not in stop_word_tokens:
            newwords.append(t)
        else:
            removedwords.append(t)

    with open(negativedict) as f:
        for _ in f:
            negativewords.add(_.strip())
    with open(positivedict) as f:
        for _ in f:
            positivewords.add(_.strip())

    for _ in newwords:
        if _ in negativewords:
            negative_score -=1
        elif _ in positivewords:
            positive_score +=1
    negative_score = negative_score*-1      #We multiply the score with -1 so that the score is a positive number.
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / ((len(newwords))+0.000001)

    return positive_score, negative_score,polarity_score,subjectivity_score, len(newwords)

def number_of_sentence_counter(articlesfilepath):
    x = ""
    with open(articlesfilepath) as f:
        for line in f:
            lines= line.strip(".") # remove last period (.) if any 
            x = re.split('[.?!]',lines)
    return len(x)

def avg_sentence_length_counter(number_of_sentences):
    with open(article_file_address) as file_obj:
        articles_tokens = WhitespaceTokenizer().tokenize(file_obj.read())
    avg_sentence_length = 0
    avg_sentence_length = len(articles_tokens) /number_of_sentences
    return round(avg_sentence_length,4)

def complex_word_counter(article_file_address):
    with open(article_file_address) as file_obj:
        articles_tokens = WhitespaceTokenizer().tokenize(file_obj.read())
    number_of_complex_words = 0
    avg_number_of_complex_words = 0
    vowel_count = 0
    vowels = {'a','e','i','o','u','A','E','I','O','U'}
    for word in articles_tokens:
        vowel_count = 0
        if word.endswith("es") or word.endswith("ed"):
            vowel_count -=1
        x = re.findall("[aeiouAEIOU]", word)
        vowel_count = vowel_count + len(x)
        if vowel_count > 2:
            number_of_complex_words +=1
    avg_number_of_complex_words = round(100*(number_of_complex_words / len(articles_tokens)))
    return number_of_complex_words, avg_number_of_complex_words

def fog_index_finder(avg_sentence_length, avg_number_of_complex_words):
    fog_index = 0
    fog_index = 0.4*(avg_sentence_length + avg_number_of_complex_words)
    return fog_index

def number_of_pronoun_counter(article_file_address):
    number_of_pronoun = 0
    pronounRegex = re.compile(r'\bI\b|\bwe\b|\bWe\b|\bmy\b|\bMy\b|\bours\b|\bus\b')
    with open(article_file_address) as file_obj:
        text  = file_obj.read()
    x = pronounRegex.findall(text)
    number_of_pronoun = len(x)
    return number_of_pronoun

def avg_word_length_finder(article_file_address):
    with open(article_file_address) as file_obj:
        articles_tokens = WhitespaceTokenizer().tokenize(file_obj.read())
    avg_word_len = 0
    total_number_of_char = 0
    for word in articles_tokens:
        new_word = re.sub(r'[^\w\s]','',word)
        for alphabet in new_word:
            total_number_of_char +=1
    avg_word_len = total_number_of_char / len(articles_tokens)
    return round(avg_word_len, 3)

# Main function part of the program
data = pd.read_excel('C:\\Users\\shiva\\OneDrive\\Desktop\\Pythonprojects\\Scrapper\\Data\\Input.xlsx')
df = pd.DataFrame(data) 
for _ in df.iterrows():
    url = _[1].values[1]
    url_id = _[1].values[0]

    try:
        print("\nExtracting and saving Data from URL to file")
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
        headers = {'User-Agent': ua}
        r = requests.get(url,headers=headers).text
        soup = BeautifulSoup(r, 'lxml')
        all_data = soup.find('div', class_= 'td-post-content')
        article_file_address = "allarticles.txt"      
        with open(article_file_address,'w') as f:
            for articles in all_data.find_all('p'):
                articlestext = articles.get_text()
                f.write(articlestext)                            # get the allarticles file 
    except Exception as e :
        print(f" {e} Error- URL- {url_id} Data Load Failed: URL Skipped")
        continue

    if not os.path.isfile("Data\\stop_words_maser_file.txt"):
        stop_words_file = stop_words_file_creator()                         # get the stop word master file
    else:
        stop_words_file = "Data\\stop_words_maser_file.txt"

    positive_score, negative_score,polarity_score,subjectivity_score, word_count = negative_positive_polarity_checker(article_file_address  , stop_words_file)
    number_of_sentences = number_of_sentence_counter(article_file_address)
    avg_sentence_length = avg_sentence_length_counter(number_of_sentences)
    number_of_complex_words, avg_number_of_complex_words = complex_word_counter(article_file_address)
    fog_index = fog_index_finder(avg_sentence_length, avg_number_of_complex_words)
    number_of_pronoun = number_of_pronoun_counter(article_file_address)
    avg_word_len = avg_word_length_finder(article_file_address)
    print(f"url_id---------------|{url_id}| Data load success:") 

    headers = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
	            'AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE',
    	        'COMPLEX WORD COUNT', 'WORD COUNT', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
    if not os.path.isfile("Data\\Output.csv"):
        db1 = pd.DataFrame(columns=headers)
        db1.to_csv("Data\\Output.csv",index=False)	
        print("Data\\Output.csv Created Successfully:")
    else:
        new_data = [url_id,url,positive_score,negative_score,polarity_score,subjectivity_score,
        avg_sentence_length,avg_number_of_complex_words,fog_index,avg_sentence_length,
        number_of_complex_words, word_count,number_of_pronoun,avg_word_len]
        df = pd.DataFrame([new_data],columns=headers)
        df.to_csv("Data\\Output.csv",mode='a', index=False, header=False)   


