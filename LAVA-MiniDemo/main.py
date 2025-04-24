from BERTController import process_text, process_paragraph_by_index
import nltk
nltk.download('punkt')
from Utils import id2label

text = "TP53 regulates MDM2 expression in cancer cells."
entities, relations, graph_file = process_text(text, id2label)

text = "Aspirins cures fever."
entities, relations, graph_file = process_text(text, id2label)

# Dataset: https://www.kaggle.com/datasets/chaitanyakck/medical-text

process_paragraph_by_index(1, filepath="text/dataset.dat", id2label=id2label)

process_paragraph_by_index(range(2, 4), filepath="text/dataset.dat", id2label=id2label)

process_paragraph_by_index([5, 7, 9], filepath="text/dataset.dat", id2label=id2label)