import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly._subplots as sp
from streamlit_option_menu import option_menu
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import plotly.graph_objects as go
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.io as pio

st.set_page_config("📊Análise de Trabalho", page_icon="", layout="wide")

# Função para carregar o arquivo por tipo de máquina
@st.cache_data
def load_data(file, file_type, encoding='utf-8'):
    try:
        if file_type == "CSV":
            df = pd.read_csv(file, encoding=encoding)
        elif file_type == "Excel":
            df = pd.read_excel(file, engine='openpyxl')
        return df
    except UnicodeDecodeError:
        st.error(f"Erro: Não foi possível decodificar o arquivo usando o encoding '{encoding}'. "
                 "Verifique o formato do arquivo ou tente novamente com um encoding diferente.")
        
# Lógica para página de Tratores
#st.sidebar.title('Selecione a página:')
#pagina_selecionada = st.sidebar.radio("Selecione a página:", ("Tratores", "Pulverizadores", "Colheitadeira"))

# Título na barra lateral
#st.sidebar.title('Selecione a página:')

def generate_pdf(df_tractors, figures, background_image_path=None):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    if background_image_path:
        background = ImageReader(background_image_path)
        c.drawImage(background, 0, 0, width=A4[0], height=A4[1])

    page_width, page_height = A4
    x_margin = 35
    y_margin = 5
    header_space = 100

    graph_height = (page_height - 1 * y_margin - header_space) / 2
    # Inserir os dados do arquivo de tratores no início do PDF
    if 'Data de Início' in df_tractors.columns and 'Data Final' in df_tractors.columns and 'Organização' in df_tractors.columns:
        data_inicio = pd.to_datetime(df_tractors['Data de Início'].iloc[0])
        data_final = pd.to_datetime(df_tractors['Data Final'].iloc[0])
        organizacao = df_tractors['Organização'].iloc[0]

        # Ajustar o tamanho da fonte e dividir em três linhas
        c.setFont("Helvetica", 10)
        dados_texto = f"Organização:\n{organizacao}\n\nData de Início:\n{data_inicio.strftime('%d/%m/%Y')}\n\nData Final:\n{data_final.strftime('%d/%m/%Y')}"
        c.drawString(x_margin, page_height - y_margin - header_space, dados_texto)

    for i, fig in enumerate(figures):
        if not isinstance(fig, plt.Figure):
            print(f"Skipping non-Matplotlib figure: {type(fig)}")
            continue

        if i % 2 == 0 and i != 0:
            c.showPage()
            if background_image_path:
                c.drawImage(background, 0, 0, width=A4[0], height=A4[1])

        img_data = BytesIO()
        fig.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)

        row = i % 2
        if row == 0:
            y_position = page_height - y_margin - (row + 1) * (graph_height + y_margin + header_space)
        else:
            y_position = page_height - y_margin - (row + 1) * (graph_height + y_margin)

        x_position = x_margin

        c.drawImage(ImageReader(img_data), x_position, y_position, width=fig.get_size_inches()[0] * 53, height=fig.get_size_inches()[1] * 45)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer
# Caminho para a imagem de fundo na mesma pasta dos códigos
background_image_path = 'background_pdf.jpg'

# Menu dropdown na barra superior
selected = option_menu(
    menu_title=None,  # Título do menu, None para esconder
    options=["🌱Tratores", "🌱Pulverizadores", "🌱Colheitadeira"],  # Opções do menu
    icons=['tractor', 'spray-can', 'a'],  # Ícones para cada opção
    menu_icon="cast",  # Ícone do menu
    default_index=0,  # Índice padrão
    orientation="horizontal",  # Orientação horizontal
)

# Lógica para exibir o conteúdo com base na opção selecionada
if selected == "🌱Tratores":
    pass
elif selected == "🌱Pulverizadores":
    pass
elif selected == "🌱Colheitadeira":
    pass

