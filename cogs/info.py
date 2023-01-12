import time
import discord
import psutil
import os

from discord.ext.commands.context import Context
from discord.ext.commands._types import BotT
from discord.ext import commands
from utils import default, http


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        self.config = default.load_json()
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self, ctx: Context[BotT]):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=["joinme", "join", "botinvite"])
    async def invite(self, ctx: Context[BotT]):
        """ Invite me to your server """
        await ctx.send("\n".join([
            f"**{ctx.author.name}**, use this URL to invite me",
            f"<{discord.utils.oauth_url(self.bot.user.id)}>"
        ]))

    @commands.command()
    async def source(self, ctx: Context[BotT]):
        
        await ctx.send("\n".join([
            f"**{ctx.bot.user}** is powered by BlackSource LLC:",
            ""
        ]))

    @commands.command(aliases=["supportserver", "feedbackserver"])
    async def blacksource(self, ctx: Context[BotT]):
        """ Get an invite to our support server! """
        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 1060414130420449391:
            return await ctx.send(f"**Here's the link.. {ctx.author.name} **\nhttps://discord.gg/PvtC5PZQqR")
        await ctx.send(f"**{ctx.author.name}** Thanks for joining.")

    @commands.command()
    async def blackanime(self, ctx: Context[BotT]):
        """ Get a link for BlackAnimev3 """
        await ctx.send(f"**Here's the link..{ctx.author.name}**\nhttps://blackanime3.vercel.app \nThank you for choosing BlackAnime")

    
    @commands.command()
    async def blackanime(self, ctx: Context[BotT]):
        """ Get a link for Manga Red """
        await ctx.send(f"**Here's the link..{ctx.author.name}**\nhttps://manga-red.vercel.app \nThank you for choosing Manga Red")


    @commands.command()
    async def mangared(self, ctx: Context[BotT]):
        """ Get a link for BlackAnimev3 """
        await ctx.send(f"**Here's the link..{ctx.author.name}**\nhttps://blackanime3.vercel.app \nThank you for choosing BlackAnime")

    
    @commands.command()
    async def blackstream(self, ctx: Context[BotT]):
        """ Get a link for Stream """
        await ctx.send(f"**Here's the link..{ctx.author.name}**\nhttps://blackstream.netlify.app/ \nThank you for choosing BlackStream")


    @commands.command()
    async def covid(self, ctx: Context[BotT], *, country: str):
        """Covid-19 Statistics for any countries"""
        async with ctx.channel.typing():
            r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

            if "message" in r:
                return await ctx.send(f"The API returned an error:\n{r['message']}")

            json_data = [
                ("Total Cases", r["cases"]), ("Total Deaths", r["deaths"]),
                ("Total Recover", r["recovered"]), ("Total Active Cases", r["active"]),
                ("Total Critical Condition", r["critical"]), ("New Cases Today", r["todayCases"]),
                ("New Deaths Today", r["todayDeaths"]), ("New Recovery Today", r["todayRecovered"])
            ]

            embed = discord.Embed(
                description=f"The information provided was last updated <t:{int(r['updated'] / 1000)}:R>"
            )

            for name, value in json_data:
                embed.add_field(
                    name=name, value=f"{value:,}" if isinstance(value, int) else value
                )

            await ctx.send(
                f"**COVID-19** statistics in :flag_{r['countryInfo']['iso2'].lower()}: "
                f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
                embed=embed
            )

    @commands.command(aliases=["info", "stats", "status"])
    async def about(self, ctx: Context[BotT]):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = None
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.add_field(name="Last boot", value=default.date(self.bot.uptime, ago=True))
        embed.add_field(
            name=f"Developer{'' if len(self.config['owners']) == 1 else 's'}",
            value="BlackSource LLC ".join([str(self.bot.get_user(x)) for x in self.config["owners"]])
        )
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )")
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)


async def setup(bot):
    await bot.add_cog(Information(bot))
