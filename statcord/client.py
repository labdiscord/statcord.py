import asyncio
import aiohttp
import psutil
from discord import Client as DiscordClient
from . import exceptions


class Client:
    """Client for using the statcord API"""
    def __init__(self, bot, key, **kwargs):
        if not isinstance(bot,DiscordClient):
            raise TypeError("Expected class deriving from discord.Client for arg bot")
        if not isinstance(bot,str):
            raise TypeError("Expected str for arg bot")

        self.bot = bot
        self.key = key
        self.base = "https://beta.statcord.com/logan/"
        self.session = aiohttp.ClientSession(loop=bot.loop)

        if kwargs.get("mem"):
            if isinstance(kwargs["mem"],bool):
                self.mem=kwargs["mem"]
            else:
                raise TypeError("Memory config : expected type bool")
        else:
            self.mem=True

        if kwargs.get("cpu"):
            if isinstance(kwargs["cpu"],bool):
                self.cpu=kwargs["cpu"]
            else:
                raise TypeError("CPU config : expected type bool")
        else:
            self.cpu = True

        if kwargs.get("debug"):
            if isinstance(kwargs["debug"],bool):
                self.cpu=kwargs["debug"]
            else:
                raise TypeError(f"CPU config : expected type bool, not {kwargs['debug'].__type__()}")
        else:
            self.debug = False

        self.custom1 = kwargs.get("custom1") or False
        self.custom2 = kwargs.get("custom2") or False
        self.active = []
        self.commands = 0
        self.popular = []
        psutil.cpu_percent()

        if self.debug:
            print("Debug Mode Enabled")

    def __headers(self):
        return {'Content-Type': 'application/json'}

    async def __handle_response(self, res: aiohttp.ClientResponse) -> dict:
        json = await res.json() or {}
        status = res.status
        if status == 200:
            return json
        elif status == 429:
            return json # Skip post until next time. (60s isnt much)
        else:
            raise exceptions.RequestFailure(status=status,response=json)

        return json

    @property
    def servers(self):
        return str(len(self.bot.guilds))

    @property
    def users(self):
        return str(len(self.bot.users))

    async def post_data(self):
        id = str(self.bot.user.id)
        commands = str(self.commands)

        if self.mem:
            mem = psutil.virtual_memory()
            memactive = str(mem.used)
            memload = str(mem.percent)
        else:
            memactive = "0"
            memload = "0"

        if self.cpu:
            cpuload = str(psutil.cpu_percent())
            cputemp = "-1"
        else:
             cpuload = "0"
            cputemp = "0"

        if self.custom1:
            custom1 = str(await self.custom1())
        else:
            custom1 = "0"

        if self.custom2:
            custom2 = str(await self.custom1())
        else:
            custom2 = "0"

        data = {
            "id":id,
            "key":self.key,
            "servers":self.servers,
            "users":self.users,
            "commands":commands,
            "active":self.active,
            "popular":self.popular,
            "memactive":memactive,
            "memload":memload,
            "cpuload":cpuload,
            "cputemp":cputemp,
            "custom1":custom1,
            "custom2":custom2,
        }
        if self.debug:
            print(data)
        self.active = []
        self.commands = 0
        self.popular = []

        async with self.session.post(url=self.base + "stats", json=data, headers=self.__headers()) as resp:
            return await self.__handle_response(resp)

    def start_loop(self):
        self.bot.loop.create_task(self.__loop())

    def command_run(self,ctx):
        self.commands += 1
        if ctx.author.id not in self.active:
            self.active.append(ctx.author.id)

        command = ctx.command.name
        found = False
        popular = list(self.popular)
        self.popular= []
        for cmd in popular:
            if cmd["name"] == command:
                found = True
                cmd["count"] = str(int(cmd["count"]) + 1)
            self.popular.append(cmd)

        if not found:
            self.popular.append({"name":command,"count":"1"})

    async def __loop(self):
        """
        The internal loop used for automatically posting server/guild count stats
        """
        await self.bot.wait_until_ready()
        print("Statcord Auto Post has started!")
        while not self.bot.is_closed():
            await self.post_data()
            await asyncio.sleep(60)