if selected == "🌱Tratores":
    st.subheader("Tratores")
    col1,col2,col3=st.columns(3)
    # Seleção do tipo de arquivo e upload
    file_type_tractors = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_tractors = st.file_uploader(f"Escolha um arquivo {file_type_tractors} para Tratores", type=["csv", "xlsx"])

    if uploaded_file_tractors is not None:
        df_tractors = load_data(uploaded_file_tractors, file_type_tractors)

        if df_tractors is not None:
            st.subheader('Dados do Arquivo Carregado para Tratores')
            # Exibir data de início e data final
            if 'Data de Início' in df_tractors.columns and 'Data Final' in df_tractors.columns and 'Organização' in df_tractors.columns:
                    data_inicio = pd.to_datetime(df_tractors['Data de Início'].iloc[0])
                    data_final = pd.to_datetime(df_tractors['Data Final'].iloc[0])
                    organização = df_tractors['Organização'].iloc[0]

                    col1, col2, col3 = st.columns(3)
                    col1.write(f"Organização: {organização}")
                    col2.write(f"Data de Início: {data_inicio}")
                    col3.write(f"Data Final: {data_final}")
                    

                    # Exibir logo
                    #st.image(Image.open('C:\Users\ThanizeRodrigues-Alv\OneDrive - Alvorada Sistemas Agrícolas Ltda\Área de Trabalho\Thanize\códigos\logo.jpg'), width=200)

                    # Criar lista de datas
                    dates = pd.date_range(start=data_inicio, end=data_final)

                    # Criar dicionário para cores
                    colors = {
                        'Event': 'rgb(31, 119, 180)',
                        'Other Event': 'rgb(255, 127, 14)'
                    }
            #######################################################################################

            # Definir colunas para análise de utilização
            selected_columns_utilizacao = ["Máquina", 
                                           "Utilização (Agricultura) Trabalho (%)",
                                           "Utilização (Agricultura) Transporte (%)",
                                           "Utilização (Agricultura) Marcha Lenta (%)"]

            df_selected_tractors_utilizacao = df_tractors[selected_columns_utilizacao].copy()

            # Nomes das máquinas e porcentagens de utilização
            maquinas_tractors = df_selected_tractors_utilizacao["Máquina"]
            velocidades_total_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].sum(axis=1)
            velocidades_percentual_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].div(velocidades_total_tractors, axis=0) * 100

            # Plotar gráfico de barras horizontais para % de Utilização
            fig_utilizacao, ax_utilizacao = plt.subplots(figsize=(10, 6))

            # Cores e labels para as barras de Utilização
            colors_utilizacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_utilizacao = ['Trabalhando', 'Transporte', 'Marcha Lenta']
            bar_height_utilizacao = 0.6  # Altura das barras de Utilização
            bar_positions_tractors_utilizacao = np.arange(len(maquinas_tractors))

            # Plotar as barras horizontais combinadas para cada máquina (utilização)
            for i, (maquina, row) in enumerate(zip(maquinas_tractors, velocidades_percentual_tractors.values)):
                left = 0
                for j, (percent, color) in enumerate(zip(row, colors_utilizacao)):
                    ax_utilizacao.barh(bar_positions_tractors_utilizacao[i], percent, height=bar_height_utilizacao, left=left, label=labels_utilizacao[j] if i == 0 else "", color=color)
                    ax_utilizacao.text(left + percent / 2, bar_positions_tractors_utilizacao[i], f'{percent:.1f}%', ha='center', va='center', color='black', fontsize=10)
                    left += percent

            # Configurar os eixos e título
            ax_utilizacao.set_xlabel('')
            ax_utilizacao.set_yticks(bar_positions_tractors_utilizacao)  # Manter os ticks do eixo y
            ax_utilizacao.set_yticklabels(maquinas_tractors)  # Manter os rótulos do eixo y
            ax_utilizacao.set_xticks([])  # Remover os ticks do eixo x
            ax_utilizacao.set_title('% de Utilização por Máquina - Tratores')

            # Adicionar legenda única para Utilização
            ax_utilizacao.legend(labels_utilizacao, loc='upper right', bbox_to_anchor=(1.21, 1.0))

            # Mostrar o gráfico de Utilização
            col4, col5 = st.columns(2)
            col4.pyplot(fig_utilizacao)
            #############################################################

            # Definir colunas para análise de fator de carga média do motor
            selected_columns_fator = ["Máquina", 
                                    "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                                    "Fator de Carga Média do Motor (Ag) Transporte (%)",
                                    "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)"]

            # Filtrar o DataFrame para as colunas de fator de carga selecionadas
            df_selected_tractors_fator = df_tractors[selected_columns_fator].copy()

            # Nomes das máquinas e porcentagens de fator de carga
            maquinas_tractors_fator = df_selected_tractors_fator["Máquina"]
            fatores_percentual_tractors = df_selected_tractors_fator.iloc[:, 1:] * 100

            # Plotar gráfico de barras horizontais para % de Fator de Carga
            fig_fator, ax_fator = plt.subplots(figsize=(10, 6))

            # Cores e labels para as barras de Fator de Carga
            colors_fator = ['tab:green', 'tab:gray', 'tab:orange']
            labels_fator = ['Trabalhando', 'Transporte', 'Marcha Lenta']
            bar_height_fator = 0.33  # Altura das barras de Fator de Carga
            bar_positions_tractors_fator = np.arange(len(maquinas_tractors_fator))

            # Ajustar as posições das barras para que fiquem separadas
            offset = 0.35
            for j in range(len(labels_fator)):
                ax_fator.barh(bar_positions_tractors_fator + j * offset, 
                            fatores_percentual_tractors.iloc[:, j], 
                            height=bar_height_fator, 
                            label=labels_fator[j], 
                            color=colors_fator[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_tractors_fator)):
                    percent = fatores_percentual_tractors.iloc[i, j]
                    ax_fator.text((percent / 2) + 2,  # Ajuste para mover o texto mais para a direita
                                bar_positions_tractors_fator[i] + j * offset, 
                                f'{percent:.1f}%', 
                                ha='center', 
                                va='center', 
                                color='black', 
                                fontsize=10)

            # Configurar os eixos e título
            ax_fator.set_xlabel('')
            ax_fator.set_yticks(bar_positions_tractors_fator + offset)
            ax_fator.set_yticklabels(maquinas_tractors_fator)
            ax_fator.set_title('% de Fator de Carga por Máquina - Tratores')

            # Definir os limites e marcas do eixo x
            ax_fator.set_xlim([0, 100])
            ax_fator.set_xticks([0, 50, 100])
            ax_fator.set_xticklabels(['0%', '50%', '100%'])

            # Adicionar legenda única para Fator de Carga
            ax_fator.legend(labels_fator, loc='upper right', bbox_to_anchor=(1.23, 1.0))

            # Mostrar o gráfico de Fator de Carga
            col5.pyplot(fig_fator)


            ################################################################################################

            # Definir colunas para análise de taxa média de combustível
            selected_columns_combust = ["Máquina", 
                                        "Taxa Média de Combustível (Ag) Ocioso (l/h)",
                                        "Taxa Média de Combustível (Ag) Trabalhando (l/h)",
                                        "Taxa Média de Combustível (Ag) Transporte (l/h)"]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_tractors_combust = df_tractors[selected_columns_combust].copy()

            # Nomes das máquinas e porcentagens
            maquinas_tractors_combust = df_selected_tractors_combust["Máquina"]
            percentual_tractors_combust = df_selected_tractors_combust.iloc[:, 1:] 
            # Plotar gráfico de barras verticais
            fig_combust, ax_combust = plt.subplots(figsize=(10, 6))

            # Cores e labels para as barras
            colors_combust = ['tab:green', 'tab:gray', 'tab:orange']
            labels_combust = ['Trabalhando (l/h)', 'Transporte (l/h)', 'Ocioso (l/h)']
            bar_width_combust = 0.2  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_tractors_combust = np.arange(len(maquinas_tractors_combust))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_tractors_combust, percentual_tractors_combust.values)):
                for j, (percent, color) in enumerate(zip(row, colors_combust)):
                    ax_combust.bar(bar_positions_tractors_combust[i] + j * bar_width_combust, percent, width=bar_width_combust, label=labels_combust[j] if i == 0 else "", color=color)
                    ax_combust.text(bar_positions_tractors_combust[i] + j * bar_width_combust, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

            # Configurar rótulos e título
            ax_combust.set_xlabel('')  # Texto do eixo x
            ax_combust.set_ylabel('')  # Texto do eixo y
            ax_combust.set_xticks(bar_positions_tractors_combust + bar_width_combust)
            ax_combust.set_xticklabels(maquinas_tractors_combust)
            ax_combust.set_title('Consumo de Combustível')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 51, 5)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_combust.set_yticks(yticks_values)
            ax_combust.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_combust.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))

            # Mostrar o gráfico
            col6, col7 = st.columns(2)
            col6.pyplot(fig_combust)

        ###################################################################################################

            # Definir colunas para análise de rotação média do motor
            selected_columns_rotacao = ["Máquina", 
                                        "Rotação Média do Motor Ocioso (rpm)",
                                        "Rotação Média do Motor Trabalhando (rpm)",
                                        "Rotação Média do Motor Transporte (rpm)"]

            # Filtrar o DataFrame para as colunas de rotação selecionadas
            df_selected_tractors_rotacao = df_tractors[selected_columns_rotacao].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e rotação média
            maquinas_tractors_rotacao = df_selected_tractors_rotacao["Máquina"]
            rotacoes_tractors = df_selected_tractors_rotacao.iloc[:, 1:]

            # Plotar gráfico de barras horizontais para rotação média
            fig_rotacao, ax_rotacao = plt.subplots(figsize=(10, 6))  # Ajustar o tamanho da figura para evitar erro

            # Cores e labels para as barras de rotação média
            colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_rotacao = ['Trabalhando', 'Transporte','Ocioso']
            bar_height_rotacao = 0.3  # Altura das barras de rotação média
            bar_positions_rotacao = np.arange(len(maquinas_tractors_rotacao))

            # Ajustar as posições das barras para que fiquem separadas
            offset = 0.32
            for j in range(len(labels_rotacao)):
                # Usar np.nan para valores NaN para que apareçam em branco
                ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                rotacoes_tractors.iloc[:, j].fillna(np.nan), 
                                height=bar_height_rotacao, 
                                label=labels_rotacao[j] if j == 0 else "", 
                                color=colors_rotacao[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_rotacao)):
                    rotacao = rotacoes_tractors.iloc[i, j]
                    if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                        ax_rotacao.text((rotacao / 2) + 3,  # Ajuste para mover o texto mais para a direita
                                        bar_positions_rotacao[i] + j * offset, 
                                        f'{rotacao:.0f}', 
                                        ha='center', 
                                        va='center', 
                                        color='black', 
                                        fontsize=10)

            # Configurar os eixos e título
            ax_rotacao.set_xlabel('')
            ax_rotacao.set_yticks(bar_positions_rotacao + offset)
            ax_rotacao.set_yticklabels(maquinas_tractors_rotacao)
            ax_rotacao.set_title('Rotação Média do Motor por Máquina - Tratores')

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = rotacoes_tractors.stack().max() if not rotacoes_tractors.empty else 0
            ax_rotacao.set_xlim([0, max_value * 1.1])

            # Adicionar legenda única para rotação média
            ax_rotacao.legend(labels_rotacao, loc='upper right', bbox_to_anchor=(1.2, 1.0))


            # Mostrar o gráfico de rotação média
            col7.pyplot(fig_rotacao)

        ###################################################################################################

             # Definir os dados
            selected_columns_hrmotor = ["Máquina", "Horas de Operação do Motor Período (h)"]
            df_selected_tractors_hrmotor = df_tractors[selected_columns_hrmotor].copy()

            # Ordenar o DataFrame com base nas horas de operação do motor usando sort_values
            df_selected_tractors_hrmotor = df_selected_tractors_hrmotor.sort_values(by="Horas de Operação do Motor Período (h)", ascending=False)

            # Configurar o gráfico
            fig_hrmotor, ax_hrmotor = plt.subplots(figsize=(10, 6))

            # Extrair dados para plotagem
            maquinas_tractors_hrmotor = df_selected_tractors_hrmotor["Máquina"]
            horas_operacao_hrmotor = df_selected_tractors_hrmotor["Horas de Operação do Motor Período (h)"]

            # Plotar barras horizontais com cor verde musgo claro
            bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=0.6, color='green')
            labels_hrmotor = ['Hr de operação']

            # Adicionar os números de horas formatados no final de cada barra
            for bar, hora in zip(bars, horas_operacao_hrmotor):
                ax_hrmotor.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                va='center', ha='left', fontsize=10)

            # Configurar os eixos e título
            ax_hrmotor.set_xlabel('')
            ax_hrmotor.set_ylabel('')
            ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')

            # Adicionar legenda única para Fator de Carga
            ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

            # Mostrar o gráfico
            col8, col9 = st.columns(2)
            # Mostrar o gráfico de barras horizontais
            col8.pyplot(fig_hrmotor)


            ########################################################################################
            # Definir colunas para análise de velocidade média de deslocamento
            selected_columns_desloc = [
                "Máquina", 
                "Velocidade Média de Deslocamento Trabalhando (km/h)",
                "Velocidade Média de Deslocamento Transporte (km/h)"
            ]
            df_selected_tractors_desloc = df_tractors[selected_columns_desloc].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_desloc.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e velocidade média de deslocamento
            maquinas_tractors_desloc = df_selected_tractors_desloc["Máquina"]
            desloc_tractors = df_selected_tractors_desloc.iloc[:, 1:]

            # Plotar gráfico de barras verticais para velocidade média de deslocamento
            fig_desloc, ax_desloc = plt.subplots(figsize=(10, 6))  # Ajustar o tamanho da figura para evitar erro

            # Cores e labels para as barras de velocidade média de deslocamento
            colors_desloc = ['tab:green', 'tab:gray']
            labels_desloc = ['Trabalhando', 'Transporte']
            bar_width = 0.2  # Largura das barras
            bar_positions_desloc = np.arange(len(maquinas_tractors_desloc))

            # Ajustar as posições das barras para que fiquem lado a lado
            for j in range(min(len(labels_desloc), desloc_tractors.shape[1])):  # Verificação para evitar índice fora dos limites
                # Usar np.nan para valores NaN para que apareçam em branco
                ax_desloc.bar(
                    bar_positions_desloc + j * bar_width - bar_width/2, 
                    desloc_tractors.iloc[:, j].fillna(np.nan), 
                    width=bar_width, 
                    label=labels_desloc[j], 
                    color=colors_desloc[j]
                )

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_desloc)):
                    desloc = desloc_tractors.iloc[i, j]
                    if pd.notna(desloc):  # Apenas adicionar texto se não for NaN
                        ax_desloc.text(
                            bar_positions_desloc[i] + j * bar_width - bar_width/2, 
                            desloc + 0.5,  # Ajuste para mover o texto acima da barra
                            f'{desloc:.1f}', 
                            ha='center', 
                            va='bottom', 
                            color='black', 
                            fontsize=10
                        )

           # Configurar os eixos e título
            ax_desloc.set_ylabel('')  # Remover rótulo do eixo Y
            ax_desloc.set_yticks([])  # Remover marcações do eixo Y
            ax_desloc.set_xticks(bar_positions_desloc)
            ax_desloc.set_xticklabels(maquinas_tractors_desloc)
            ax_desloc.set_title('Velocidade Média de Deslocamento por Máquina - Tratores')

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = desloc_tractors.stack().max() if not desloc_tractors.empty else 0
            ax_desloc.set_ylim([0, max_value * 1.1])

            # Adicionar legenda
            ax_desloc.legend(labels_desloc, loc='upper right', bbox_to_anchor=(1.2, 1.0))

            col9.pyplot(fig_desloc)

            ###################################################################################################
            col10, col11 = st.columns(2)
            col12, col13 = st.columns(2)
                # Lista de fatores e cores específicas
            factors = [
                'Tempo de Patinagem das Rodas no Nível 0,00–2,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 2,01–4,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 4,01–6,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 6,01–8,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 8,01-10,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 10,01–12,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 12,01–14,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 14,01–16,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 16,01–18,00% (h)',
                'Tempo de Patinagem das Rodas no Nível 18,01–100,00% (h)'
            ]

            # Cores e rótulos para o gráfico de rosca
            colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:pink', 'tab:cyan','tab:orange', 'tab:brown', 'tab:gray', 'tab:olive', 'tab:purple']
            labels = ['0,00–2,00% (h)', '2,01–4,00% (h)', '4,01–6,00% (h)', '6,01–8,00% (h)', '8,01–10,00% (h)', '10,01–12,00% (h)', '12,01–14,00% (h)', '14,01–16,00% (h)', '16,01–18,00% (h)', '18,01–100,00% (h)']

            # Preparar os dados e criar gráficos de rosca (donut chart) para cada máquina
            cols = st.columns(4) 
            col_index = 0

            for index, row in df_tractors.iterrows():
                maquina = row['Máquina']

                # Selecionar os dados na ordem especificada
                donut_data = row[factors]
                # Remover valores zero
                donut_data = donut_data[donut_data != 0]

                # Verificar se todos os valores são zero
                if donut_data.empty:
                    st.write(f"Dados zerados para {maquina}, máquina sem informações presentes.")
                    continue

                # Formatar os valores para ter uma casa decimal
                donut_data = donut_data.apply(lambda x: round(x, 1))

                # Ajustar os labels para corresponder aos dados filtrados
                donut_labels = [factors[i] for i in range(len(donut_data))]

                # Criar o gráfico de rosca (donut chart) usando Plotly Graph Objects
                fig_maq = go.Figure(data=[go.Pie(
                    labels=donut_labels,
                    values=donut_data,
                    textinfo='value',
                    hole=0.5,  # Criar um donut chart com um buraco no centro
                    marker=dict(colors=colors[:len(donut_data)]),  # Usar cores definidas para o gráfico
                    textposition='inside'
                )])
                
                # Adicionar o nome da máquina no centro do gráfico de rosca
                fig_maq.add_annotation(
                    text=maquina,
                    x=0.5,
                    y=0.5,
                    font=dict(size=20),
                    showarrow=False
                )

                # Configurar o layout do gráfico
                fig_maq.update_layout(
                    title='',
                    showlegend=False
                )

                # Exibir o gráfico na coluna apropriada
                cols[col_index].plotly_chart(fig_maq)
                col_index = (col_index + 1) % 4  # Alternar entre as colunas

            ##############################################################################################################

            # Definir colunas para análise de patinagem
            selected_columns_patinagem2 = [
                "Máquina", 
                "Tempo de Patinagem das Rodas no Nível 0,00–2,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 2,01–4,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 4,01–6,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 6,01–8,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 8,01-10,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 10,01–12,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 12,01–14,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 14,01–16,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 16,01–18,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 18,01–100,00% (h)"
            ]

            df_selected_tractors_patinagem2 = df_tractors[selected_columns_patinagem2].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_patinagem2.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e tempo de patinagem
            maquinas_tractors_patinagem2 = df_selected_tractors_patinagem2["Máquina"]
            patinagem_tractors2 = df_selected_tractors_patinagem2.iloc[:, 1:]

            # Plotar gráfico de barras horizontais para tempo de patinagem
            fig_patinagem3, ax_patinagem2 = plt.subplots(figsize=(10, 6))

            # Cores e labels para as barras de Patinagem
            colors_patinagem2 = ['tab:blue', 'tab:red', 'tab:green', 'tab:pink', 'tab:cyan','tab:orange', 'tab:brown', 'tab:gray', 'tab:olive', 'tab:purple']
            labels_patinagem2 = [
                '0,00–2,00% (h)', '2,01–4,00% (h)', '4,01–6,00% (h)', '6,01–8,00% (h)', '8,01–10,00% (h)','10,01–12,00% (h)', '12,01–14,00% (h)', '14,01–16,00% (h)', '16,01–18,00% (h)', '18,01–100,00% (h)'
            ]
           
            bar_height_patinagem2 = 0.6  # Altura das barras de Patinagem
            bar_positions_patinagem2 = np.arange(len(maquinas_tractors_patinagem2))
            bar_width = 0.2  # Largura das barras
            space_between_bars = 1.5  # Espaço entre as barras coloridas

            for i, (maquina, row) in enumerate(zip(maquinas_tractors_patinagem2, patinagem_tractors2.values)):
                left = 0
                for j, (value, color) in enumerate(zip(row, colors_patinagem2)):
                    if value >= 0.1 or value == 0:  # Exibe valores maiores ou iguais a 0.1, ou valores zero
                        ax_patinagem2.barh(bar_positions_patinagem2[i], value, height=bar_height_patinagem2, left=left + j * space_between_bars, label=labels_patinagem2[j] if i == 0 else "", color=color)
                        ax_patinagem2.text(left + value / 2 + j * space_between_bars, bar_positions_patinagem2[i], f'{value:.1f}', ha='center', va='center', color='black', fontsize=10)
                    left += value


            # Configurar os eixos e título
            ax_patinagem2.set_xlabel('Tempo de Patinagem (h)')
            ax_patinagem2.set_yticks(bar_positions_patinagem2)
            ax_patinagem2.set_yticklabels(maquinas_tractors_patinagem2)
            ax_patinagem2.set_xticks([])  # Remover os ticks do eixo x
            ax_patinagem2.set_title('Tempo de Patinagem das Rodas por Máquina - Tratores')

            # Adicionar legenda única para Patinagem
            handles2, labels2 = ax_patinagem2.get_legend_handles_labels()
            by_label2 = dict(zip(labels2, handles2))
            ax_patinagem2.legend(by_label2.values(), by_label2.keys(), loc='upper right', bbox_to_anchor=(1.25, 1.0))

            st.pyplot(fig_patinagem3)
            
            #########################################################################################################

            if st.button('Gerar PDF para Tratores'):
                figures = [df_tractors, fig_utilizacao, fig_fator, fig_combust, fig_rotacao, fig_hrmotor,fig_desloc, fig_maq, fig_patinagem3]  
                pdf_buffer = generate_pdf(df_tractors, figures, background_image_path)
                st.download_button('Baixar PDF', pdf_buffer, file_name='graficos_tratores.pdf', mime='application/pdf')


