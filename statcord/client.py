import asyncio
from discord import User
import aiohttp
from .exceptions import *


class Client:

    def __init__(self, bot, key):
        self.bot = bot
        self.key = key
        self.session = None
        self.base = "https://statcord.com/apollo/"

    def __session_init(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    def __headers(self):
        return {'content-type': 'application/json'}
    
    async def __handle_response(self, resp: aiohttp.ClientResponse) -> dict:

        status = resp.status
        response = await resp.text()

        try:
            json = await resp.json()
        except:
            json = {}

        # Error
        if status != 200:
            print(response)

        return json

    @property
    def servers(self):
        try:
            count = len(self.bot.guilds)
        except AttributeError:
            count = len(self.bot.servers)

        return count

    @property
    def users(self):
        count = len(self.bot.users)
        return count

    async def post_data(self):
        bot_id = str(self.bot.user.id)
        key = self.key
        servers = str(self.servers)
        users = str(self.users)
        data = {"id":bot_id,"key":key,"servers":servers,"users":users}
        self.__session_init()
        async with self.session.post(url=self.base + "post/stats", json=data, headers=self.__headers()) as resp:
            return await self.__handle_response(resp)


    def start_loop(self):
        self.bot.loop.create_task(self.__loop())

    async def __loop(self):
        """
        The internal loop used for automatically posting server/guild count stats
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.post_data()
            await asyncio.sleep(1800)
