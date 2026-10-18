import time
import keyboard
import pyautogui
import pyttsx3
import io
import base64
from PIL import Image
from openai import OpenAI

# Inizializza la sintesi vocale locale
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Inserisci la tua API Key di OpenAI
client = OpenAI(api_key="LA_TUA_OPENAI_API_KEY")

def parla(testo):
    print(f"🤖 Bot: {testo}")
    engine.say(testo)
    engine.runAndWait()

def cattura_schermo():
    screenshot = pyautogui.screenshot()
    buffered = io.BytesIO()
    screenshot.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analizza_giocata():
    parla("Analizzo lo schermo...")
    base64_image = cattura_schermo()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Sei un coach esperto di Fortnite. Analizza lo screenshot e dai UN SOLO consiglio tattico ultra-conciso (massimo 15 parole) su posizionamento, salute, scudo o armi."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Cosa devo fare adesso in partita?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=100,
        )

        consiglio = response.choices[0].message.content
        parla(consiglio)

    except Exception as e:
        print(f"Errore: {e}")
        parla("Errore durante l'analisi.")

print("🎮 Coach Fortnite AI Attivo!")
print("Premi F9 in partita per ricevere il consiglio vocale.")

keyboard.add_hotkey('F9', analizza_giocata)
keyboard.wait()
