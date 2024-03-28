import os
from google.cloud import storage
from loguru import logger
import mysql.connector

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logger.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:
        logger.exception(e)

def list_buckets():
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        logger.info("Conexão bem-sucedida. Baldes disponíveis:")
        for bucket in buckets:
            logger.info(bucket.name)
    except Exception as e:
        logger.error("Falha ao conectar ao Cloud Storage:", e)

def test_mysql_connection(socket_path, user, password, database):
    try:
        conn = mysql.connector.connect(unix_socket=socket_path, user=user, password=password, database=database)
        if conn.is_connected():
            logger.info("MySQL connection successful.")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            logger.info("Tabelas disponíveis:")
            for table in tables:
                logger.info(table[0])
            cursor.close()
            conn.close()
    except Exception as e:
        logger.exception("Failed to connect to MySQL:", e)

if __name__ == "__main__":
    list_buckets()
    instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
    socket_path = f"/cloudsql/{instance_connection_name}"
    test_mysql_connection(
        socket_path=socket_path,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
    )
    upload_blob(bucket_name="infograficos", source_file_name="./content.txt", destination_blob_name="content.txt")
