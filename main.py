import discord
import os
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Enable message content reading
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Basic commands
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello {message.author.mention}! 👋')
    
    elif message.content.startswith('$biubiu'):
        await message.channel.send('biubiu bot activated! 🎯')
    
    elif message.content.startswith('$help'):
        help_text = """
**Available Commands:**
`$hello` - Say hello
`$biubiu` - Activate the bot
`$help` - Show this message
        """
        await message.channel.send(help_text)

client.run(os.getenv('TOKEN'))