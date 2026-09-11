import discord
from discord.ext import commands
from google import genai

# Cargar modelo preentrenado
ai_client = genai.Client(api_key="-")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"¡Bot Ecologista conectado como: {bot.user.name}!")

@bot.command()
async def eco(ctx, *, pregunta: str = None):
    """Responde consultas sobre el cuidado del medio ambiente y reciclaje."""
    if pregunta is None:
        await ctx.send(" Por favor escribe una duda ecológica. Ejemplo: `!eco ¿Cómo separar las basuras?`")
        return


    mensaje_espera = await ctx.send("Pensando respuesta...")

    try:
        # Llamada corregida especificando model= y contents=
        response = ai_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=pregunta,
            config={
                "system_instruction": (
                    "Eres un experto educador en ciencias ambientales, desarrollo sostenible y ecología. "
                    "Tu objetivo es responder de forma clara, motivadora y práctica a preguntas sobre cómo cuidar el planeta."
                )
            }
        )

        # Extraemos el texto dentro del bloque try
        respuesta_ia = response.text
        
    except Exception as error:
        await mensaje_espera.edit(content=f" Ocurrió un error al consultar la IA: {error}")
TOKEN = "-"

if __name__ == "__main__":
    bot.run(TOKEN)