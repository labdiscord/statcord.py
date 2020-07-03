import asyncio
import aiohttp
from discord import User
import psutil

class Client:

    def __init__(self, bot, key, **data):
        self.bot = bot
        self.key = key
        self.session = None
        self.base = "https://beta.statcord.com/logan/"
        self.ratelimited = False

        self.mem = True
        self.cpu = True

        self.custom1 = None
        self.custom2 = None

        try:
            if (isinstance(data["mem"],bool)):
                self.mem = data["mem"]
            else:
                print("Memory config must be a Boolean.")
        except:
            self.mem = True

        try:
            if (isinstance(data["cpu"],bool)):
                self.cpu = data["cpu"]
            else:
                print("CPU config must be a Boolean.")
        except:
            self.cpu = True

        try:
            self.custom1 = data["custom1"]
            if(not isinstance(self.custom1(),str)):
                self.custom1 = None
                print("The Custom 1 config function must return a String.")
        except:
            self.custom1 = None

        try:
            self.custom2 = data["custom2"]
            if(not isinstance(self.custom2(),str)):
                self.custom2 = None
                print("The Custom 2 config function must return a String.")
        except:
            self.custom2 = None

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
        
        memactive = "0"
        memload = "0"
        cpuload = "0"
        cputemp = "0"
        custom1 = "0"
        custom2 = "0"

        if self.mem:
            mem = psutil.virtual_memory()
            memactive = str(mem.used)
            memload = str(mem.percent)

        if self.cpu:
            cpuload = str(psutil.cpu_percent(interval=1))
            cputemp = "-1"

        if self.custom1:
            custom1 = await self.custom1()
        
        if self.custom2:
            custom2 = await self.custom2()

        data = {"id":bot_id,"key":key,"servers":servers,"users":users,"commands":str(self.commands),"active":self.active,"popular":self.popular,"memactive":memactive,"memload":memload,"cpuload":cpuload,"cputemp":cputemp,"custom1":custom1,"custom2":custom2}
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
