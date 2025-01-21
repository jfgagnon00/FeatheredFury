import os

from azure.storage.blob import BlobServiceClient
from datetime import datetime, timezone


def get_timestamp():
    now = datetime.now( timezone.utc )
    ts = now.timestamp()
    print("now:", datetime.fromtimestamp(ts))
    return str(ts)

def convert_timestamp(ts):
    ts = float(ts)
    now = datetime.fromtimestamp(ts)
    print("now:", now)

data = b"Hello World"
meta_data = { "timestamp": get_timestamp()}
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

client_service = BlobServiceClient.from_connection_string(conn_str=conn_str)

# ecriture
print("Check container")
container_client = client_service.get_container_client("reference")
if container_client is None or not container_client.exists():
    print("Create container")
    container_client = client_service.create_container("reference")

blob_client = container_client.upload_blob(name="data", data=data, overwrite=True)

meta = blob_client.get_blob_properties().metadata
meta.update(meta_data)
blob_client.set_blob_metadata(meta)

# lecture
container_client = client_service.get_container_client(container="reference")
for b in container_client.list_blobs():
    blob_client = container_client.get_blob_client(b.name)
    data = blob_client.download_blob(encoding="UTF-8").readall()
    meta = blob_client.get_blob_properties().metadata
    convert_timestamp(meta["timestamp"])
    print(data)
