import pandas as pd
import streamlit as st
import os
import ast
import plotly.express as px
import json
from datetime import datetime

#   PT:
#   Essa função serve para limpar os dados, o dado em CSV vem com uma coluna "Value" onde possui um json DENTRO da coluna, 
#   entretanto, esse json muda de acordo com o valor de "Key". Essa função vai limpar colunas dispensáveis para a leitura dos dados, arrumar a data,
#   pegar cada valor do json "Value" e criar uma nova coluna do DF


#   EN:
#   This function is intended to clean the data. The CSV data includes a column named "Value" which contains a json WITHIN the column. However, 
#   this json varies according to the value of "Key". This function will clean unnecessary columns for data reading, 
#   fix the date, extract each value from the "Value" json, and create a new column in the DataFrame.


def clean_key_data(df_health, valor: str):

   
    df_health = df_health[df_health['Key'] == valor].copy()
    df_health['parsed_json'] = df_health['Value'].apply(json.loads)
 
 
    
    json_df = pd.json_normalize(df_health['parsed_json'])
    
 
    df_health = pd.concat([df_health.reset_index(drop=True), json_df.reset_index(drop=True)], axis=1)

    df_health= df_health.drop('Value', axis=1)
    df_health= df_health.drop('parsed_json', axis=1)
    
    

    if 'time' in df_health.columns:
        df_health = df_health.drop('time', axis=1)
        json_df = json_df.drop('time', axis=1)
    
    if 'date_time' in df_health.columns:
       df_health['date_time'] = pd.to_datetime(df_health['date_time'], unit='s', errors='coerce')
    
    if 'start_time' in df_health.columns:
        df_health['start_time'] = pd.to_datetime(df_health['start_time'], unit='s', errors='coerce')

    if 'end_time' in df_health.columns:
        df_health['end_time'] = pd.to_datetime(df_health['end_time'], unit='s', errors='coerce')

    if 'bedtime' in df_health.columns:
        df_health['bedtime'] = pd.to_datetime(df_health['bedtime'], unit='s', errors='coerce')

    if 'wake_up_time' in df_health.columns:
        df_health['wake_up_time'] = pd.to_datetime(df_health['wake_up_time'], unit='s', errors='coerce')

    df_health = df_health.dropna()
    df_health = df_health[(df_health.iloc[:, 1:] != 0).all(axis=1)]
    
   
    return df_health, json_df.columns.to_list()

def clean_date(df_health):
    
    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s', errors='coerce')
    df_health['Date'] = df_health['Time'].dt.strftime('%d-%m-%Y')
    df_health["Hora"] = df_health["Time"].dt.strftime('%H:%M')
    
  
    

    df_health = df_health.drop('Sid', axis=1)
    df_health = df_health.drop('Time', axis=1)
    df_health = df_health.drop('UpdateTime', axis=1)
    df_health = df_health.drop('Uid', axis=1)

    return df_health

def date_filter(df_health, startDate, endDate):

    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s', errors='coerce')
    df_health = df_health[( df_health['Time'].dt.date >= startDate) & ( df_health['Time'].dt.date <= endDate)]
    
    return df_health
   
def skill_chart(df, valor: str, cor: str):

    
    fig = px.bar(
        x=df['Date'], 
        y=df[valor], 
        text=df[valor],
        color=df[cor],
        orientation='v',
        template='presentation',
        
    )

    return fig
                        
   


st.set_page_config(layout='wide')
st.title('MIBAND DATA')
st.info('If you want to find your Mifit data go to: https://www.mi.com/global/support/article/KA-11566/')

col1, col2, col3 = st.columns(3)
sideCol1, sideCol2 = st.sidebar.columns(2)


df = pd.read_csv(f'{os.getcwd()}\\DADOS\\HEALTH_DATA.csv')



filter_data_I = sideCol1.date_input(
            'Start Date', value=datetime(2019, 1, 1), format="DD/MM/YYYY", key='dataInicial')
filter_data_F = sideCol2.date_input(
            'End Date', value="today", format="DD/MM/YYYY", key='dataFinal')



df = date_filter(df, filter_data_I, filter_data_F )

df_health = clean_date(df) 





categorias = df_health['Key'].unique()



selecionado = col1.selectbox(label="Select the category you wish to analyse!", options=categorias)



df_steps, cols = clean_key_data(df_health, valor=selecionado)




if selecionado:
    valores = col2.selectbox(label='Select the value column!', options=cols)
    cor = col3.selectbox(label='Select the color column!', options=cols)

with st.expander('DataFrame'):
    st.info(f'Rows of data: {len(df_steps)}')
    st.dataframe(df_steps, use_container_width=True)
    

fig = skill_chart(df_steps, valor=valores, cor=cor)
st.plotly_chart(fig, use_container_width=True)