import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "!", description = "Bot numéro 1")
@bot.event
async def on_ready():
    print("Your Bot is ready!")

@bot.event
async def on_message(message):

    mess = message.content
    if mess == "!Ping":
        await message.channel.send("Pong !")
    if mess == "!Bonjour":
        await message.channel.send("Bonjour !!!")     

bot.run("ODA4NjQ5MTU5OTI1OTU2NjI5.YCJnNw.F2YKC2ubeazi-FUClgK5H7OA9o0")  