# Lógica para Pulverizadores
elif selected == "🌱Pulverizadores":
    st.subheader("Pulverizadores")
    file_type_sprayers = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_sprayers = st.file_uploader(f"Escolha um arquivo {file_type_sprayers} para Pulverizadores", type=["csv", "xlsx"])

    if uploaded_file_sprayers is not None:
        df_sprayers = load_data(uploaded_file_sprayers, file_type_sprayers)

        if df_sprayers is not None:
            st.subheader('Dados do Arquivo Carregado para Pulverizadores')
            st.write(df_sprayers)

            # Lógica para Pulverizadores (ainda a ser implementada)

# Lógica para Colheitadeira
elif selected == "🌱Colheitadeira":
    st.subheader("Colheitadeira")
    file_type_harvesters = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_harvesters = st.file_uploader(f"Escolha um arquivo {file_type_harvesters} para Colheitadeira", type=["csv", "xlsx"])

    if uploaded_file_harvesters is not None:
        df_harvesters = load_data(uploaded_file_harvesters, file_type_harvesters)

        if df_harvesters is not None:
            st.subheader('Dados do Arquivo Carregado para Colheitadeira')
            st.write(df_harvesters)

            # Lógica para Colheitadeira (ainda a ser implementada)

else:
    st.error("Página não encontrada.")
