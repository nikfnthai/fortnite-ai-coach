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
    parla("Analizzo...")
    base64_image = cattura_schermo()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Sei un coach pro-player di Fortnite. Analizza lo screenshot e dai UN SOLO consiglio tattico immediato (massimo 10-12 parole) su posizionamento, salute o fight."
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
            max_tokens=80,
        )

        consiglio = response.choices[0].message.content
        parla(consiglio)

    except Exception as e:
        print(f"Errore: {e}")
        parla("Errore durante l'analisi.")

print("🎮 Coach Fortnite AI Attivo per Torneo!")
print("Premi il tasto CAPS LOCK in partita per ricevere il consiglio vocale all'istante!")

keyboard.add_hotkey('caps lock', analizza_giocata)
keyboard.wait()
