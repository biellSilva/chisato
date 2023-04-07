from discord import app_commands
from discord.ext import commands


class ColorsCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def colors(self, ctx: commands.Context, name: str, hex: str):
        '''Create role with hex color'''

        if not ctx.author.guild_permissions.kick_members:
            await ctx.reply('Missing permission')
            return

        role = await ctx.guild.create_role(name=name, colour=int(hex.replace('#', ''), 16))
        
        await ctx.guild.edit_role_positions({role: len(ctx.guild.roles)-7})

        await ctx.send(role.mention)

async def setup(bot):
    await bot.add_cog(ColorsCommand(bot))
