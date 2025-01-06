# import json
# import re
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# def extract_info_from_pdf(
#     pdf_path: str,
#     openai_api_key: str,
#     model_name: str = "GPT-4o"
# ) -> dict:
#     loader = PyPDFLoader(pdf_path)
#     docs = loader.load()

#     splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
#     chunks = splitter.split_documents(docs)

#     embeddings = OpenAIEmbeddings(
#         openai_api_key=openai_api_key,
#         model="text-embedding-ada-002"
#     )
#     vectorstore = Chroma.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#         persist_directory=None
#     )
#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     llm = ChatOpenAI(
#         openai_api_key=openai_api_key,
#         model=model_name,
#         temperature=0.0,
#         verbose=True
#     )
#     chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         chain_type="stuff",
#         verbose=True
#     )

#     prompt = """
#         Considere que no documento jurídico, as seguintes convenções se aplicam:
#     - Se encontrar "Tipo: Promovente" ou "Promovente" ou "Requerente", isso se refere ao Autor do processo.
#     - Se encontrar "Tipo: Promovido" ou "Promovido" ou "Requerido", isso se refere ao Réu do processo.
#     - Se houver menções a CPF, CNPJ, ou RG ao lado de um Promovente, isso corresponde ao "Documento do autor".
#     - Se houver menções a CPF, CNPJ, ou RG ao lado de um Promovido, isso corresponde ao "Documento do réu".
#     - Pode haver múltiplos autores e réus. Caso sim, retorne todos em listas (ex.: "reus": ["Nome1", "Nome2"]).
#     - Se não constar, deixe em branco ou null.

#     Agora, **extraia**:
#     - Nome do autor
#     - Documento do autor
#     - Nome(s) do(s) réu(s)
#     - Documento(s) do(s) réu(s)

#     Retorne **exatamente** no formato JSON (sem nada além), com as chaves:

#     {
#     "autor_nome": "",
#     "autor_documento": "",
#     "reus": [],
#     "reus_documentos": []
#     }
#     Se alguma informação não existir, deixe em branco ou null.
#     Não inclua nada além do JSON.
#     """

#     raw_response_dict = chain.invoke(prompt)

#     raw_result_str = raw_response_dict["result"]

#     match = re.search(r"\{.*\}", raw_result_str, re.DOTALL)
#     if match:
#         json_str = match.group(0)
#         try:
#             data = json.loads(json_str)
#         except:
#             data = {
#                 "autor_nome": None,
#                 "autor_documento": None,
#                 "reus": [],
#                 "reus_documentos": []
#             }
#     else:
#         data = {
#             "autor_nome": None,
#             "autor_documento": None,
#             "reus": [],
#             "reus_documentos": []
#         }

#     return data

import json
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def extract_info_from_pdf(
    pdf_path: str,
    openai_api_key: str,
    model_name: str = "GPT-4o"
) -> dict:
    """Extrai informações jurídicas de um arquivo PDF.

    Realiza a leitura e processamento de um documento PDF, utiliza
    embeddings para busca no vetor store e e o modelo LLM da OpenIA para
    extrair as informações solicitadas.

    Args:
        pdf_path (str): Caminho do arquivo PDF a ser processado.
        openai_api_key (str): Chave de API para autenticação na OpenAI.
        model_name (str): Nome do modelo LLM a ser usado (GPT-4o).

    Returns:
        dict: Dicionário contendo as informações extraídas no formato:
            {
                "autor_nome": str,
                "autor_documento": str,
                "reus": list,
                "reus_documentos": list
            }
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model="text-embedding-ada-002"
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=None
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model=model_name,
        temperature=0.0,
        verbose=True
    )
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        verbose=True
    )

    prompt = """
        Considere que no documento jurídico, as seguintes convenções se aplicam:
    - Se encontrar "Tipo: Promovente" ou "Promovente" ou "Requerente", isso se refere ao Autor do processo.
    - Se encontrar "Tipo: Promovido" ou "Promovido" ou "Requerido", isso se refere ao Réu do processo.
    - Se houver menções a CPF, CNPJ, ou RG ao lado de um Promovente, isso corresponde ao "Documento do autor".
    - Se houver menções a CPF, CNPJ, ou RG ao lado de um Promovido, isso corresponde ao "Documento do réu".
    - Pode haver múltiplos autores e réus. Caso sim, retorne todos em listas (ex.: "reus": ["Nome1", "Nome2"]).
    - Se não constar, deixe em branco ou null.

    Agora, **extraia**:
    - Nome do autor
    - Documento do autor
    - Nome(s) do(s) réu(s)
    - Documento(s) do(s) réu(s)

    Retorne **exatamente** no formato JSON (sem nada além), com as chaves:

    {
    "autor_nome": "",
    "autor_documento": "",
    "reus": [],
    "reus_documentos": []
    }
    Se alguma informação não existir, deixe em branco ou null.
    Não inclua nada além do JSON.
    """

    raw_response_dict = chain.invoke(prompt)
    raw_result_str = raw_response_dict["result"]

    match = re.search(r"\{.*\}", raw_result_str, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            data = json.loads(json_str)
        except:
            data = {
                "autor_nome": None,
                "autor_documento": None,
                "reus": [],
                "reus_documentos": []
            }
    else:
        data = {
            "autor_nome": None,
            "autor_documento": None,
            "reus": [],
            "reus_documentos": []
        }

    return data
