import streamlit as st
import numpy as np
import pandas as pd
import os
import re
import utilities
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('data/2_aggregates/agg_latest_spot.csv', index_col=0)
all_ville = df.ville.unique().tolist()
all_specialite = df.specialite.unique().tolist()
liste_ville = all_ville
liste_specialite = all_specialite

### Visuels ###
#Main Panel
st.title('ECN Results Analysis')

graph_selection = st.selectbox(
    "Choissisez un graphique :",
    ("Carte Thermique ", "Boites à Moustaches", "Résulats par Ville à travers le temps","Résulats par Spécialité à travers le temps")
)

annee_selection = st.slider('Plage de date',min_value=2010,max_value=2020,value=(2010, 2020))

filtreVille_bool = st.radio('Filtre par Ville', ['Toutes les villes','Appliquer un filtre'], index = 0)

if filtreVille_bool == "Appliquer un filtre":
    liste_ville = st.multiselect('Selectionnez les villes que vous souhaitez garder:',options=all_ville, default=all_ville)


filtreSpecialite_bool = st.radio('Filtre par Spécialite', ['Toutes les spécialites','Appliquer un filtre'], index = 0)

if filtreSpecialite_bool == "Appliquer un filtre":
    liste_specialite = st.multiselect('Selectionnez les spécialités que vous souhaitez garder:',options=all_specialite, default=all_specialite)



#Side Panel
st.sidebar.title('Contexte')

st.sidebar.write('Aux cours des études de Médecine française, les élèves de tous les pays se mesurent les uns aux autres dans un concours national à la fin de la 6ème\
    : l\'ECN. A la suite de ce concours, les élèves choissisent une ville et une spécialité dans l\'ordre des résultats. \
        Ce projet essaie de faciliter la compréhension des résultats des 10 dernières années intuitivement.')


language = st.sidebar.selectbox(
    "Selectionnez une langue",
    ("Français", "English")
)

#######


#Step 1- Make sure Input file is good 
#df = utilities.find_unclean_input(2010)

#Step 2- Trasnform Raw data to clean data
#for year in range(2010,2021):
#    st.write(year)
#    utilities.raw_to_cleaned(year)

#Step 3- Inspect Clean Data to homogenize it. Especially Ville and Specialite
#df = utilities.show_column_values("specialite")
#df_final= utilities.cleaned_to_aggregates_latest_spot()
#df_final.to_csv(f'data/2_aggregates/agg_latest_spot.csv', index=True)

### Show chart based on inputs ###

with st.beta_expander("See explanation"):
    st.write("The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")
