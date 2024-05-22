import time
from datetime import datetime
from typing import Any, Optional

import discord
from discord import app_commands
from discord.ext import commands
from pytz import timezone

from extensions import config
from extensions.utils import check_date_format


class Commands(commands.Cog):
    """Uncategorized Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="avatar")
    @app_commands.describe(
        member="Select a member",
        image="Select between Discord or Guild avatar, default: Guild",
    )
    @app_commands.choices(
        image=[
            app_commands.Choice(name="Guild Avatar", value=0),
            app_commands.Choice(name="Discord Avatar", value=1),
        ]
    )
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: Optional[discord.Member],
        image: Optional[int] = 0,
    ):
        """Member Avatar"""

        member = member or interaction.user
        assert member
        em = discord.Embed(color=config.cinza)

        if image == 0:
            em.set_image(url=member.display_avatar.url)
            em.set_footer(text=member.display_name, icon_url=member.display_avatar.url)
        elif image == 1:
            em.set_image(url=member.avatar.url)
            em.set_footer(
                text=f"{member.name} | {member.global_name}", icon_url=member.avatar.url
            )

        await interaction.response.send_message(embed=em)

    @commands.hybrid_command(
        name="unixtime", aliases=["unix", "ut"], with_app_command=True
    )
    @app_commands.describe(date="dd/mm/yyyy", hour="HH:MM")
    async def unixtime(
        self, ctx: commands.Context[Any], date: Optional[str], hour: Optional[str]
    ):
        """Convert datetime to Discord timestamp"""

        if not date and not hour:
            unixtime = int(time.time())

        elif date and hour:
            unixtime = int(time.mktime(check_date_format(f"{date} {hour}")))

        else:
            unixtime = int(time.mktime(check_date_format(date)))

        em = discord.Embed(
            color=config.cinza,
            title="Discord Timestamps",
            description=f"""
                           \\<t:{unixtime}> - <t:{unixtime}>
                           \\<t:{unixtime}:t> - <t:{unixtime}:t>
                           \\<t:{unixtime}:T> - <t:{unixtime}:T>
                           \\<t:{unixtime}:d> - <t:{unixtime}:d>
                           \\<t:{unixtime}:D> - <t:{unixtime}:D>
                           \\<t:{unixtime}:f> - <t:{unixtime}:f>
                           \\<t:{unixtime}:F> - <t:{unixtime}:F>
                           \\<t:{unixtime}:R> - <t:{unixtime}:R>
                           """,
        )

        await ctx.send(embed=em, ephemeral=True)

    @commands.hybrid_command(name="asura", with_app_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    async def asura_command(self, ctx: commands.Context[Any]):
        """Asura Command"""

        ASURA_ID = 446434441804513338

        assert ctx.guild
        asura = ctx.guild.get_member(ASURA_ID)
        assert asura

        timeout_timer = datetime.fromtimestamp(
            (
                asura.timed_out_until or datetime.now(tz=timezone("UTC"))
                if asura.is_timed_out()
                else datetime.now(tz=timezone("UTC"))
            ).timestamp()
            + 30,
            tz=timezone("UTC"),
        )

        em = discord.Embed(
            color=config.cinza,
            description=f"<@{ASURA_ID}> banido até <t:{int(timeout_timer.timestamp())}:R>.",
        )

        await asura.timeout(timeout_timer)

        await ctx.send(embed=em)


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
