import discord
from discord.ext import commands, tasks
import configparser

config = configparser.ConfigParser()
token = config['KEYS']['token']

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=['gp '], intents=intents)

initial_extensions = []


@bot.event
async def on_ready():
    print('Guinea Pig in online!')
    print(f"Guinea Pig is active in {len(bot.guilds)} servers!")


@bot.event
async def on_message(message):
    pass

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(token)
