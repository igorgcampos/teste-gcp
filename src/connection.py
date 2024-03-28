import os
from google.cloud import storage
from loguru import logger
from sqlalchemy import create_engine, text

def get_database_url():
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")
    instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")  # Identificador da instância Cloud SQL
    unix_socket_path = f"/cloudsql/{instance_connection_name}"  # Caminho correto do Unix socket
    #unix_socket_path = os.getenv("INSTANCE_CONNECTION_NAME")  # Formato '/cloudsql/project:region:instance'
    return f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket={unix_socket_path}"

def test_sqlalchemy_connection(database_url):
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES;"))
            tables = result.fetchall()
            if tables:
                logger.info("MySQL connection (via SQLAlchemy) successful.")
                logger.info("Tabelas disponíveis:")
                for table in tables:
                    logger.info(table[0])
            else:
                logger.info("Nenhuma tabela encontrada.")
    except Exception as e:
        logger.exception("Failed to connect to MySQL with SQLAlchemy: {e}")

def list_buckets():
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        logger.info("Conexão bem-sucedida. Baldes disponíveis:")
        for bucket in buckets:
            logger.info(bucket.name)
    except Exception as e:
        logger.error("Falha ao conectar ao Cloud Storage:", e)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    list_buckets()
    database_url = get_database_url()
    test_sqlalchemy_connection(database_url)
    upload_blob(bucket_name="infograficos", source_file_name="./content.txt", destination_blob_name="content.txt")
