import streamlit as st
import numpy as np
import pandas as pd
import os
import re
import utilities
import matplotlib
import matplotlib.pyplot as plt

#Visuels
#Main Panel
st.title('ECN Results Analysis')

graph_selection = st.selectbox(
    "Choissisez un graphique :",
    ("Carte Thermique ", "Boites à Moustaches", "Résulats par Ville à travers le temps","Résulats par Spécialité à travers le temps")
)

annee_selection = st.slider('Plage de date',min_value=2010,max_value=2020,value=(2010, 2020))

#st.checkbox("Filtre par Ville",)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#Side Panel
st.sidebar.title('Contexte')

st.sidebar.write('Aux cours des études de Médecine française, les élèves de tous les pays se mesurent les uns aux autres dans un concours national à la fin de la 6ème\
    : l\'ECN. A la suite de ce concours, les élèves choissisent une ville et une spécialité dans l\'ordre des résultats. \
        Ce projet essaie de faciliter la compréhension des résultats des 10 dernières années intuitivement.')


language = st.sidebar.selectbox(
    "Selectionnez une langue",
    ("Français", "English")
)



#Step 1- Make sure Input file is good 
#df = utilities.find_unclean_input(2010)

#Step 2- Trasnform Raw data to clean data
#df = utilities.raw_to_cleaned(2010)

#Step 3- Inspect Clean Data to homogenize it. Especially Ville and Specialite
#df = utilities.show_column_values("specialite")
df_final= utilities.cleaned_to_aggregates_latest_spot()
df_final.to_csv(f'data/2_aggregates/agg_latest_spot.csv', index=True)

#Part 2 - Use CSV
#df = pd.read_csv('trd_files/trd_resultats_2010_11.csv', index_col=0)
#df_rfd_01 = utilities.create_df_lastest_spot(df)

#t.write(df_rfd_01)
#st.table(df_rfd_01)
#list(df.index.values) 
#list(df.columns) 

#df_rfd_01_np = df_rfd_01.to_numpy()
#st.write(type(df_rfd_01_np))

