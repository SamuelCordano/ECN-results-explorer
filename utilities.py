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


def clean_data(df,annee):
    if annee < 2019:
        df_final = pd.DataFrame(columns=['classement','title', 'firstNames','dateOfBirth','specialite','ville','annee'])
    elif annee >= 2019:
        df_final = pd.DataFrame(columns=['classement','title', 'firstNames','specialite','ville','annee'])

    #Clean_data - delete mentions with "nom d'usage"
    #df= df.raw_data.str.replace("\) \(.*?\)", ")", regex=True)
    df["raw_data"]= df.raw_data.str.replace("\) \(.*?\)", ")", regex=True)
    # Example: 2005 M. Descoux (Jérémy), nom d'usage : Descoux-Frias,
    df["raw_data"]= df.raw_data.str.replace("\), nom d'usage .*?,", "),", regex=True)

    #Clean_data - delete mentions with "épouse"
    # Example: 878 Mme Dufour (Ségolène, Marie), épouse Pueyo, née le 29 décembre 1986, médecine générale à Rouen.
    df["raw_data"]= df.raw_data.str.replace("\), épouse .*?,", "),", regex=True)

    df["raw_data"]= df.raw_data.str.replace("\), époux .*?,", "),", regex=True)
    df["raw_data"]= df.raw_data.str.replace("\), famille .*?,", "),", regex=True)

    #Clean data: enlever les virgules de la spécialité: endocrinologie, diabète, maladies métaboliques
    df["raw_data"]= df.raw_data.str.replace("endocrinologie, diabète, maladies métaboliques", "endocrinologie diabète maladies métaboliques", regex=True)

    # pour 2017 et après: médecine et santé au travail -> médecine du travail
    #Pour 2017 et après: chirurgie plastique, reconstructrice et esthétique -> chirurgie plastique reconstructrice et esthétique
    df["raw_data"]= df.raw_data.str.replace("médecine et santé au travail", "médecine du travail", regex=True)
    df["raw_data"]= df.raw_data.str.replace("chirurgie plastique, reconstructrice et esthétique", "chirurgie plastique reconstructrice et esthétique", regex=True)


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

    if annee < 2019:
        #Step 4: Date of Birth
        df_final["dateOfBirth"]= df.raw_data.str.split(")").str[1]
        df_final["dateOfBirth"]= df_final["dateOfBirth"].str.split(", ").str[1]

        #Step 5: Specialite and Ville
        df_final["specialite"]= df.raw_data.str.split(")").str[1]
        df_final["specialite"]= df_final["specialite"].str.split(",").str[2]
    elif annee >= 2019:
        #Step 4: No Data of Birth 

        #Step 5: Specialite and Ville
        df_final["specialite"]= df.raw_data.str.split(")").str[1]
        df_final["specialite"]= df_final["specialite"].str.split(",").str[1]
    
    if annee > 2016:
        df_final[['specialite','ville']] = df_final['specialite'].str.split(' à | aux | en | au ',n=1,expand=True)
    else:
        df_final[['specialite','ville']] = df_final['specialite'].str.split(' à | aux | en ',n=1,expand=True)
    
    #Step 5.B: clean Specialite and Ville
    df_final["specialite"]= df_final["specialite"].str.lower()

    df_final["ville"]= df_final["ville"].str.rstrip(".")
    df_final["ville"]= df_final.ville.str.replace("CHU d('|e )|Hospices Civils de |l'Assistance Publique(-| des )Hôpitaux de ", "", regex=True)
    df_final["ville"]= df_final.ville.str.replace("(o|O)céan( |-)Indien|la Réunion", "La Réunion", regex=True)
    df_final["ville"]= df_final.ville.str.replace("Ile-de-France|l'AP-HP", "Paris", regex=True)
    df_final["ville"]= df_final.ville.str.replace("Aix-Marseille|l'AP-HM", "Marseille", regex=True)
    df_final["ville"]= df_final.ville.str.replace("(l|L)a Martinique(| )/(| )Pointe-à-Pitre|Antilles-Guyane", "Martinique/Pointe-à-Pitre", regex=True)
    df_final= df_final.replace({'ville': {"HCL": "Lyon"}})


    #Step 6: Annee
    df_final["annee"]= annee


    return df_final

