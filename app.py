import pandas as pd
import streamlit as st
import os
import ast
import plotly.express as px
import json
from datetime import datetime


EXPLANATION = {"weight": "Peso",
               "bmi": "IMC",
               "body_fat_rate": r"% Gordura",
               "Date": "Data",
               "moisture_rate": "% Hidratação",
               "bone_mass": "% Massa Óssea",
               "basal_metabolism": "Metabolismo Basal",
               "muscle_rate": "% Massa Muscular",
               "protein_rate": "% Proteína",
               "visceral_fat": r"% Gordura Visceral",
               "bpm": "BPM",
               "stress": "Estresse",
               "calories": "Calorias",
               "spo2": "% Oxigênio no Sangue",
               "bedtime": "H. Adormeceu",
               "wake_up_time": "H. Acordou",
               "timezone": "Fuso horário",
               "duration": "Duração (minutos)",
               "sleep_deep_duration": "Sono Profundo (minutos)",
               "sleep_light_duration": "Sono Leve (minutos)",
               "sleep_rem_duration": "Sono Rem (minutos)",
               "sleep_awake_duration": "Tempo acordado (minutos)",
               "total_score": "Pontuação",
               "breath_quality": "Qualidade da respiração",
               "daily_pai": "Diário",
               "total_pai": "Total",
               "high_zone_pai": "Máximo",
               "medium_zone_pai": "Media",
               "low_zone_pai": "Baixa",
               "start_time": "Inicio",
               "end_time": "Fim",
               "type": "Tipo",
               "steps": "Passos",
               "distance": "Distância",

}

CATEGORIAS = {"weight": "Peso",
              "heart_rate": "Batimentos",
              "stress": "Estresse",
              "steps": "Passos",
              "calories": "Calorias",
              "single_spo2": "Somente Oxigênio no Sangue",
              "watch_night_sleep": "Sono",
              "pai": "PAI",
              "resting_heart_rate": "Batimentos em Repouso",
              "dynamic": "Dinâmico",
              "intensity": "Intenso",
              "single_heart_rate": "Somente Batimentos",
              "watch_daytime_sleep": "Cochilos",
              "single_stress": "Somente Estresse",
              "abnormal_heart_beat": "Batimentos Anormais",

}

VALORES = ["Data", "Hora", "Peso", "IMC", r"% Gordura", "% Hidratação", "% Massa Óssea", "Metabolismo Basal", 
           "% Massa Muscular", "% Proteína", r"% Gordura Visceral", "BPM", "Estresse", "Calorias", ""
           
           
           ] 
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
    df_health= df_health.drop('Key', axis=1)
    
    

    if 'time' in df_health.columns:
        df_health = df_health.drop('time', axis=1)
        json_df = json_df.drop('time', axis=1)
    
    if 'date_time' in df_health.columns:
       df_health = df_health.drop('date_time', axis=1)
       json_df = json_df.drop('date_time', axis=1)
    
    if 'items' in df_health.columns:
       df_health = df_health.drop('items', axis=1)
       json_df = json_df.drop('items', axis=1)

    if 'friendly_score' in df_health.columns:
       df_health = df_health.drop('friendly_score', axis=1)
       json_df = json_df.drop('friendly_score', axis=1)
    
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
    df_health = df_health.rename(columns=EXPLANATION)
    json_df = json_df.rename(columns=EXPLANATION)
    
    return df_health, json_df.columns.to_list()

#   PT:
#   Essa é a limpeza geral do dataframe, ele troca os padrões de dados para os padrões corretos, formata as datas corretamente, também dropa diversas colunas indesejadas

#   EN:
#   This is the general cleaning of the dataframe, it changes data patterns to the correct ones, formats dates properly, and also drops various unwanted columns. 

@st.cache_data
def clean_date(df_health):
    
    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s', errors='coerce')
    df_health['Date'] = df_health['Time'].dt.strftime('%d-%m-%Y')
    df_health["Hora"] = df_health["Time"].dt.strftime('%H:%M')
    
  
    

    df_health = df_health.drop('Sid', axis=1)
    df_health = df_health.drop('Time', axis=1)
    df_health = df_health.drop('UpdateTime', axis=1)
    df_health = df_health.drop('Uid', axis=1)
    df_health['Key'] = df_health['Key'].replace(CATEGORIAS)

    return df_health

#   PT:
#   Esse é o filtro de data do dataframe

#   EN:
#   This is the date filter of the DF

def date_filter(df_health, startDate, endDate):

    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s', errors='coerce')
    df_health = df_health[( df_health['Time'].dt.date >= startDate) & ( df_health['Time'].dt.date <= endDate)]
    
    return df_health

#   PT:
#   Cria o gráfico

#   EN:
#   Create the chart
   
def skill_chart(df, valor: str, valor2: str):

    fig = px.line(
        df, 
        x=valor, 
        y=valor2, 
        template='presentation',
    )


    return fig
   


st.set_page_config(layout='wide')
st.title('MIBAND DATA')
st.info('Se quiser baixar os seus dados da MIBAND: https://www.mi.com/global/support/article/KA-11566/')

col1, col2, col3 = st.columns(3)
sideCol1, sideCol2 = st.sidebar.columns(2)


df = pd.read_csv(f'{os.getcwd()}/DADOS/HEALTH_DATA.csv')



filter_data_I = sideCol1.date_input(
            'Data Inicial', value=datetime(2019, 1, 1), format="DD/MM/YYYY", key='dataInicial')
filter_data_F = sideCol2.date_input(
            'Data Final', value="today", format="DD/MM/YYYY", key='dataFinal')


df_health = clean_date(df) 

if filter_data_F:
 df = date_filter(df, filter_data_I, filter_data_F )



categorias = df_health['Key'].unique()

selecionado = col1.selectbox(label="Selecione a categoria que deseja analisar!", options=categorias)


df_steps, cols = clean_key_data(df_health, valor=selecionado)
cols.append("Data")
cols.append("Hora")


with st.expander('DataFrame Tratado'):
    st.info(f'Linhas do dataframe: {len(df_steps)}      |        Filtro: {selecionado}')
    st.dataframe(df_steps, use_container_width=True)
with st.expander('DataFrame Semi Tratado'):
    st.info(f'Linhas do dataframe: {len(df_health)}')
    st.dataframe(df_health, use_container_width=True)
with st.expander('DataFrame Bruto'):
    st.info(f'Linhas do dataframe: {len(df)}')
    st.dataframe(df, use_container_width=True)



valores = col2.selectbox(label='Selecione o valor que deseja observar!', options=cols, index=None)
cor = col3.selectbox(label='Selecione o segundo valor!', options=cols, index=None)

if valores and cor:

    fig = skill_chart(df_steps, valor=valores, valor2=cor)
    st.plotly_chart(fig, use_container_width=True)

    

