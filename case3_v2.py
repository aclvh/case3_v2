#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


def intro():
    import streamlit as st

    st.write("""# Case 3 – Van data naar informatie:
             Een dashboard over elektrisch mobiliteit en laadpalen""")
#     st.sidebar.success("Selecteer een pagina.")

    st.markdown(
    """
    Streamlit is een open-source app framework wat specifiek is gemaakt voor
    Machine Learning en Data Science projecten.
    In dit project is een dashboard gemaakt over elektrisch mobiliteit en laadpalen.
    Deze is gemaakt aan de hand van meerdere datasets:
    * Een dataset die verkregen is via OpenChargeMap
    * Laadpaaldata.csv (gekregen van docenten van de HvA)
    * 2 Datasets van de RDW
        1. Open-Data-RDW-Gekentekende_voertuigen
        2. Open-Data-RDW-Gekentekende_voertuigen_brandstof
    
    Om vervolgens meer informatie over het project te lezen
    
    **👈 Selecteer dan een keuze uit de balk hiernaast**.""")


# In[ ]:


def OpenChargeMap():
    import streamlit as st
    import pandas as pd
    import requests
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')    
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.""")
    
    # API en data inladen
    code_API ="""
        # Inladen API - kijk naar country code en maxresults
        # Mijn API key: 28e1b6b5-74e9-4a18-91f2-fde28f7b71e5
        response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=28e1b6b5-74e9-4a18-91f2-fde28f7b71e5")
        
        # Omzetten naar dictionary
        responsejson = response.json()
        responsejson
        
        # Dataframe bevat kolom die een list zijn. 
        # Met json_normalize zet je de eerste kolom om naar losse kolommen
        Laadpalen = pd.json_normalize(responsejson)

        # Daarna nog handmatig kijken welke kolommen over zijn in dit geval Connections
        # Kijken naar eerst laadpaal op de locatie
        # Kan je uitpakken middels:
        df4 = pd.json_normalize(Laadpalen.Connections)
        df5 = pd.json_normalize(df4[0])
        df5.head()

        # Bestanden samenvoegen en head tonen
        Laadpalen = pd.concat([Laadpalen, df5], axis=1)
        Laadpalen.head(3)"""
    
#     response = requests.get("https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=28e1b6b5-74e9-4a18-91f2-fde28f7b71e5")
#     responsejson = response.json()
#     Laadpalen = pd.json_normalize(responsejson)
#     df4 = pd.json_normalize(Laadpalen.Connections)
#     df5 = pd.json_normalize(df4[0])
#     df5.head()
#     Laadpalen = pd.concat([Laadpalen, df5], axis=1)
#     Laadpalen.head(3)

    Laadpalen = pd.read_csv("Laadpalen.csv")
    Laadpalen.head()

    st.code(code_API, language = 'python')
    st.write(Laadpalen.head(3))
    


# In[ ]:


def laadpaaldata():
    import streamlit as st
    import pandas as pd
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')    
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset Laadpaaldata.csv
        die is gedeeld door de HvA docenten van de minor Data Science.""")
    
    # API en data inladen
    code_API ="""
    # Inladen csv-bestand en head tonen
    laadpalen = pd.read_csv('laadpaaldata.csv')
    laadpalen.head()"""
    
    laadpalen = pd.read_csv('laadpaaldata.csv')
    laadpalen.head()

    st.code(code_API, language = 'python')
    st.write(laadpalen.head())
    


# In[ ]:


