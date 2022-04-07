import torch
import pandas as pd
import numpy as np
import re
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

####################################### Modèle de BERT #######################################

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def main():
    com = input("WWrite your comment:")
    res = model(com)
    print(res)
    note = int(torch.argmax(res.logits)) + 1
    print(note)
    return(res, note)

if __name__ == "__main__":
    main()