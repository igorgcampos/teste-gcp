import os
from google.cloud import storage
from loguru import logger
import mysql.connector


def upload_blob(
    bucket_name, source_file_name, destination_blob_name
):  # pylint: disable=C0116
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        logger.info(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:  # pylint: disable=W0718
        logger.exception(e)


def list_buckets():  # pylint: disable=C0116
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        logger.info("Conexão bem-sucedida. Baldes disponíveis:")
        for bucket in buckets:
            logger.info(bucket.name)
    except Exception as e:  # pylint: disable=W0718
        logger.error("Falha ao conectar ao Cloud Storage:", e)


def test_mysql_connection(
    host, user, password, database
):  # pylint: disable=W0621,C0116
    try:
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

        if connection.is_connected():
            logger.info("Conexão bem-sucedida ao banco de dados MySQL!")
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            logger.info("Tabelas disponíveis:")
            for table in tables:
                logger.info(table[0])
            cursor.close()
            connection.close()
    except Exception as e:  # pylint: disable=W0718
        logger.exception(e)


if __name__ == "__main__":
    list_buckets()
    test_mysql_connection(
        host=os.getenv("INSTANCE_CONNECTION_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
    )
    upload_blob(bucket_name="infograficos", source_file_name="./content.txt", destination_blob_name="content.txt")
