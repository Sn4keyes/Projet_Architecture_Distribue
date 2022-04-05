##### DOCKERFILE FOR IMAGE PYSPARK NOTEBOOK #####
FROM jupyter/pyspark-notebook:python-3.8.8

RUN pip install numpy
RUN pip install kafka-python
RUN pip install pyspark
RUN pip install pymongo
RUN pip install nltk
RUN pip install spacy
RUN python -m spacy download en_core_web_sm