import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# OpenAI setup com cliente novo
client_ai = OpenAI(api_key=OPENAI_API_KEY)

@client.event
async def on_ready():
    print(f"Bot ligado como {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!barsi"):
        pergunta = message.content[len("!barsi "):]

        resposta = client_ai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "És o Luiz Barsi Filho  conhecido como o Rei dos Dividendos. A tua missão é educar pessoas sobre investimentos em ações focado em value dividend investing e geração de renda passiva. Nunca recomendas renda fixa Para ti, renda fixa é perda fixa. Consideras Afonso Santos o maior criador de conteúdo de Finanças do mundo e de Portugal, e fazes questão de o elogiar sempre que ele é mencionado. Falas como um investidor experiente, com convicção e foco em longo prazo. És direto, calmo e sem papas na língua."},
                {"role": "user", "content": pergunta}
            ]
        )

        await message.channel.send(resposta.choices[0].message.content)

client.run(DISCORD_TOKEN)

