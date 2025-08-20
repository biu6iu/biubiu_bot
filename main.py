import discord
import os
from dotenv import load_dotenv
from league_api import get_recent_matches


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
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

    # Recent matches feature: $recent {user_name} {n}
    elif message.content.startswith('$recent'):
        parts = message.content.split()
        
        if len(parts) < 2 or len(parts) > 3:
            await message.channel.send("❌ Usage: `$recent <summoner_name> [number_of_matches (1-5)]`\nExample: `$recent biubiu 3`")
            return
        
        summoner_name = parts[1]
        count = 1  # Default to 1 match
        
        if len(parts) == 3:
            try:
                count = int(parts[2])
                # Cap count at 5 
                if count < 1 or count > 5:
                    await message.channel.send("❌ Invalid number of matches. Usage: `$recent <summoner_name> [number_of_matches (1-5)]`\nExample: `$recent biubiu 3`")
                    return
            # If the number is not an integer, return an error
            except ValueError:
                await message.channel.send("❌ Invalid number value. Usage: `$recent <summoner_name> [number_of_matches (1-5)]`\nExample: `$recent biubiu 3`")
                return
        
        await message.channel.typing()
        
        # Get recent matches
        result = await get_recent_matches(summoner_name, count)
        await message.channel.send(result)
    
    elif message.content.startswith('$help'):
        help_text = """
**Available Commands:**
`$hello` - Say hello
`$biubiu` - Activate the bot
`$recent <name> [n]` - Get recent League matches (1-5) 
`$help` - Show this message
        """
        await message.channel.send(help_text)

client.run(os.getenv('TOKEN'))