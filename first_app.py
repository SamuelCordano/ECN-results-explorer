import streamlit as st
import numpy as np
import pandas as pd
import os
import re
import utilities
import matplotlib
import matplotlib.pyplot as plt

st.title('ECN Results Analysis')


#Step 1- Make sure Input file is good 
#df = utilities.find_unclean_input(2010)

#Step 2 Save File
df = utilities.raw_to_cleaned(2010)
#st.write(df)


"""
#Step 3 - Find Specialities for each year 
list_of_years = range(2010,2021)
list_of_placeholders = [1,1,1,1,1,1,1,1,1,1,1,1,1]
df = pd.DataFrame(index=range(44),columns=list_of_years)
st.write(df)
for year in list_of_years:
    df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
    #st.write(df)
    list_of_specialite = sorted(df_year.specialite.unique())
    if len(list_of_specialite)<40:
        list_of_specialite.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    #st.write(list_of_specialite)
    df[year]= list_of_specialite
    #st.write(type(list_of_specialite)) 
    st.write(year)
    #st.write(df)

st.write(df)
"""

#Step 4 - Find Ville for each year 
list_of_years = range(2010,2021)
df = pd.DataFrame(index=range(28),columns=list_of_years)
st.write(df)
for year in list_of_years:
    df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
    #st.write(df)
    list_of_specialite = sorted(df_year.ville.unique())
    #st.write(list_of_specialite)
    df[year]= list_of_specialite
    #st.write(type(list_of_specialite)) 
    #st.write(year)
    #st.write(df)

st.write(df)

#Part 2 - Use CSV
#df = pd.read_csv('trd_files/trd_resultats_2010_11.csv', index_col=0)
#df_rfd_01 = utilities.create_df_lastest_spot(df)

#t.write(df_rfd_01)
#st.table(df_rfd_01)
#list(df.index.values) 
#list(df.columns) 

#df_rfd_01_np = df_rfd_01.to_numpy()
#st.write(type(df_rfd_01_np))

