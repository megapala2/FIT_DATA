import pandas as pd
import streamlit as st
import os
import ast
import plotly.express as px
import json

#   PT:
#   Essa função serve para limpar os dados, o dado em CSV vem com uma coluna "Value" onde possui um dicionário DENTRO da coluna, 
#   entretanto, esse dicionário muda de acordo com o valor de "Key". Essa função vai limpar colunas dispensáveis para a leitura dos dados, arrumar a data,
#   pegar cada valor do dicionário "Value" e criar uma nova coluna do DF


#   EN:
#   This function is intended to clean the data. The CSV data includes a column named "Value" which contains a dictionary WITHIN the column. However, 
#   this dictionary varies according to the value of "Key". This function will clean unnecessary columns for data reading, 
#   fix the date, extract each value from the "Value" dictionary, and create a new column in the DataFrame.


def clean_key_data(df_health, valor: str):

   
    df_health = df_health[df_health['Key'] == valor].copy()
    df_health['parsed_json'] = df_health['Value'].apply(json.loads)
 
 
    
    json_df = pd.json_normalize(df_health['parsed_json'])
    
 
    df_health = pd.concat([df_health.reset_index(drop=True), json_df.reset_index(drop=True)], axis=1)

    df_health= df_health.drop('Value', axis=1)
    df_health= df_health.drop('parsed_json', axis=1)
    
    

    if 'time' in df_health.columns:
        df_health['time'] = pd.to_datetime(df_health['time'], unit='s', errors='coerce')
    
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

   
    return df_health, json_df.columns.to_list()

def clean_date(df_health):
    
    

    df_health['UpdateTime'] = pd.to_datetime(df_health['UpdateTime'], unit='s', errors='coerce')
    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s', errors='coerce')
    df_health["Mês-Ano"] = df_health["UpdateTime"].apply(lambda x: str(x.day)+ "-" + str(x.month) + "-" + str(x.year))
    df_health = df_health.drop('Uid', axis=1)
    df_health = df_health.drop('Sid', axis=1)

    return df_health

def skill_chart(df, valor: str, cor: str):
 
    fig = px.bar(
        x=df['Time'], 
        y=df[valor], 
        color=df[cor],
        orientation='v',
        template='presentation',
        
    )

    return fig
                        
   


st.set_page_config(layout='wide')
col1, col2, col3 = st.columns(3)

df = pd.read_csv(f'{os.getcwd()}\\DADOS\\HEALTH_DATA.csv')
df_health = clean_date(df) 

categorias = df_health['Key'].unique()

selecionado = col1.selectbox(label="Selecione a categoria que deseja olhar!", options=categorias)


df_steps, cols = clean_key_data(df_health, valor=selecionado)

if selecionado:
    valores = col2.selectbox(label='Selecione a coluna de valor!', options=cols)
    cor = col3.selectbox(label='Selecione a coluna de cor!', options=cols)

with st.expander('DataFrame'):
    st.info(f'Rows of data: {len(df_steps)}')
    st.dataframe(df_steps, use_container_width=True)


