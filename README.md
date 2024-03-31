
# MiBand Data Analysis
Este projeto é uma aplicação para análise de dados coletados da MiBand. Ele permite visualizar e analisar diversas métricas de saúde registradas pela MiBand, como peso, batimentos cardíacos, estresse, passos, calorias queimadas, entre outros.

## Instalação
Para executar este projeto, siga estas etapas:

**Clone o repositório**:

```
git clone https://github.com/megapala2/miband-data-analysis.git
```

**Instale as dependências**:
```
pip install pandas streamlit plotly
```
**Execute o aplicativo**:
```
streamlit run app.py
```

## Como Usar
Ao executar o aplicativo, você verá um menu à esquerda com opções de filtragem por data.
Selecione um intervalo de datas para visualizar os dados.
Escolha a categoria de dados que deseja analisar no menu suspenso.
Selecione os valores que deseja observar nos gráficos.
Os gráficos serão atualizados automaticamente com os valores selecionados.

## Funcionalidades
**Limpeza de Dados**: O aplicativo realiza a limpeza e formatação dos dados coletados da MiBand, incluindo a conversão de datas e remoção de colunas indesejadas.

**Filtragem por Data**: Permite filtrar os dados por um intervalo de datas específico para uma análise mais precisa.

**Visualização Interativa**: Utiliza a biblioteca Plotly para criar gráficos interativos que facilitam a análise e comparação dos dados.

## Contribuição
Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões para melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).






