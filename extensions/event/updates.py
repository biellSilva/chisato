import discord

from discord import app_commands
from discord.ext import commands
from datetime import datetime


class UpdatesAlertsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer_glob = 0
        self.timer_cn = 0

    @commands.Cog.listener(name='on_message')
    async def updates_alert(self, message: discord.Message):

        if message.author.id in (1119694027688787999, 1093576369281179768, 1093576407268995072, 1093576439300894801):
                                    # leaks global      # social media      # game announcement     # tof codes
            # global ping

            if message.author.id == 1119694027688787999:
                if self.timer_glob < datetime.now().timestamp():
                    await message.reply(content='<@&1093579221756026990>')
                    self.timer_glob = int(datetime.now().timestamp() + 60*60*15)
            else:
                await message.reply(content='<@&1093579221756026990>')
            
        
        if message.author.id in (1119694952000147618, 1119694073675120770) and '@' in message.content:
                                    # leak cn               # cn announcement
            
            # cn ping
            if message.author.id == 1119694952000147618:
                if self.timer_cn < datetime.now().timestamp():
                    await message.reply(content='<@&1093579258573623379>')
                    self.timer_cn = int(datetime.now().timestamp() + 60*60*15)
            else:
                await message.reply(content='<@&1093579258573623379>')


async def setup(bot: commands.Bot):
    await bot.add_cog(UpdatesAlertsCog(bot))