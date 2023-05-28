# Asistente Virtual


## Motivación

Los modelos de lenguaje natural procesado han llegado para revolucionar la manera en la que interactuamos con sistemas inteligentes, especificamente asistentes virtuales y chatbots.
Desde su su creación, estos modelos ya cuentan con una vasta cantidad de conocimiento de todo tipo. Sin embargo, ¿Qué sucede si lo queremos hacer experto en un area? Para esto, podemos utilizar los mismos models previamente mencionados y darle acceso a documentos 
con los que podrá tener conversaciones y responder preguntas.


## ¿Qué/Quién es Quetzal?

Quetzal es un asistente virtual basado en el modelo GPT 3.5 de Openai. Este asistente tiene acceso a la base de datos generada por el equipo que contiene alguno de los productos mas populares de Banorte. Con este conocimiento agregado, Quetzal es capaz de responder preguntas complejas, poco explicitas, poco estructuras o con errores gramáticales. Esto le ofrece una gran ventaja frente a los asistentes virtuales tradicionales.

## Funcionalidad

El código actual funciona para que el asistente responda a mensajes de Telegram, esto debido a la facilidad con la que se puede obtener acceso a la API de dicho servicio de mensajería.
* El asistente puede recibir mensajes de texto y contestarlos utilizando los documentos proporcionados.
* El asistente puede recibir mensajes de voz transcribirlos a texto utilizando Whisper (OpenAI) y contestarlos utilizando los documentos proporcionados relacionados.


## ¿Cómo funciona?

A simples rasgos, cuando el asistente recibe un mensaje buscará información relevante en los documentos proveidos y responderá la pregunta utilizando solo el contenido autorizado.
Esta tarea parece simple, sin embargo, para que la experiencia sea lo mas fluida y eficaz posible se presentan algunos desafios. A continuación los presentamos y como fueron resueltos.
* Desafio: La pregunta del usuario puede ser implicita de la conversación pasada.
* Solución: Guardamos la conversación del asistente con cada cliente en una base de datos Redis (tipo cache, rápido acceso).
* Personalización: No existe un servicio diferente para los diferentes perfiles de usuario.
* Solución: Crear diferentes agentes (asistentes) donde cada uno tiene especificaciones para el tipo de cliente con el que trabajará.
* Desafio: El cliente puede no tener una pregunta, simplemente quiere explorar sus opciones.
* Solución: El asistente ha sido programada para reconocer este tipo de mensajes y lo que hará será tratar la conversación basado en el tipo de cliente con el que esta trabajando y le indicará recomendaciones dependiendo de ello.



## Activar al asistente

Crear un archivo `.env` e incluir las variables requeridas para el funcionamiento.
```
OPENAI_API_KEY=""
TELEGRAM_TOKEN=""
REDIS_URL=""
```

Para levantar el servidor se utiliza Docker-compose. Esto comenzará el servidor de Fastapi, Nginx y Redis.
```
docker compose up
```


