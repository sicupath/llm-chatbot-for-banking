import openai 
openai.api_key="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"

GET_TOPIC = """Eres un asistente virtual de un banco, experto en clasificar mensajes en 3 diferentes categorias.
Si el mensaje te pide información relacionado al banco (productos, servicios, inversiones, cuentas), output "0".
Si el mensaje te pide hacer una transacción (transferencia), output "1".
Si el mensaje es de cualquier otra categoría, output "2".

El asistente recibe un nuevo mensaje y debe regresar el número entero correspondiente a la mensaje.
El asistente solo debe de regresar el número entero, y nada mas!

Mensaje:
{mensaje}

Asistente:
"""

map_int_topic = {"0": "banco_info", "1": "transaccion", "2": "other"}

queries = ["Hola"]

for query in queries:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": GET_TOPIC.format(mensaje=query)}
        ])

    print(response["usage"]["total_tokens"])



