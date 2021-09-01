from discord.ext import commands, tasks


class Work(commands.Cog, name="Work"):
    def __init__(self, bot):
        self.bot = bot

    async def update_level(self, current_level, current_experience, gained_experience):
        experience = current_experience + gained_experience
        if experience >= self.bot.levels[current_level + 1]:
            experience = 0
            level = current_level + 1
            print("Someone leveled up!")
            return level, experience
        else:
            return current_level, experience

    @commands.command(name="mine",
                      brief="Gain experience by mining")  # , description="Use your pickaxe to mine experience, buy better pickaxes for better rates")
    async def mine(self, ctx):
        user = await self.bot.users_collection.find_one({"_id": str(ctx.author.id)})
        print(user)
        if 'pickaxe' in user:
            pickaxe = user['pickaxe']
        else:
            pickaxe = 1

        experience_mined = 10 / user['level'] * pickaxe

        level, experience = await self.update_level(user['level'], user['experience'], experience_mined)
        await self.bot.users_collection.update_one({"_id": user["_id"]},
                                                   {"$set":
                                                       {
                                                           "level": level,
                                                           "experience": experience,
                                                           "pickaxe": pickaxe
                                                       }
                                                   })


def setup(bot):
    bot.add_cog(Work(bot))
