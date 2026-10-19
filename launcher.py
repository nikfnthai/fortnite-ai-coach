import time
import keyboard
import pyautogui
import pyttsx3
import io
import base64
import pygetwindow as gw
from PIL import Image
from openai import OpenAI
import customtkinter as ctk

# Configurazione grafica iniziale
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fortnite AI Coach Launcher")
app.geometry("400x520")
app.resizable(False, False)

# Inizializzazione sintesi vocale
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def parla(testo, genere="Maschile"):
    print(f"🤖 Bot: {testo}")
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        if genere == "Femminile":
            engine.setProperty('voice', voices[1].id)
        else:
            engine.setProperty('voice', voices[0].id)
            
    engine.say(testo)
    engine.runAndWait()

def è_in_gioco():
    try:
        finestra_attiva = gw.getActiveWindow()
        if finestra_attiva and "fortnite" in finestra_attiva.title.lower():
            return True
    except Exception:
        pass
    return False

def analizza_giocata():
    if switch_attivo.get() == 0:
        return
    
    if not è_in_gioco():
        print("⚠️ Fortnite non è in primo piano. Ignorato.")
        return

    parla("Analizzo...", combo_voce.get())
    
    api_key = entry_key.get().strip()
    if not api_key or api_key == "Inserisci API Key OpenAI":
        parla("Inserisci una chiave API valida.")
        return

    client = OpenAI(api_key=api_key)
    
    try:
        screenshot = pyautogui.screenshot()
        buffered = io.BytesIO()
        screenshot.save(buffered, format="JPEG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Sei un coach pro-player di Fortnite. Analizza lo screenshot e dai UN SOLO consiglio tattico immediato (massimo 10 parole)."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Cosa faccio adesso?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                },
            ],
            max_tokens=50,
        )

        consiglio = response.choices[0].message.content
        parla(consiglio, combo_voce.get())

    except Exception as e:
        print(f"Errore: {e}")
        parla("Errore durante l'analisi.")

# --- INTERFACCIA GRAFICA (GUI) ---

label_title = ctk.CTkLabel(app, text="🎮 Fortnite AI Coach", font=("Arial", 22, "bold"))
label_title.pack(pady=15)

entry_key = ctk.CTkEntry(app, width=320, placeholder_text="Inserisci la tua API Key OpenAI (sk-...)")
entry_key.pack(pady=5)

switch_attivo = ctk.CTkSwitch(app, text="Assistente Live Attivo")
switch_attivo.select()
switch_attivo.pack(pady=15)

label_key = ctk.CTkLabel(app, text="Tasto Rapido Fissato: [ CAPS LOCK ]", text_color="cyan")
label_key.pack(pady=5)

label_voce = ctk.CTkLabel(app, text="Genere Voce Assistente:")
label_voce.pack(pady=2)
combo_voce = ctk.CTkOptionMenu(app, values=["Maschile", "Femminile"])
combo_voce.pack(pady=5)

def apri_guida():
    guida_win = ctk.CTkToplevel(app)
    guida_win.title("Guida & Regolamento")
    guida_win.geometry("350x300")
    txt = ctk.CTkTextbox(guida_win, width=320, height=260)
    txt.pack(pady=10)
    txt.insert("0.0", "📜 GUIDA RAPIDA:\n\n1. Inserisci la tua API Key di OpenAI.\n2. Assicurati che lo switch sia su Attivo.\n3. Apri Fortnite in modalità finestra o borderless.\n4. Premi CAPS LOCK in partita per ricevere il consiglio vocale nell'orecchio!")

btn_guida = ctk.CTkButton(app, text="📜 Leggi Guida & Regolamento", fg_color="transparent", border_width=1, command=apri_guida)
btn_guida.pack(pady=20)

keyboard.add_hotkey('caps lock', analizza_giocata)

app.mainloop()
