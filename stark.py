import discord
from discord.ext import commands
import datetime
import os
from nltk.chat.util import Chat, reflections
from pairs import pairs
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix = "!", description = "Bot numéro 1")
date = datetime.datetime.now()

class Stark(discord.Client, Chat):

    def __init__(self, pairs, reflections):
        discord.Client.__init__(self)
        Chat.__init__(self, pairs, reflections)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        mess = message.content
        mess = mess.lower() 
        if message.author == self.user:
            return
        if mess == "!ping":
            await message.channel.send("Pong !")
        if mess == "!date":
            await message.channel.send("**%s**" % date)
        if mess == "!bonjour":
            await message.channel.send("Bonjour **%s** :smiley:" % message.author)
        if mess == "!shutdown":
            await message.channel.send("Bye bye !")
            await bot.logout()
        else:
            resp = self.respond(mess)
            if resp!=None:
                await message.channel.send(resp)
            else:
                await message.channel.send("repeat please, I don't anderstand")

client = Stark(pairs, reflections)
#client.run(os.getenv("TOKEN"))  
client.run('ODA4NjQ5MTU5OTI1OTU2NjI5.YCJnNw.F2YKC2ubeazi-FUClgK5H7OA9o0')