def rdw_data():
    import streamlit as st
    
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')    
    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de twee gekozen datasets
        van de RDW:
        1. Open-Data-RDW-Gekentekende_voertuigen
        2. Open-Data-RDW-Gekentekende_voertuigen_brandstof
        Deze zijn met behulp van de volgende code ingeladen:""")
    
    # API en data inladen
    code_API ="""
        # Bestand 'Gekentekende_voertuigen' inladen
        selectie_voertuigen = 'kenteken, voertuigsoort, merk, aantal_zitplaatsen, eerste_kleur, aantal_cilinders, cilinderinhoud, maximum_trekken_massa_geremd, datum_eerste_tenaamstelling_in_nederland, catalogusprijs, lengte, breedte, wielbasis'

        client_1 = Socrata("opendata.rdw.nl", None)
        elektrische_voertuigen = client_1.get("m9d7-ebf2",
                                              limit = 15200000,
                                              where = "voertuigsoort='Personenauto'",
                                              select = selectie_voertuigen)

        elektrische_voertuigen_df = pd.DataFrame.from_records(elektrische_voertuigen)
        elektrische_voertuigen_df
        
        
        # Bestand 'Gekentekende_voertuigen brandstof' inladen
        selectie_brandstof = 'kenteken, brandstof_omschrijving, emissiecode_omschrijving'

        client = Socrata("opendata.rdw.nl", None)
        brandstof = client.get("8ys7-d773",
                               limit = 14500000,
                               select = selectie_brandstof)

        brandstof_df = pd.DataFrame.from_records(brandstof)
        brandstof_df['brandstof_omschrijving'].value_counts()
        brandstof_df
        
        # Bestanden samenvoegen en omzetten naar csv bestand
        df = pd.merge(elektrische_voertuigen_df, brandstof_df, how = 'inner', on = 'kenteken')
        df.to_csv('samengevoegd.csv')
        """
    st.code(code_API, language = 'python')
    
    st.write("""
        Aangezien de datasets bestaan uit respectievelijk 15.1 miljoen rijen met 92 kolommen en 14.4 miljoen rijen met
        36 kolommen kan een normale laptop dit vanwege de grootte niet inladen.
        
        Om deze bestanden te kunnen gebruiken zijn een aantal kolommen geselecteerd die nodig waren voor specifieke
        grafieken om de bestanden wel in te kunnen laden, aangezien de bestanden dan minder groot zijn.
        Ook is gefilterd op enkel de voertuigsoort, 'personenauto'.
        Op deze manier kunnen de benodigde kolommen en rijen van de datasets wel ingeladen en samengevoegd worden.
        Vervolgens wordt het samengevoegde bestand omgezet naar een csv bestand, zodat werken met de dataset sneller
        gaat.
        """)
    
    ######################################################################################
    # Plot 1 met cum aantal auto's per brandstof omschrijving
    ######################################################################################
    df_fig2 = pd.read_csv('df_fig1.csv')
    
    fig1 = px.line(df_fig1,
               y = "cum aantal",
               x = "datum",
               color = "brandstof_omschrijving")

    fig1.update_layout(title = "Cumulatief aantal auto's per brandstofsoort",
                   xaxis_title = "Datum",
                   yaxis_title = "Aantal auto's",
                   legend_title = "Brandstof soort",
                   xaxis = dict(rangeslider = dict(visible = True)))
    
    st.plotly_chart(fig1)
    
    ######################################################################################
    # Regressiemodel met 2 losse plotjes en uit te voeren onderdeel
    ######################################################################################
    df_model = pd.read_csv('df_model.csv')
    
    fig_model1 = px.scatter(df_model,
                        x = 'emissiecode_omschrijving',
                        y = 'cilinderinhoud',
                        opacity = 0.65,
                        trendline='ols',
                        trendline_color_override='darkblue')

    fig_model1.update_layout(title = "Regressie tussen de emissiecode en de cilinderinhoud",
                             xaxis_title = "Emissiecode omschrijving",
                             yaxis_title = "Cilinderinhoud")

    st.plotly_chart(fig_model1)
    
    fig_model2 = px.scatter(df_model,
                        x = 'aantal_cilinders',
                        y = 'cilinderinhoud',
                        trendline='ols',
                        trendline_color_override = 'red')

    fig_model2.update_layout(title = "Regressie tussen het aantal cilinders en de cilinderinhoud",
                             xaxis_title = "Aantal cilinders",
                             yaxis_title = "Cilinderinhoud")

    st.plotly_chart(fig_model2)
    
    ######################################################################################


# In[ ]:


page_names_to_funcs = {
    "Opdrachtomschrijving": intro,
    "OpenChargeMap": OpenChargeMap,
    "Laadpaaldata.csv": laadpaaldata,
    "Datasets van de RDW": rdw_data
}

demo_name = st.sidebar.selectbox("Kies een pagina", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

