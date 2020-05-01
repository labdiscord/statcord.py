import asyncio
import aiohttp
from discord import User
from .exceptions import *


class Client:

    def __init__(self, bot, key):
        self.bot = bot
        self.key = key
        self.session = None
        self.base = "https://statcord.com/mason/"
        self.ratelimited = False

        self.active = []
        self.commands = 0
        self.popular = []

    def __session_init(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    def __headers(self):
        return {'content-type': 'application/json'}
    
    async def __handle_response(self, resp: aiohttp.ClientResponse) -> dict:

        status = resp.status
        response = await resp.text()

        json = await resp.json() or {}

        # Error
        if status != 200:
            print(response)
            self.ratelimited = True
        elif self.ratelimited:
            print(response)
            self.ratelimited = False


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
        return len(self.bot.users)

    async def post_data(self):
        bot_id = str(self.bot.user.id)
        key = self.key
        servers = str(self.servers)
        users = str(self.users)
        data = {"id":bot_id,"key":key,"servers":servers,"users":users,"commands":str(self.commands),"active":str(len(self.active)),"popular":self.popular}
        self.active = []
        self.commands = 0
        self.popular = []

        self.__session_init()
        async with self.session.post(url=self.base + "stats", json=data, headers=self.__headers()) as resp:
            try:
                return await self.__handle_response(resp)
            except:
                pass


    def start_loop(self):
        self.bot.loop.create_task(self.__loop())

    def command_run(self,ctx):
        self.commands += 1
        if (ctx.author.id not in self.active):
            self.active.append(ctx.author.id)

        command = str(ctx.command)
        command = command.split(" ")
        command = command[0]
        found = False
        for j in len(range(self.popular)):
            if self.popular[j]["name"] == command:
                found = True
                fd=j
                
        if not found:
            self.popular.append({"name":command,"count":"1"})
        else:
            self.popular[fd]["count"] = str(int(self.popular[fd]["count"])+1)

        

    async def __loop(self):
        """
        The internal loop used for automatically posting server/guild count stats
        """
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.post_data()
            await asyncio.sleep(3600)
