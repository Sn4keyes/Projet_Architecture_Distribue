#!/usr/bin/python

from pymongo import MongoClient
from sqlite3 import Connection
import traitement_comm_EN
from http import client
import streamlit as st
import pandas as pd
import numpy as np
import lineaire
import sqlite3
import bert

MODEL1 = "Linear"
MODEL1_2 = "Linear Bis"
MODEL2 = "Bert"
MODEL3 = "WordToVec"
MODEL4 = "CBOW"

########## MODELS COMMUNICATION ##########
def get_cbow_model(comment):
    res = 'Sorry there are no results'
    return res

def get_word_to_vec_model(comment):
    res = 'Sorry there are no results'
    return res

def get_bert_model(comment):
    res = bert.main(comment)
    return res

def get_linear_bis_model(comment):
    res = 'Sorry the are no results'
    return res

def get_linear_model(comment):
    res = lineaire.main(comment)
    return res

def send_comment_to_model(comment, model):
    if model == MODEL1:
        model_res = get_linear_model(comment)
    elif model == MODEL1_2:
        model_res = get_linear_bis_model(comment)
    elif model == MODEL2:
        model_res = get_bert_model(comment)
    elif model == MODEL4:
        model_res = get_word_to_vec_model(comment)
    else:
        model_res = get_cbow_model(comment)
    return model_res
########## ########## ##########

########## MODELS ##########
def fourth_model():
    st.subheader("Modèle 5 : CBOW")
    st.warning('Sorry this model is not yet implemented.')
    st.text("Entrer un commentaire pour prédire le prochain mot selon le context d'une phrase.")
    with st.form("form_cbow"):
        comment_cbow = st.text_area("Comment for CBOW model", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            model_res = send_comment_to_model(comment_cbow, MODEL4)
            st.write("Result of model : ", model_res)

def third_model():
    st.subheader("Modèle 4 : WordToVec")
    st.warning('Sorry this model is not yet implemented.')
    st.text("Entrer un commentaire pour calculer la distance entre les mots de votre\ncommentaire et des mots appartenant aux vocabulaire classifié par notre model.")
    with st.form("form_word_to_vec"):
        comment_word_to_vec = st.text_area("Comment for WordToVec model", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            model_res = send_comment_to_model(comment_word_to_vec, MODEL3)
            st.write("Result of model : ", model_res)

def second_model():
    st.subheader("Modèle 3 : Bert")
    st.text("Entrer un commentaire pour détecter si un commentaire est Positif ou Négatif.\nEtablir sa note de 1 à 5 et les probabilités de chaque note.")
    with st.form("form_bert"):
        comment_bert = st.text_area("Comment for Bert model", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            model_res = send_comment_to_model(comment_bert, MODEL2)
            st.write("Result of model : ")
            st.write(model_res)

def first_bis_model():
    st.subheader("Modèle 2 Bis : Linéaire/Spark")
    st.warning('Sorry this model is not yet implemented.')
    st.text("Entrer un commentaire pour détecter si un commentaire est Positif ou Négatif.")
    with st.form("form_linear_bis"):
        comment_linear_bis = st.text_area("Comment for Linear model with Spark", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            model_res = send_comment_to_model(comment_linear_bis, MODEL1_2)
            st.write("Result of model : ")
            st.write(model_res)

def first_model():
    st.subheader("Modèle 1 : Linéaire")
    st.text("Entrer un commentaire pour détecter si un commentaire est Positif ou Négatif.")
    with st.form("for_linear"):
        comment_linear = st.text_area("Comment for Linear model", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            model_res = send_comment_to_model(comment_linear, MODEL1)
            state_res = int(model_res[0])
            st.write("Result of model : ")
            if state_res == 1:
                st.write("Ceci est un commentaire positif")
            else:
                st.write("Ceci est un commentaire négatif")
            st.write(model_res)
########## ########## ##########

########## FRONT ##########
def build_sidebar():
    with st.sidebar:
        st.title("Credits :")
        st.header("project produced by :")
        st.write("- **Mathieu Ly-Wa-Hoi**")
        st.write("- **BARRY Mamadou Djoulde**")
        st.write("- **Hugo Chantelot**")

def manage():
    build_sidebar()
    st.title("Project Architecture Distribué")
    first_model()
    first_bis_model()
    second_model()
    third_model()
    fourth_model()
########## ########## ##########

########## MAIN ##########
@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

def main():
    client_connect = MongoClient('mongo', 27017, username = 'root', password = 'root')
    manage()
    return client_connect

if __name__ == "__main__":
    client_connect = main()
########## ########## ##########