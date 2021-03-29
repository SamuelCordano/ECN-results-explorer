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
df = utilities.find_unclean_input(2017)

#Step 2 Save File
#df = utilities.raw_to_cleaned(2017)


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

