# main.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------------------------------
# 1) VERIFICACIÓN DEL WEBHOOK (GET)
# ---------------------------------------------------
@app.route('/')
def home():
    return "🚀 Servidor Flask funcionando correctamente"

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Meta (WhatsApp) enviará un GET con ?hub.mode=subscribe&hub.verify_token=<...>&hub.challenge=<...>
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    
    if mode == 'subscribe' and token == "EAAOFr299ugQBOZCY7JTZBe2vydfOS2kNglVV5A0kVZB5i8H47eOtS2XUxD4SH9IIaRGHBDfY5ugSQ4zPs3OEsXEI2BpVx5GXqrnEZAe5i3qlBkU1gNUTy8wliFVzs1eIdwMp73TPW9Tjz8TarQgdzZAtw2sZCWDaXghxZAMw8g5DtXGnjUEYSp70j51PqXZC4TwEi31gb8ChuvlV90bkzn5X4BZARr4UZD":
        print("✅ Webhook verificado correctamente.")
        return challenge, 200
    else:
        print("❌ Fallo en la verificación del webhook.")
        return "Error de verificación", 403


# ---------------------------------------------------
# 2) RECIBIR MENSAJES (POST)
# ---------------------------------------------------
@app.route('/webhook', methods=['POST'])
def receive_message():
    """
    Aquí WhatsApp enviará las notificaciones de mensajes entrantes.
    Vamos a imprimir el contenido y responder automáticamente.
    """
    data = request.get_json()
    print("=== Mensaje entrante ===")
    print(data)

    if data and "entry" in data and len(data["entry"]) > 0:
        changes = data["entry"][0].get("changes")
        if changes and len(changes) > 0:
            value = changes[0].get("value")
            messages = value.get("messages")
            if messages and len(messages) > 0:
                incoming_msg = messages[0]["text"]["body"]
                from_number = messages[0]["from"] 
                print(f"📩 Mensaje de {from_number}: {incoming_msg}")

                # Responder 
                reply_text = f"¡Hola! Recibimos tu mensaje: {incoming_msg}"
                send_whatsapp_message(reply_text, from_number)

    return jsonify({"status": "ok"}), 200


# ---------------------------------------------------
# 3) FUNCIÓN PARA RESPONDER MENSAJES
# ---------------------------------------------------
def send_whatsapp_message(message_text, recipient_number):
    """
    Enviar un mensaje de WhatsApp usando la API de Meta.
    """
    phone_number_id = "588358997696171"  
    access_token = "EAAOFr299ugQBOZCY7JTZBe2vydfOS2kNglVV5A0kVZB5i8H47eOtS2XUxD4SH9IIaRGHBDfY5ugSQ4zPs3OEsXEI2BpVx5GXqrnEZAe5i3qlBkU1gNUTy8wliFVzs1eIdwMp73TPW9Tjz8TarQgdzZAtw2sZCWDaXghxZAMw8g5DtXGnjUEYSp70j51PqXZC4TwEi31gb8ChuvlV90bkzn5X4BZARr4UZD" 

    url = f"https://graph.facebook.com/v16.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 Respuesta de la API de WhatsApp:", response.status_code, response.json())


# ---------------------------------------------------
# 4) EJECUTAR EL SERVIDOR
# ---------------------------------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
