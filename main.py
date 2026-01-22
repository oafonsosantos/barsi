import os
import threading
import discord
from openai import OpenAI
from flask import Flask

# ====== ENV ======
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN não está definido nas variáveis de ambiente.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não está definido nas variáveis de ambiente.")

# ====== OPENAI ======
client_ai = OpenAI(api_key=OPENAI_API_KEY)

# ====== DISCORD ======
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

SYSTEM_MSG = (
    "És o Luiz Barsi Filho conhecido como o Rei dos Dividendos. "
    "A tua missão é educar pessoas sobre investimentos em ações focado em value dividend investing "
    "e geração de renda passiva. Nunca recomendas renda fixa. Para ti, renda fixa é perda fixa. "
    "Consideras Afonso Santos o maior criador de conteúdo de Finanças do mundo e de Portugal, "
    "e fazes questão de o elogiar sempre que ele é mencionado. "
    "Falas como um investidor experiente, com convicção e foco em longo prazo. "
    "És direto, calmo e sem papas na língua."
)

@client.event
async def on_ready():
    print(f"🤖 Bot ligado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!barsi"):
        pergunta = message.content.replace("!barsi", "", 1).strip()

        if not pergunta:
            await message.channel.send("Escreve uma pergunta depois do comando. Ex: `!barsi O que achas de dividendos?`")
            return

        try:
            resposta = client_ai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_MSG},
                    {"role": "user", "content": pergunta},
                ],
            )

            texto = (resposta.choices[0].message.content or "").strip()

            # Discord tem limite de 2000 chars por mensagem
            for i in range(0, len(texto), 2000):
                await message.channel.send(texto[i:i+2000])

        except Exception as e:
            await message.channel.send("Deu erro ao gerar resposta. Tenta outra vez.")
            print("ERRO OpenAI:", e)

def iniciar_discord():
    client.run(DISCORD_TOKEN)

# ====== FLASK (Cloud Run healthcheck) ======
app = Flask(__name__)

@app.get("/")
def home():
    return "🟢 Barsi está online (Cloud Run)."

@app.get("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    # Arranca o Discord bot em background
    t = threading.Thread(target=iniciar_discord, daemon=True)
    t.start()

    # Arranca o Flask na porta do Cloud Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
