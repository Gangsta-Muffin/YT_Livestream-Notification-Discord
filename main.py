from nextcord.ext import commands, tasks
import nextcord as ncrd
import json
import os
import threading


bot = commands.Bot(command_prefix="--")


@bot.event
async def on_ready():
    print("Bot is up!")


for file in os.listdir("./extensions"):
    if file.endswith(".py"):
        print(file)
        bot.load_extension(f"extensions.{file[:-3]}")
 



bot.run("YOUR BOT TOKEN HERE")
