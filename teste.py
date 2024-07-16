import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Título da página
st.title('Análise de Dados de Organizações')

# Opção para o usuário escolher o tipo de arquivo 
file_type = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))

# Função para carregar o arquivo
def load_data(file):
    if file_type == "CSV":
        df = pd.read_csv(file)
    elif file_type == "Excel":
        df = pd.read_excel(file, engine='openpyxl')  # Use 'engine=openpyxl' para ler arquivos XLSX
    return df

# Carregar arquivo CSV ou Excel
uploaded_file = st.file_uploader(f"Escolha um arquivo {file_type}", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Ler o arquivo
    df = load_data(uploaded_file)

    # Mostrar os dados brutos
    st.subheader('Dados do Arquivo Carregado')
    st.write(df)

    # Lista de lojas disponíveis no DataFrame
    lojas_disponiveis = df['Loja Responsável'].unique().tolist()
    
    # Filtro para escolher a loja
    selected_loja = st.selectbox("Escolha a Loja:", lojas_disponiveis)

    # Verificar se a coluna 'Nome Organização' existe no DataFrame
    if 'Nome Organização' in df.columns and 'Hectares Conectados' in df.columns:
        # Filtrar os dados pelo nome da loja selecionada
        df_filtrado = df[df['Loja Responsável'] == selected_loja]

        # Agrupamento por Nome da Organização e soma dos Hectares Conectados
        grouped_data = df_filtrado.groupby('Nome Organização')['Hectares Conectados'].sum().reset_index()

        # Ordenando os dados pela quantidade de Hectares Conectados
        grouped_data = grouped_data.sort_values(by='Hectares Conectados', ascending=False)

        # Exibindo o gráfico de barras com ECharts
        chart_data = grouped_data.head(50)  

        st.subheader(f'Hectares Conectados por Nome da Organização (Loja: {selected_loja})')
        st_echarts(options={
            'tooltip': {'trigger': 'axis', 'axisPointer': {'type': 'shadow'}},
            'xAxis': {'type': 'category', 'data': chart_data['Nome Organização'].tolist()},
            'yAxis': {'type': 'value'},
            'series': [{'name': 'Hectares Conectados', 'type': 'bar', 'data': chart_data['Hectares Conectados'].tolist()}]
        })
    else:
        st.warning("As colunas necessárias ('Nome Organização' e 'Hectares Conectados') não foram encontradas no arquivo.")
