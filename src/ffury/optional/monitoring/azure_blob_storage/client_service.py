import os

from azure.storage.blob import BlobServiceClient


def get_client_service() -> BlobServiceClient:
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if conn_str is None or conn_str == "":
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING non definie")
    return BlobServiceClient.from_connection_string(conn_str=conn_str)
