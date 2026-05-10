import requests
from datetime import datetime
import boto3
import os

URL = "https://siata.gov.co/ultimasFotosCamaras/ultimacam_incendio_girardota_norte.jpg"

# Descargar imagen
img = requests.get(URL).content

# Nombre con fecha y hora
nombre = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

# Guardar temporalmente
with open(nombre, "wb") as f:
    f.write(img)

# Conexión Cloudflare R2
s3 = boto3.client(
    service_name='s3',
    endpoint_url=os.environ['R2_ENDPOINT'],
    aws_access_key_id=os.environ['R2_ACCESS_KEY'],
    aws_secret_access_key=os.environ['R2_SECRET_KEY'],
)

# Subir al bucket
s3.upload_file(nombre, "siata-camaras", nombre)

print("Imagen subida:", nombre)
