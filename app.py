import streamlit as st
import tempfile

from utils.rabbit import send_message

st.set_page_config(
    page_title="Upload de Processos Jurídicos",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="auto"
)

custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        max-width: 600px;
        margin: 0 auto;
        padding-top: 1rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Upload de Processos Jurídicos")
st.write("Faça upload de 1 a 5 cópias integrais de processos jurídicos em formato PDF.")

uploaded_files = st.file_uploader(
    label="Selecione um ou mais arquivos PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Enviar"):
    """Processa o upload de arquivos PDF e envia para analise.

    Realiza a validação dos arquivos enviados pelo usuário, salva
    temporariamente no servidor e adiciona mensagens à fila RabbitMQ.

    Raises:
        ValueError: Caso nenhum arquivo seja enviado ou mais de 5 arquivos sejam carregados.
    """
    if not uploaded_files:
        st.warning("Por favor, selecione ao menos um arquivo PDF.")
    elif len(uploaded_files) > 5:
        st.warning("Você pode fazer upload de no máximo 5 arquivos PDFs.")
    else:
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            message_dict = {
                "file_path": tmp_path,
                "original_name": file.name
            }
            send_message(message_dict)

        st.success(f"{len(uploaded_files)} arquivos enviados para analise na fila!")