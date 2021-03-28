import streamlit as st
import numpy as np
import pandas as pd
import os
import re
import utilities
import matplotlib
import matplotlib.pyplot as plt

st.title('My first app')

df = pd.read_csv('raw_files/resultats_2010.txt', header=None, delimiter = "\t",names=["raw_data"])

st.write(utilities.clean_2010_11_data_v2(df_head5,2010))


#df_final = utilities.clean_2010_11_data(df_test)
#st.write(df_final)
#df_final.to_csv('trd_files/trd_resultats_2010_11.csv', index=True)  



#Part 2 - Use CSV
#df = pd.read_csv('trd_files/trd_resultats_2010_11.csv', index_col=0)
#df_rfd_01 = utilities.create_df_lastest_spot(df)

#t.write(df_rfd_01)
#st.table(df_rfd_01)
#list(df.index.values) 
#list(df.columns) 

#df_rfd_01_np = df_rfd_01.to_numpy()
#st.write(type(df_rfd_01_np))

