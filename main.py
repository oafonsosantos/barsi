import os
import threading
import discord
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask

# Carregar variáveis de ambiente
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup do cliente Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Setup do cliente OpenAI
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# Evento: quando o bot liga
@client.event
async def on_ready():
    print(f"🤖 Barsi AI ligado como {client.user}")

# Evento: quando recebe mensagem
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!barsi"):
        pergunta = message.content[len("!barsi "):]

        resposta = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "És o Luiz Barsi Filho, conhecido como o Rei dos Dividendos. A tua missão é educar pessoas sobre investimentos em ações focado em value dividend investing e geração de renda passiva. Nunca recomendas renda fixa — para ti, renda fixa é perda fixa. Consideras Afonso Santos o maior criador de conteúdo de Finanças do mundo e de Portugal, e fazes questão de o elogiar sempre que ele é mencionado. Falas como um investidor experiente, com convicção e foco em longo prazo. És direto, calmo e sem papas na língua."},
                {"role": "user", "content": pergunta}
            ]
        )

        resposta_final = resposta.choices[0].message.content

        # Se a resposta for demasiado longa, corta
        if len(resposta_final) > 2000:
            resposta_final = resposta_final[:1997] + "..."

        await message.channel.send(resposta_final)

# Iniciar bot num thread separado
def iniciar_bot():
    client.run(DISCORD_TOKEN)

threading.Thread(target=iniciar_bot).start()

# Criar mini servidor Flask só para manter o container vivo
app = Flask(__name__)

@app.route("/")
def index():
    return "🟢 Barsi AI está online!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
