import discord
import os
import dotenv

from discord.ext import commands

from extensions import config


class Dumbot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix='c!', intents=intents, case_insensitive=True, strip_after_prefix=True)


    async def setup_hook(self):
        self.task = self.loop.create_task(self.ch_pr())

        for folder in os.listdir('./extensions'):
            if not folder.endswith('.py') and not folder == 'views':
                for filename in os.listdir(f'./extensions/{folder}'):
                    if filename.endswith('.py'):
                        await self.load_extension(f'extensions.{folder}.{filename[:-3]}')
                        print(f'{folder}.{filename[:-3]} loaded')

    async def on_ready(self):
        print(f'''
    {"-"*20}
        {bot.user}
        {bot.status} - {round(bot.latency * 1000)}ms
    {"-"*20}
        ''')

    async def ch_pr(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f'c!help ou /help'))


bot = Dumbot(intents=discord.Intents.all())


chisato = dotenv.get_key(dotenv_path=dotenv.find_dotenv(), key_to_get='chisato')

bot.run(token=chisato)
