import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Nome do arquivo de banco de dados
DB_FILE = 'ocorrencias.xlsx'

# Função para inicializar o Excel se não existir
def init_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=['ID', 'Data', 'Tipo', 'Descricao', 'Prioridade', 'Status'])
        df.to_excel(DB_FILE, index=False)

def salvar_ocorrencia(tipo, desc, prioridade):
    df = pd.read_excel(DB_FILE)
    novo_id = len(df) + 1
    nova_linha = {
        'ID': novo_id,
        'Data': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'Tipo': tipo,
        'Descricao': desc,
        'Prioridade': prioridade,
        'Status': 'Pendente'
    }
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_excel(DB_FILE, index=False)

# Interface do App
st.title("🚨 Registro de Ocorrências")
init_db()

with st.form("form_ocorrencia", clear_on_submit=True):
    tipo = st.selectbox("Tipo da Ocorrência", ["Manutenção", "Segurança", "TI", "Outros"])
    prioridade = st.select_slider("Prioridade", options=["Baixa", "Média", "Alta"])
    descricao = st.text_area("Descrição detalhada")
    
    submit = st.form_submit_button("Registrar Ocorrência")
    
    if submit:
        if descricao:
            salvar_ocorrencia(tipo, descricao, prioridade)
            st.success(f"Ocorrência registrada com sucesso!")
        else:
            st.error("Por favor, preencha a descrição.")

st.divider()
st.subheader("Histórico de Registros")
st.dataframe(pd.read_excel(DB_FILE), use_container_width=True)