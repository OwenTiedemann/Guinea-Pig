from discord.ext import commands


class BotManagement(commands.Cog, name="Bot Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Loads specified cog")
    @commands.is_owner()
    async def load(self, ctx, bot_extension):
        self.bot.load_extension(f'cogs.{bot_extension}')
        await ctx.send(f"Loaded the {bot_extension} cog")

    @commands.command(brief="Unloads specified cog")
    @commands.is_owner()
    async def unload(self, ctx, bot_extension):
        self.bot.unload_extension(f'cogs.{bot_extension}')
        await ctx.send(f"Unloaded the {bot_extension} cog")

    @commands.command(brief="Reloads specified cog")
    @commands.is_owner()
    async def reload(self, ctx, bot_extension):
        self.bot.unload_extension(f'cogs.{bot_extension}')
        self.bot.load_extension(f'cogs.{bot_extension}')
        await ctx.send(f"Reloaded the {bot_extension} cog")


def setup(bot):
    bot.add_cog(BotManagement(bot))