import configparser

import discord
import motor.motor_asyncio
from discord.ext import commands

config = configparser.ConfigParser()
config.read('config.ini')
token = config['KEYS']['discord_token']
mongo_token = config['KEYS']['mongo_token']

database_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_token)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=['gp '], intents=intents)

initial_extensions = ['cogs.work', 'jishaku']

database = database_client['Leveling']
bot.users_collection = database['Users']

bot.levels = {
    0: 0,
    1: 1,
    2: 10,
    3: 100,
    4: 250,
    5: 750,
    6: 1500,
    7: 3000,
    8: 5000,
    9: 7500,
    10: 10000,
}


@bot.event
async def on_ready():
    print('Guinea Pig in online!')
    print(f"Guinea Pig is active in {len(bot.guilds)} servers!")


@bot.event
async def on_member_join(member):
    if await bot.users_collection.count_documents({"_id": str(member.id)}, limit=1) == 0:
        user_dict = {"_id": str(member.id), "level": 0, "experience": 0, "total_messages": 0}
        await bot.users_collection.insert_one(user_dict)


def update_level(current_level, current_experience):
    experience = current_experience + 1
    if experience == bot.levels[current_level + 1]:
        experience = 0
        level = current_level + 1
        print("Someone leveled up!")
        return level, experience
    else:
        return current_level, experience


@bot.event
async def on_message(message):
    if not message.author.bot:
        if await bot.users_collection.count_documents({"_id": str(message.author.id)}, limit=1) == 0:
            user_dict = {"_id": str(message.author.id), "level": 0, "experience": 0, "total_messages": 0}
            await bot.users_collection.insert_one(user_dict)

        print(message.author.id)
        user = await bot.users_collection.find_one({"_id": str(message.author.id)})
        print(user)
        level, experience = update_level(user['level'], user['experience'])
        await bot.users_collection.update_one({"_id": user["_id"]},
                                              {"$set":
                                                  {
                                                      "level": level,
                                                      "experience": experience,
                                                      "total_messages": user['total_messages'] + 1
                                                  }
                                              })

    await bot.process_commands(message)


if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(token)
