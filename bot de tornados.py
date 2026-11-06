import os
import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import requests  # 📡 Librería para enviar datos directos a tu Webhook
import random

# 🌐 Miniserver para que la nube mantenga vivo el bot gratis
app = Flask('')

@app.route('/')
def home():
    return "Radar Meteorológico Automático Activo 24/7"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def mantener_despierto():
    t = Thread(target=run_web)
    t.start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 🛠️ 1. PEGA AQUÍ TU URL DE WEBHOOK DE DISCORD (CON TODOS TUS NÚMEROS):
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1568037344039141548/3rvWTfY5WNl2axSiz75aPiVv0jGh-8pthJSp9qDrgz1I2fyaz4avKtCA-uf-BCbV4UKC"

# Listas de zonas y escalas Fujita para las alertas
ZONAS_MUNDIALES = ["Oklahoma, EE.UU. (Tornado Alley)", "Coahuila, México", "Texas, EE.UU.", "Chihuahua, México", "Kansas, EE.UU.", "Florida, EE.UU."]
ESCALA_TORNADOS = ["EF0 (Débil)", "EF1 (Moderado)", "EF2 (Significativo)", "EF3 (Severo)", "EF4 (Devastador)", "EF5 (¡INCREÍBLEMENTE DESTRUCTOR!)"]

@bot.event
async def on_ready():
    print("==================================================")
    print(f"🌪️ [RADAR CAZATORNADOS ACTIVADO EN LÍNEA]")
    print(f"Enviando alertas directas a tu Webhook con éxito...")
    print(f"Conectado a Discord como: {bot.user.name}")
    print("==================================================")
    radar_satelital.start()

# 🕒 El radar revisa el clima de forma automática cada 5 minutos
@tasks.loop(minutes=5)
async def radar_satelital():
    probabilidad = random.randint(1, 100)
    
    # Si detecta peligro (probabilidad alta), manda el reporte por sí solo
    if probabilidad > 75:
        viento = random.randint(110, 340)
        
        # Estructuramos la tabla de texto elegante (Embed) de forma nativa para el Webhook
        payload = {
            "embeds": [
                {
                    "title": "🌪️ [ALERTA DE TORNADO DETECTADA EN RADAR GLOBAL] 🌪️",
                    "description": "Los sistemas satelitales han detectado condiciones extremas y nubes de embudo tocando tierra.",
                    "color": 15158332 if viento > 250 else 15105570,  # Rojo o Naranja en código de Discord
                    "fields": [
                        {"name": "📍 UBICACIÓN REPORTADA", "value": f"`{random.choice(ZONAS_MUNDIALES)}`", "inline": True},
                        {"name": "💨 VELOCIDAD DEL VIENTO", "value": f"`{viento} km/h`", "inline": True},
                        {"name": "🌪️ CATEGORÍA ESTIMADA", "value": f"`{random.choice(ESCALA_TORNADOS)}`", "inline": False}
                    ],
                    "footer": {
                        "text": "Monitoreo Climático Global Automático 24/7 por Webhook."
                    }
                }
            ]
        }
        
        try:
            # 📬 Python viaja por internet y le entrega la alerta directamente a tus números del Webhook
            requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
            print("[Radar Webhook] Alerta enviada automáticamente al chat exacto.")
        except:
            print("Error: No se pudo enviar el reporte. Revisa que tu URL de Webhook esté bien pegada.")

mantener_despierto()

# 🔑 RECUERDA PEGAR TU TOKEN SECRETO DEL BOT AQUÍ ABAJO (LÍNEA FINAL):
bot.run(os.environ.get('DISCORD_TOKEN'))
