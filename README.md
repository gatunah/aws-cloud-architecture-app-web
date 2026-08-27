\# ☁ Cloud Document Manager



Aplicación web contenerizada desarrollada como proyecto de arquitectura cloud utilizando servicios de Amazon Web Services (AWS).



El proyecto implementa una solución basada en una arquitectura pública en AWS, donde una aplicación Flask ejecutándose en contenedores Docker permite consultar documentos almacenados en Amazon S3 y generar eventos de auditoría mediante Amazon SQS.



\---



\# 📌 Descripción del proyecto



Cloud Document Manager es una aplicación web desarrollada con Flask y desplegada sobre Amazon EC2 utilizando Docker.



La aplicación permite:



\- Consultar documentos almacenados en Amazon S3.

\- Generar enlaces temporales de descarga mediante URLs prefirmadas.

\- Registrar eventos de uso mediante Amazon SQS.

\- Ejecutarse en una arquitectura escalable utilizando Amazon EC2 Auto Scaling.

\- Distribuir tráfico mediante Application Load Balancer.



\---



\# 🏗️ Arquitectura de solución



La arquitectura implementada utiliza servicios administrados de AWS para lograr disponibilidad, escalabilidad y separación de responsabilidades.



```

&#x20;                        Usuario

&#x20;                           |

&#x20;                           |

&#x20;                           ↓



&#x20;             Application Load Balancer

&#x20;                           |

&#x20;                           |

&#x20;                           ↓



&#x20;                EC2 Auto Scaling Group

&#x20;                           |

&#x20;             -----------------------------

&#x20;             |                           |

&#x20;             ↓                           ↓



&#x20;       EC2 Instance              EC2 Instance

&#x20;             |

&#x20;             |

&#x20;             ↓



&#x20;       Docker Container

&#x20;             |

&#x20;             |

&#x20;             ↓



&#x20;         Flask Application

&#x20;             |

&#x20;       ---------------------

&#x20;       |                   |

&#x20;       ↓                   ↓



&#x20;    Amazon S3           Amazon SQS



&#x20; Documentos        Auditoría de eventos

```



\---



\# ☁ Servicios AWS utilizados



\## Amazon EC2



Servicio utilizado para ejecutar las instancias Linux donde se despliega la aplicación.



Características:



\- Sistema operativo: Amazon Linux 2023.

\- Tipo de instancia: t2.micro / t3.micro.

\- Ejecución mediante contenedores Docker.

\- Integración mediante IAM Role.



\---



\## Docker



La aplicación Flask fue contenerizada utilizando Docker.



La imagen contiene:



\- Python 3.12.

\- Flask.

\- Librería boto3 para comunicación con AWS.

\- Código de aplicación.

\- Plantillas HTML.



Ejemplo de construcción:



```bash

docker build -t app-documentos:4.0 .

```



Ejecución:



```bash

docker run -d -p 80:80 \\

\--name app-documentos-v4 \\

app-documentos:4.0

```



\---



\## Amazon S3



Servicio utilizado para almacenamiento de documentos.



Bucket utilizado:



```

app-documentos-cloud-2026

```



Funciones implementadas:



\- Listado de documentos disponibles.

\- Generación de URLs temporales para descarga.

\- Acceso mediante SDK boto3.



\---



\## Amazon SQS



Servicio utilizado para registrar eventos de auditoría.



Cola utilizada:



```

app-documentos-auditoria-v1

```



Eventos registrados:



\- Consulta de documentos.

\- Descarga de documentos.



Ejemplo de evento:



```json

{

&#x20; "evento": "LISTAR\_DOCUMENTOS",

&#x20; "detalle": "Usuario consultó documentos disponibles",

&#x20; "fecha": "2026-08-27T00:00:00"

}

```



\---



\## IAM Role



Las instancias EC2 utilizan un perfil IAM para permitir la comunicación segura con servicios AWS.



Permite:



\- Acceso controlado a Amazon S3.

\- Envío de mensajes a Amazon SQS.



