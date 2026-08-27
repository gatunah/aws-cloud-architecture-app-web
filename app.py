from flask import Flask, render_template, redirect
import boto3
import json
from datetime import datetime

app = Flask(__name__)

BUCKET_NAME = "app-documentos-cloud-2026"

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/169222583198/app-documentos-auditoria-v1"

s3 = boto3.client("s3", region_name="us-east-1")
sqs = boto3.client("sqs", region_name="us-east-1")


def enviar_evento(tipo_evento, detalle):

    mensaje = {
        "evento": tipo_evento,
        "detalle": detalle,
        "fecha": datetime.utcnow().isoformat()
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(mensaje)
    )


@app.route("/")
def inicio():

    archivos = []

    try:
        respuesta = s3.list_objects_v2(
            Bucket=BUCKET_NAME
        )

        for objeto in respuesta.get("Contents", []):
            archivos.append(objeto["Key"])

        enviar_evento(
            "LISTAR_DOCUMENTOS",
            "Usuario consultó documentos disponibles"
        )

    except Exception:
        archivos.append("Error conectando a S3")


    return render_template(
        "index.html",
        bucket=BUCKET_NAME,
        archivos=archivos
    )


@app.route("/descargar/<nombre>")
def descargar(nombre):

    enviar_evento(
        "DESCARGA_DOCUMENTO",
        nombre
    )

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": nombre
        },
        ExpiresIn=3600
    )

    return redirect(url)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=80
    )
