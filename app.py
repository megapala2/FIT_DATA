import pandas as pd
import streamlit as st
import os
import ast
import plotly.express as px

#   PT:
#   Essa função serve para limpar os dados, o dado em CSV vem com uma coluna "Value" onde possui um dicionário DENTRO da coluna, 
#   entretanto, esse dicionário muda de acordo com o valor de "Key". Essa função vai limpar colunas dispensáveis para a leitura dos dados, arrumar a data,
#   pegar cada valor do dicionário "Value" e criar uma nova coluna do DF


#   EN:
#   This function is intended to clean the data. The CSV data includes a column named "Value" which contains a dictionary WITHIN the column. However, 
#   this dictionary varies according to the value of "Key". This function will clean unnecessary columns for data reading, 
#   fix the date, extract each value from the "Value" dictionary, and create a new column in the DataFrame.


def clean_key_data(df_health, valor: str):

    df = df_health[df_health['Key'] == valor].copy()
    novas_colunas = pd.DataFrame([ast.literal_eval(d) for d in df['Value']])
    df = pd.concat([df, novas_colunas], axis=1)
    df = df.drop('Value', axis=1)
    df = df.drop('Uid', axis=1)
    df = df.drop('Sid', axis=1)

   
    return df, novas_colunas.columns.to_list()

def clean_date(df_health):

    df_health['UpdateTime'] = pd.to_datetime(df_health['UpdateTime'], unit='s')
    df_health['Time'] = pd.to_datetime(df_health['Time'], unit='s')
    df_health["Mês-Ano"] = df_health["UpdateTime"].apply(lambda x: str(x.day)+ "-" + str(x.month) + "-" + str(x.year))
    

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

df = pd.read_csv(f'{os.getcwd()}\\DADOS\\HEALTH_DATA.csv')
df_health = clean_date(df) 

categorias = df_health['Key'].unique()

selecionado = st.selectbox(label="Selecione a categoria que deseja olhar!", options=categorias)


df_steps, cols = clean_key_data(df_health, valor=selecionado)

if selecionado:
    valores = st.selectbox(label='Selecione a coluna de valor!', options=cols)
    cor = st.selectbox(label='Selecione a coluna de cor!', options=cols)


st.dataframe(df_steps)
fig = skill_chart(df_steps, valor=valores, cor=cor)

st.plotly_chart(fig)