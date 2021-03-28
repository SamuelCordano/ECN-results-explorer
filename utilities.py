import streamlit as st
import numpy as np
import pandas as pd
import os
import re
import utilities

#Old Stuff
#df = pd.read_csv('raw_files/resultats_2010_11.txt', header=None, delimiter = "\t")
#num_rows = df.shape[0]
#df_final = pd.DataFrame(columns=['title', 'lastName', 'firstNames','dateOfBirth','spécialité','ville'])

def find_unclean_input(df):

    for index, row in df.iterrows():

        
        #st.write(row)
        row_frame = row.to_frame()
        row_string = row_frame.to_string()
        row_string = row_string.strip()

        if ") (" in row_string:
            continue

        row_decomposed_2 = row_string.split(')')[1]

        countCommas = row_decomposed_2.count('à')
        countCommas2 = row_decomposed_2.count(' aux ')
        countCommas3 = row_decomposed_2.count(' en ')
        if (countCommas+countCommas2+countCommas3) != 1:
            st.write(row_decomposed_2)
            st.write(index)

def clean_2010_11_data_v2(df,annee):

    #df_final = pd.DataFrame(columns=['classement','title', 'lastName', 'firstNames','dateOfBirth','specialite','ville'])
    df_final = pd.DataFrame(columns=['classement','title', 'firstNames','dateOfBirth','specialite','ville','annee'])

    #Clean_data - delete mentions with "nom d'usage"
    #df= df.raw_data.str.replace("\) \(.*?\)", ")", regex=True)
    df["raw_data"]= df.raw_data.str.replace("\) \(.*?\)", ")", regex=True)


    #Step 1: Classement, Title, Last Name
    df_final["classement"]= df.raw_data.str.split(" ").str[0]
    df_final["title"]= df.raw_data.str.split(" ").str[1]
    
    ### WIP 
    #Step 2: Last Name
    #df_final["lastName"]= df.raw_data.str.split("(").str[0]
    #df_final["lastName"]= df_final["lastName"].str.split(" ").str[2:]
    #df_final["lastName"]= df_final["lastName"].str.split(df_final["title"]).str[1]
    #df_final["lastName"]= df_final["lastName"].str.cat(df_final["lastName"])

    #Step 3: First Names
    df_final["firstNames"]= df.raw_data.str.split(")").str[0]
    df_final["firstNames"]= df_final["firstNames"].str.split("(").str[1]

    #Step 4: Date of Birth
    df_final["dateOfBirth"]= df.raw_data.str.split(")").str[1]
    df_final["dateOfBirth"]= df_final["dateOfBirth"].str.split(", ").str[1]

    #Step 5: Specialite and Ville
    df_final["specialite"]= df.raw_data.str.split(")").str[1]
    df_final["specialite"]= df_final["specialite"].str.split(",").str[2]
    #df_final["specialite"]= df_final["specialite"].str.split(" à | aux | en ").str[0]
    df_final[['specialite','ville']] = df_final['specialite'].str.split(' à | aux | en ',expand=True)

    df_final["ville"]= df_final["ville"].str.rstrip(".")

    df_final["annee"]= annee

    #st.write(df_final.dtypes)

    return df_final


def clean_2010_11_data(df):

    df_final = pd.DataFrame(columns=['classement','title', 'lastName', 'firstNames','dateOfBirth','specialite','ville'])

    for index, row in df.iterrows():
        st.write(row)
        st.write(type(row))

        row_string_direct = row.to_string()
        st.write(row_string_direct)
        st.write(type(row_string_direct))

        row_frame = row.to_frame()
        st.write(row_frame)
        st.write(type(row_frame))
        
        row_string = row_frame.to_string()
        st.write(row_string)
        st.write(type(row_string))
        row_string = row_string.strip()
        st.write(row_string)

        if ") (" in row_string:
            #row_string = re.sub(') (.*?)', '', row_string)
            continue

        #st.write(row_string)
        #st.write(row_frame)
        #st.write(row_frame_string)
        row_decomposed = row_string.split(' ')
        #st.write(row_decomposed)

        #Step 1: Classement, Title
        row_classement = row_decomposed[2]
        row_title =row_decomposed[3]

        #Step 1.b: Last Name
        row_lastName = row_string.split('(')[0]
        row_lastName = row_lastName.split(row_title)[1]

        #Step 2: First Names
        row_decomposed_2 = row_string.split(')')[0]
        row_firstNames = row_decomposed_2.split('(')[1]

        #Step 3: Date of Birth
        row_decomposed_3 = row_string.split(')')[1]
        row_dateOfBirth = row_decomposed_3.split(',')[1]

        #Step 4: Specialite and Ville
        row_decomposed_3 = row_string.split(')')[1]
        st.write(row_decomposed_3)
        row_decomposed_4 = row_decomposed_3.split(',')[2]
        row_specialite = re.split(' à | aux | en ',row_decomposed_4)[0]
        row_ville = re.split(' à | aux | en ',row_decomposed_3)[1]

        df_final.loc[index] = [row_classement,row_title,row_lastName,row_firstNames,row_dateOfBirth,row_specialite,row_ville]
    
    return df_final


def create_df_lastest_spot(df):
    villes_list = sorted(df.ville.unique().tolist())
    specialite_list = sorted(df.specialite.unique().tolist())

    df_results =pd.DataFrame(index=specialite_list,columns=villes_list)

    for index, row in df.iterrows():
        df_results.at[row["specialite"], row["ville"]] =row["classement"]

    return df_results


def draw_heat_map(df):
    villes_list = sorted(df.ville.unique().tolist())
    specialite_list = sorted(df.specialite.unique().tolist())
    df_rfd_01_np_float = df_rfd_01_np.astype(float)

    vegetables = specialite_list
    farmers = villes_list
    harvest = df_rfd_01_np_float


    ### ACTUAL DRAWING
    plt.figure(figsize=(100,100))

    fig, ax = plt.subplots()
    im = ax.imshow(harvest)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(farmers)))
    ax.set_yticks(np.arange(len(vegetables)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(farmers)
    ax.set_yticklabels(vegetables)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    #for i in range(len(vegetables)):
    #    for j in range(len(farmers)):
    #        text = ax.text(j, i, harvest[i, j],
    #                       ha="center", va="center", color="w")

    ax.set_title("Classement où le dernier combo spécialité/ville a été selectionné")
    fig.tight_layout()
    #plt.show()
    #plt.savefig("test.png")
    st.pyplot(fig)