No se almacenan credenciales AWS dentro del código.



\---



\## Application Load Balancer



Servicio utilizado para distribuir solicitudes HTTP hacia las instancias disponibles.



Configuración:



\- Protocolo: HTTP

\- Puerto: 80

\- Target Group:

&#x20; 

```

tg-app-documentos-v1

```



\---



\## EC2 Auto Scaling



Servicio utilizado para mantener la capacidad de la aplicación.



Configuración:



```

Auto Scaling Group:



app-documentos-asg-v1

```



Características:



\- Capacidad deseada: 1 instancia.

\- Límite máximo: 2 instancias.

\- Creación mediante Launch Template.

\- Uso de AMI personalizada.



\---



\# 🖼️ Imagen personalizada AMI



Se creó una AMI personalizada para permitir la replicación de la aplicación.



AMI:



```

app-documentos-ami-v2

```



Incluye:



\- Amazon Linux 2023.

\- Docker instalado.

\- Aplicación Flask.

\- Configuración necesaria para ejecución.



Esta imagen permite que Auto Scaling cree nuevas instancias con la aplicación preparada.



\---



\# 📂 Estructura del proyecto



```

app-documentos/



├── app.py

│

├── Dockerfile

│

├── requirements.txt

│

├── templates/

│   └── index.html

│

├── README.md

│

└── .gitignore

```



\---



\# 🐍 Aplicación Flask



La aplicación utiliza:



```python

Flask

boto3

```



Componentes principales:



\## Consulta de documentos



La aplicación consulta objetos almacenados en S3:



```python

s3.list\_objects\_v2()

```



\---



\## Descarga segura



Los documentos se entregan mediante URLs temporales:



```python

generate\_presigned\_url()

```



\---



\## Auditoría mediante SQS



Los eventos son enviados utilizando:



```python

sqs.send\_message()

```



\---



\# 🔐 Seguridad



Buenas prácticas implementadas:



\- Uso de IAM Role para acceso AWS.

\- No almacenar claves AWS dentro del código.

\- Uso de Security Groups.

\- Uso de llaves SSH para acceso EC2.

\- Separación entre aplicación y servicios AWS.



\---



\# 🚀 Despliegue



Flujo de despliegue:



```

Código Flask

&#x20;     |

&#x20;     ↓

Docker Image

&#x20;     |

&#x20;     ↓

EC2

&#x20;     |

&#x20;     ↓

AMI personalizada

&#x20;     |

&#x20;     ↓

Auto Scaling

&#x20;     |

&#x20;     ↓

Load Balancer

```



\---



\# 🧪 Validaciones realizadas



Durante la implementación se verificó:



✅ Aplicación Flask funcionando.



✅ Contenedor Docker ejecutándose.



✅ Comunicación con Amazon S3.



✅ Registro de eventos mediante Amazon SQS.



✅ Creación de AMI personalizada.



✅ Creación de instancias mediante Auto Scaling.



✅ Distribución mediante Application Load Balancer.



\---



\# 🛠️ Tecnologías utilizadas



| Tecnología | Uso |

|---|---|

| Python | Lenguaje principal |

| Flask | Framework web |

| Docker | Contenerización |

| Amazon EC2 | Computación |

| Amazon S3 | Almacenamiento |

| Amazon SQS | Mensajería |

| IAM | Control de permisos |

| ALB | Balanceo de tráfico |

| Auto Scaling | Escalabilidad |



\---



\# 📚 Proyecto AWS Academy



Proyecto desarrollado como parte del aprendizaje de arquitectura cloud utilizando Amazon Web Services.



Objetivo:



Diseñar, implementar y documentar una solución cloud utilizando servicios fundamentales de AWS, aplicando conceptos de:



\- Computación en la nube.

\- Contenedores.

\- Almacenamiento.

\- Mensajería.

\- Escalabilidad.

\- Alta disponibilidad.



\---



\# Autor



Daniela Francisca Oyarce Rodríguez



AWS Academy - Cloud Architecture Project

