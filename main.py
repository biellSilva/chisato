import discord
import os
import dotenv

from discord.ext import commands


class Dumbot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix='c!', intents=intents,
                         help_command=None, case_insensitive=True, strip_after_prefix=True)
        self.initial_extensions = []

    async def setup_hook(self):
        self.task = self.loop.create_task(self.ch_pr())

        for folder in os.listdir('./extensions'):

            if not folder.endswith('.py') and not folder == 'views':
                for filename in os.listdir(f'./extensions/{folder}'):
                    if filename.endswith('.py'):
                        await self.load_extension(f'extensions.{folder}.{filename[:-3]}')
                        self.initial_extensions.append(filename[:-3])

        print(self.initial_extensions)

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

env_path = dotenv.find_dotenv()
chisato = dotenv.get_key(dotenv_path=env_path, key_to_get='chisato')

bot.run(token=chisato)
