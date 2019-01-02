
from .RPGBotCore import RPGBotCore
def setup(bot):
	n = RPGBotCore(bot)
	
	bot.add_cog(n)