def find_unclean_input(annee): 
    df = pd.read_csv(f'data/0_raw/resultats_{annee}.txt', header=None, delimiter = "\t",names=["raw_data"])

    if annee > 2016:
        df_check = df[df.raw_data.str.count(' à | aux | en | au ') !=1]
    else:
        df_check = df[df.raw_data.str.count(' à | aux | en ') !=1]

    if len(df_check.index) != 0:
        st.write("Hey it seems there is at least one row with multiple instances of à | aux | en  -- Deal with it before moving on ;)")
        st.write(df_check)

    df = clean_data(df,annee)

    st.write("Liste des villes")
    st.write(df.ville.unique())
    st.write("Liste des candidats où la ville est vide: ")
    st.write(df[df["ville"].isnull()]) 

    st.write("Liste des spécialités")
    st.write(df.specialite.unique())
    st.write("List des candidats où la spécialité est vide: ")
    st.write(df[df["specialite"].isnull()]) 
    
    return df

def raw_to_cleaned(annee):
    df = pd.read_csv(f'data/0_raw/resultats_{annee}.txt', header=None, delimiter = "\t",names=["raw_data"])
    df = clean_data(df,annee)
    df.to_csv(f'data/1_cleaned/resultats_{annee}_clean.csv', index=True)
    return df

def create_df_lastest_spot(df):
    villes_list = sorted(df.ville.unique().tolist())
    specialite_list = sorted(df.specialite.unique().tolist())

    df_results =pd.DataFrame(index=specialite_list,columns=villes_list)

    for index, row in df.iterrows():
        df_results.at[row["specialite"], row["ville"]] =row["classement"]

    return df_results



def show_column_values(column):
    list_of_years = range(2010,2021)

    if column =="ville":
        df = pd.DataFrame(index=range(28),columns=list_of_years)
        for year in list_of_years:
            df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
            list_of_specialite = sorted(df_year.ville.unique())
            df[year]= list_of_specialite
        st.write(df)

    elif column=="specialite":
        df = pd.DataFrame(index=range(44),columns=list_of_years)
        for year in list_of_years:
            df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
            list_of_specialite = sorted(df_year.specialite.unique())
            if len(list_of_specialite)<40:
                list_of_specialite.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1])
                #Before 2016 there was only 29 specialite, we add placeholders in order to come up to 43
            df[year]= list_of_specialite
        st.write(df)

    else:
        st.write("This function only works for cities and specialite ;-)")

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

# FUNCTIONS TO GO TO TRUSTED
def cleaned_to_aggregates_latest_spot():
    df_final = pd.DataFrame(columns=['classement','specialite','ville','annee'])
    list_of_years = range(2010,2021)
    #list_of_years = range(2010,2013)

    for year in list_of_years:
        df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
        df_year = df_year[['classement','specialite','ville','annee']]
        num_rows = max(df_year.classement)
        
        df_agg= df_year.groupby(['specialite','ville','annee']).max()
        df_agg = df_agg.reset_index(level=['specialite','ville','annee'])

        #Transform Classement to have a number between 0, best, to 1, worst. Because the number of candidates changes each year
        df_agg["classement"] = pd.to_numeric(df_agg["classement"], downcast="float")
        df_agg["classement"]= df_agg["classement"].divide(num_rows)

        #Clean Spécialité (take out leading white space and Capitalize first word)
        df_agg["specialite"]= df_agg["specialite"].str.lstrip(" ")
        df_agg["specialite"]= df_agg["specialite"].str.capitalize()
        
        df_final= df_final.append(df_agg)
    df_final.to_csv(f'data/2_aggregates/agg_latest_spot.csv', index=True)
    return df_final

def cleaned_to_full_data():
    df_final = pd.DataFrame(columns=['classement','specialite','ville','annee'])
    list_of_years = range(2010,2021)

    for year in list_of_years:
        df_year = pd.read_csv(f'data/1_cleaned/resultats_{year}_clean.csv', index_col=0)
        df_year = df_year[['classement','specialite','ville','annee']]
        num_rows = max(df_year.classement)
        
        #Transform Classement to have a number between 0, best, to 1, worst. Because the number of candidates changes each year
        df_year["classement"] = pd.to_numeric(df_year["classement"], downcast="float")
        df_year["classement"]= df_year["classement"].divide(num_rows)

        #Clean Spécialité (take out leading white space and Capitalize first word)
        df_year["specialite"]= df_year["specialite"].str.lstrip(" ")
        df_year["specialite"]= df_year["specialite"].str.capitalize()
        
        df_final= df_final.append(df_year)
    df_final.to_csv(f'data/2_aggregates/full.csv', index=True)
    return df_final