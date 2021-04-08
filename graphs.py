"""
#import matplotlib
#import plotly
#from plotly import tools
#import plotly.offline as py
#import plotly.figure_factory as ff 
"""
import os
import re
import utilities
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from joypy import joyplot
from matplotlib import cm

def showgraph(graph_selection, liste_annee, liste_ville, liste_specialite):
    if graph_selection =="Carte Thermique":
        df = pd.read_csv('data/2_aggregates/agg_latest_spot.csv', index_col=0)
        df = df[df.ville.isin(liste_ville)&df.specialite.isin(liste_specialite)&df.annee.isin(liste_annee)]

        fig = px.density_heatmap(df, x="ville", y="specialite", z="classement", histfunc="avg")
        st.plotly_chart(fig,use_container_width=True)

    if graph_selection =="Boites à Moustaches":
        st.write("WIP")

    if graph_selection =="Résulats par Ville à travers le temps":
        df= df.groupby(['ville','annee']).max()
        df = df.reset_index(level=['ville','annee'])
        st.write(df)

        fig = px.line(df, x="annee", y="classement", color='ville')
        st.plotly_chart(fig,use_container_width=True)

    if graph_selection =="Résulats par Spécialité à travers le temps":
        fig = px.line(df, x="annee", y="classement", color='specialite')
        st.plotly_chart(fig,use_container_width=True)

    
    if graph_selection =="Lignes de crêtes par Ville":
        df_full = pd.read_csv('data/2_aggregates/full.csv', index_col=0)
        df_full = df_full[df_full.ville.isin(liste_ville)&df_full.specialite.isin(liste_specialite)&df_full.annee.isin(liste_annee)]
        plt.figure()
        joyplot(
            data=df_full[['classement', 'ville']], 
            by='ville',
            figsize=(12, 8),
            linecolor="blue", 
            colormap=cm.autumn_r
        )
        plt.title('Ligne de crête des classements par ville', fontsize=20)
        st.pyplot(plt,use_container_width=True)

    
    if graph_selection =="Lignes de crêtes par Spécialité":
        st.write("WIP")


    


def checkFilter(graph_selection, liste_annee, liste_ville, liste_specialite):
    df = pd.read_csv('data/2_aggregates/agg_latest_spot.csv', index_col=0)
    df = df[df.ville.isin(liste_ville)&df.specialite.isin(liste_specialite)&df.annee.isin(liste_annee)]

    all_ville = df.ville.unique().tolist()
    all_specialite = df.specialite.unique().tolist()
    all_annee = df.annee.unique().tolist()


    st.write(all_ville)
    st.write(all_specialite)
    st.write(all_annee)
    
