import streamlit as st
import plotly.express as px

# Dados de exemplo para o gráfico de donut
data = dict(
    categories=["A", "B", "C", "D"],
    values=[20, 30, 25, 25]
)

# Criar figura usando Plotly Express
fig = px.pie(data, values='values', names='categories', hole=0.5)

# Configurações do layout do gráfico
fig.update_layout(
    title='Gráfico de Donut',
    showlegend=True,
    legend=dict(
        orientation='h',  # Orientação horizontal para a legenda
        yanchor='bottom',  # Ancoragem da legenda na parte inferior
        y=-0.2,  # Posição vertical em relação ao gráfico (valor negativo para posicionar abaixo)
        xanchor='center',  # Ancoragem da legenda ao centro
        x=0.5  # Posição horizontal em relação ao gráfico
    ),
    annotations=[
        dict(
            text='Texto no Centro',
            x=0.5,
            y=0.5,
            font=dict(size=20),
            showarrow=False
        )
    ]
)

# Exibir o gráfico no aplicativo Streamlit
st.title("Donut Chart Infographic")
st.plotly_chart(fig)
