<h1 align="center" id="statcordpy">
    statcord.py
</h1>

<h3 align="center">A simple API wrapper for statcord.com  to connect your bot and get your bot stats.</h3>



----

<!-- Content -->
## Installation

Install via pip (recommended)

```Shell
python3 -m pip install statcord.py
```

## Features

* AUTOMATIC server & user count updating.

## Example Discord.py Cogs

### Posting Server & User Count

```Python
from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key = "statcord.com-ADDYOURKEYHERE"
        self.api = statcord.Client(self.bot,self.key)
        self.api.start_loop()



def setup(bot):
    bot.add_cog(StatcordPost(bot))

```

## Contributing

Contributions are always welcome!\
Take a look at any existing issues on this repository for starting places to help contribute towards, or simply create your own new contribution to the project.

When you are ready, simply create a pull request for your contribution and we will review it whenever we can!

### Donating

You can also help me and the project out by sponsoring me through a [donation on PayPal](http://paypal.me/deltafloof).


## Discussion, Support and Issues

Need support with this project, have found an issue or want to chat with others about contributing to the project?
> Please check the project's issues page first for support & bugs!

Not found what you need here?

* If you have an issue, please create a GitHub issue here to report it, include as much detail as you can.
* _Alternatively,_ You can join our Discord server to discuss any issue or to get support for the project.:

<a href="http://statcord.com/discord" target="_blank">
    <img src="https://discordapp.com/api/guilds/608711879858192479/embed.png" alt="Discord" height="30">
</a>
