import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = "!", description = "Bot numéro 1")

@bot.event
async def on_ready():
    print("Your Bot is ready!")

@bot.event
async def on_message(message):
    mess = message.content
    mess = mess.lower() 
    if mess == "!ping":
        await message.channel.send("Pong !")
    if mess == "!bonjour":
        await message.channel.send("Bonjour **%s** :smiley:" % message.author)
    if mess == "!shutdown":
        await message.channel.send("@everyone Bye bye !")
        await bot.logout()   

bot.run("ODA4NjQ5MTU5OTI1OTU2NjI5.YCJnNw.F2YKC2ubeazi-FUClgK5H7OA9o0")  