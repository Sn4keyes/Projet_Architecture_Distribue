from transformers import AutoTokenizer, AutoModelForSequenceClassification
from traitement_comm_EN import main as traitement
import pandas as pd
import numpy as np
import torch
import re
import os

####################################### Modèle de BERT #######################################

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
EXAMPLE_BAD = "I don't like this movie"
EXAMPLE_GOOD = "I really like this movie"

def main(comment):
    com = traitement(comment)
    com = tokenizer.encode(com, return_tensors = 'pt')
    res = model(com)
    print(res)
    note = int(torch.argmax(res.logits)) + 1
    print(note)
    return(res, note)

if __name__ == "__main__":
    main()