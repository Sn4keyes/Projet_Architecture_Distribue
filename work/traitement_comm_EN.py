#!/usr/bin/python

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import spacy
import nltk
import re

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")
lemmer = WordNetLemmatizer()

def tokenise(comment):
    # Enlève tout ce qui n'est pas mot ou espace
    comm = re.sub(r"[^\w\s]'",'',comment)
    # conserve les caractères importants
    comm = re.sub('[^a-zA-Zàèéêîïâäëôö0-9 ]', '', comm)
    # enlève les caractères en double
    comm = re.sub('(.)\\1{2,}', "\\1", comm)
    # tout en minuscule
    comm = comm.lower()
    # Tokeniser la phrase
    doc = nlp(comm)
    # Retourner le texte de chaque token
    return [X.text for X in doc]

stopWords = set(stopwords.words('english'))

def lemming(comment):
    doc = nlp(comment)
    return [lemmer.lemmatize(X.text) for X in doc]

def main(comment):
    com = tokenise(comment)
    lem_com = ''
    for token in com:
        if token not in stopWords:
            lem_com = lem_com + ' ' + token
    return(lem_com)

if __name__ == "__main__":
    main()