import asyncio
import aiohttp
from discord import User
from .exceptions import *


class Client:

    def __init__(self, bot, key):
        self.bot = bot
        self.key = token
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

        if kwargs.get("bandwidth"):
            if isinstance(kwargs["bandwidth"],bool):
                self.bandwidth=kwargs["bandwidth"]
            else:
                raise TypeError("Bandwidth config : expected type bool")
        else:
            self.bandwidth = True

        if kwargs.get("debug"):
            if isinstance(kwargs["debug"],bool):
                self.debug=kwargs["debug"]
            else:
                raise TypeError("Debug config : expected type bool")
        else:
            self.debug = False

        self.active = []
        self.commands = 0
        self.popular = []
        self.previous_bandwidth = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        psutil.cpu_percent()

        if self.debug:
            print("Statcord debug mode enabled")

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
        else:
            cpuload = "0"

        if self.bandwidth:
            current_bandwidth = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            bandwidth = str(current_bandwidth-self.previous_bandwidth)
            self.previous_bandwidth = current_bandwidth
        else:
            bandwidth = "0"

        if self.custom1:
            custom1 = str(await self.custom1())
        else:
            custom1 = "0"

        if self.custom2:
            custom2 = str(await self.custom2())
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
            "bandwidth":bandwidth,
            "custom1":custom1,
            "custom2":custom2,
        }
        if self.debug:
            print("Posting data")
            print(data)
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
        for j in range(len(self.popular)):
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
        print("Statcord Auto Post has started!")
        while not self.bot.is_closed():
            await self.post_data()
            await asyncio.sleep(60)
