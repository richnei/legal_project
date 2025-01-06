# Upload de Processos Jurídicos com RabbitMQ e OpenAI

Este projeto é uma aplicação para processamento automatizado de arquivos PDF relacionados a processos jurídicos. Ele utiliza o RabbitMQ para fila de mensagens, o OpenAI GPT para extração de informações, e outras ferramentas modernas para facilitar a integração e o fluxo de trabalho.

## Funcionalidades Principais

- **Upload de PDFs**: Interface amigável em Streamlit para upload de até 5 arquivos PDF.
- **Processamento Automático**: Extração de dados jurídicos importantes, como nomes de autores e réus, e seus documentos (CPF/CNPJ).
- **Armazenamento Estruturado**: Salvamento das informações extraídas em arquivos Excel.
- **Fila de Mensagens**: Gerenciamento de tarefas assíncronas usando RabbitMQ.

## Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Para a interface de upload de arquivos.
- **[RabbitMQ](https://www.rabbitmq.com/)**: Para fila de mensagens e processamento assíncrono.
- **[OpenAI API](https://openai.com/)**: Para extração de informações usando modelos avançados de linguagem.
- **[LangChain](https://www.langchain.com/)**: Para integração com vetores e processamento de texto.
- **[ChromaDB](https://docs.trychroma.com/)**: Para armazenamento e consulta eficiente de vetores.
- **Python**: Linguagem principal utilizada para desenvolver o projeto.

## Requisitos

- **Python 3.8** ou superior
- **RabbitMQ** instalado e configurado
- Uma conta OpenAI com chave de API
- Arquivo `.env` configurado com as seguintes variáveis:
  ```env
  RABBITMQ_HOST=localhost
  RABBITMQ_PORT=5672
  RABBITMQ_USER=guest
  RABBITMQ_PASS=guest
  RABBITMQ_QUEUE=process_queue
  OPENAI_API_KEY=sua_chave_aqui
  OPENAI_MODEL=gpt-4


## Instalação

Clone o repositório:

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

## Crie e ative o ambiente virtual:

python -m venv venv
source venv/bin/activate
ou
venv\Scripts\activate 

## Instale as dependências:

pip install -r requirements.txt

Configure o arquivo .env conforme mencionado nos requisitos.

Inicie o RabbitMQ e verifique se ele está rodando.

## Como Usar

Execute o Streamlit:

streamlit run app.py

Acesse a interface no navegador pelo link exibido no terminal.

Faça upload de arquivos PDF para iniciar o processamento.

Execute o consumidor para processar os arquivos na fila:

python consumer.py

As planilhas geradas serão salvas no diretório do projeto e o usuario é notificado.

Estrutura do Projeto

📂 seu-repositorio
├── app.py                # Interface Streamlit para upload
├── consumer.py           # Consumidor do RabbitMQ
├── utils/
│   └── rabbit.py         # Funções auxiliares para RabbitMQ
├── extractor/
│   └── pdf_extractor.py  # Lógica de extração de informações dos PDFs
├── requirements.txt      # Dependências do projeto
├── .env                  # Configurações do ambiente (não commitado)
└── README.md             # Documentação do projeto

Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

