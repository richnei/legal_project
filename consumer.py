import ast
import pandas as pd
from decouple import config
from extractor.pdf_extractor import extract_info_from_pdf
from utils.rabbit import get_rabbitmq_channel

OPENAI_API_KEY = config("OPENAI_API_KEY")
OPENAI_MODEL = config("OPENAI_MODEL")

def process_and_save(file_path, original_name, extracted_data):
    """Processa os dados extraídos e salva no formato adequado.

    Args:
        file_path (str): Caminho do arquivo PDF processado.
        original_name (str): Nome original do arquivo PDF.
        extracted_data (dict): Dados extraídos do PDF.
    """
    for key, val in extracted_data.items():
        if val is None or (isinstance(val, list) and not val):
            extracted_data[key] = "Não consta"
        elif isinstance(val, list):
            extracted_data[key] = ", ".join(val)

    df = pd.DataFrame([extracted_data])

    autor_nome = extracted_data["autor_nome"]
    if autor_nome == "Não consta" or not autor_nome:
        base_filename = f"SemAutor_{original_name}.xlsx"
    else:
        autor_sanitizado = autor_nome.replace(" ", "_")
        base_filename = f"{autor_sanitizado}.xlsx"

    df.to_excel(base_filename, index=False)
    print(f"[✓] Planilha gerada: {base_filename}")

def callback(ch, method, properties, body):
    """Callback executado quando uma mensagem chega na fila do RabbitMQ."""
    message = ast.literal_eval(body.decode("utf-8"))
    file_path = message["file_path"]
    original_name = message["original_name"]

    extracted_data = extract_info_from_pdf(
        pdf_path=file_path,
        openai_api_key=OPENAI_API_KEY,
        model_name=OPENAI_MODEL,
    )

    process_and_save(file_path, original_name, extracted_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    """Inicia o consumidor."""
    channel, connection = get_rabbitmq_channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="process_queue", on_message_callback=callback)

    print("[*] Aguardando mensagens na fila. CTRL+C para sair.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
