from redbot.core import commands
from redbot.core import Config
import asyncio
import discord
import random
from redbot.core.utils.chat_formatting import pagify
import json
from PIL import Image
from redbot.core.data_manager import bundled_data_path
from redbot.core.data_manager import cog_data_path 



class RPGBotCore(commands.Cog):

	def __init__(self, bot):
		self.config = Config.get_conf(self, identifier=10320)		
		character_data = {
		##basic info
			"name": "",
			"race": "", 
			"gender": "",
			"age": "",
			"world": "",
			"class": "",
			"desc": "",
			"avatar": "https://cdn.discordapp.com/attachments/514979120527179776/528816068601577474/boticon.png",
		##stats
			"maxHP": 0,
			"curHP": 0,
			"level": 1,
			"xp_to_lv": 0,
			"curXP": 0,
			"core_points": 0,
		##core stats + mods
			"stats": {
				"strength": 0,
				"STRmod": 0,
				"dexterity": 0,
				"DEXmod": 0,
				"intellect": 0,
				"INTmod": 0,
				"wisdom": 0,
				"WISmod": 0,
				"charisma": 0,
				"CHAmod": 0,
				"vitality": 0,
				"VITmod": 0,
				"has_stats": False
			},
		##combat stuff
			"max_dmg": 4,
			"weapon_skills": {
				"skill1": "None",
				"skill2": "Unlocks at Level 20",
				},
			"in_combat": False,
		##inventory
			"inventory": {
				"weapon1": "None",
				"weapon1_type": "None",
				"weapon2": "Unlocks at Level 20",
				"weapon2_type": "Unlocks at level 20",
				"items": {
					"Nexus Crystal": "Can be used out of combat to return to the Nexus.",
					"Health Potion Lv1(5)": "Restores 15% health."
					},
				"quest_items": {

					},
			},		
		#actionable abilities			
			"abilities": {
				"slot1": {
					"name": "None",
					"desc": "None",
					"math": "None"
					},
				"slot2": {
					"name": "Unlocks at level 5.",
					"desc": "None",
					"math": "None"
					},
				"slot3": {
					"name": "Unlocks at level 10.",
					"desc": "None",
					"math": "None"
					},
				"slot4": {
					"name": "Unlocks at level 20",
					"desc": "None",
					"math": "None"
					},
				"slot5": {
					"name": "Unlocks at level 30",
					"desc": "None",
					"math": "None"
					},																						
			},	
			"has_data": False
			}
				
		
		
		
		self.config.register_guild(**character_data)	
		self.bot = bot
### character editing loop
	async def add_char_info_dict(self, ctx, info_type:tuple, member:discord.Member, name:str):
		def check(message):
		    return message.author == ctx.message.author
		if info_type[0] == "desc":
			x = None
			h = 2
		else:
			x = 60
			h = 1 
		i = 0
		while i == 0:
		    purge_mark = await ctx.send("Please input your character's {}.".format(info_type[h]), delete_after=60)
		    try:
		        input_var = await self.bot.wait_for('message', check=check, timeout=x)
		    except asyncio.TimeoutError:
		        await ctx.send("You took too long to respond. Terminating.")
		        
		        return False
		    input_var = input_var.content
		    if input_var.lower() == "cancel":
		        await ctx.send("Cancelling Character Creation.")
		        
		        await self.config.member(member).clear_raw()
		        return False
		    else:
		        await ctx.send("Is {} correct? Respond with yes or no.".format(input_var), delete_after=60)
		        ii = 0
		        while ii == 0:
		            try:
		                msg = await self.bot.wait_for('message', check=check, timeout=x)
		            except asyncio.TimeoutError:
		                await ctx.send("You took too long to respond. Terminating")
		                
		                return False
		            y = msg.content.lower()
		            if y == "yes":
		                await self.config.member(member).set_raw(name, info_type[0], value=input_var)
		                i = 1
		                ii = 1
		            elif y == "no":
		                
		                return await self.add_char_info_dict(ctx, info_type, member, name)
		            elif y == "cancel":
		                await ctx.send("Cancelling Character Creation.")
		                
		                await self.config.member(member).clear_raw()
		                return False
		            else:
		                await ctx.send("Please enter yes or no.")
		    await ctx.send("Character {} has been set to {}".format(info_type[1], input_var))
		    
		    await asyncio.sleep(1)
		    return True
### character command group
	@commands.group(name="character", aliases=("char", "c"), autohelp=True)
	async def character(self, ctx):
		if ctx.invoked_subcommand is None:
			pass
### new character creation
	@character.command(name="newchar", aliases=("new", "n", "create"))
	async def new_dict_test(self, ctx, name:str):
		"""
		Begins the first time character creation tool.
		Once this tool has been used once, you cannot access it again for the same character.
		"""
		member = ctx.author
		try:
			getinfo = await self.config.member(member).get_raw(name)
			tf = getinfo["has_data"]
			if tf == True:
				await ctx.send("Sorry, you already have data for that character. Please use `{}char edit <name>` to edit that character.".format(ctx.prefix))
		except KeyError:			
			initm = await ctx.send("**__Initializing character builder__.**")
			new_data = await self.config.guild(ctx.guild).get_raw()
			await asyncio.sleep(1)
			await initm.edit(content="**__Initializing character builder__. .**")
			await asyncio.sleep(1)
			await initm.edit(content="**__Initializing character builder__. . .**")
			await self.config.member(member).set_raw(name, value=new_data)
			await asyncio.sleep(1)
			await initm.edit(content="**Type cancel at any time to exit the character builder and reset all responses.**")
			await asyncio.sleep(1)
			purge_mark = ctx.message
			info_list = [("name", "Name"), ("race", "Race"), ("class", "Class/Profession/Occupation"), ("gender", "Gender"), ("age", "Age"), ("world", "World of Origin"), ("desc", "description", "description. Must be under 2000 characters"), ("avatar", "avatar url")]
			for info_type in info_list:
			    is_complete = None
			    await ctx.channel.purge(limit=100, after=purge_mark)
			    is_set = await self.add_char_info_dict(ctx, info_type, member, name)
			    if not is_set:
			        await self.config.member(member).clear()
			        await ctx.send("Incomplete profile build. Data reset.")
			        break
			await self.config.member(member).set_raw(name, "has_data", value=True)
			await asyncio.sleep(1)
			await ctx.channel.purge(limit=100, after=ctx.message)
			await asyncio.sleep(1)
			await ctx.message.delete()
			part_two = await ctx.send("Character Creation complete! Opening Stat editor. . .")
			await asyncio.sleep(3)
			await part_two.delete()
			await self.set_stats(ctx, member, name)
### character editor
	@character.command(name="edit", aliases=("e", "change", "alter"))
	async def edit_char_test(self, ctx, name:str):
		"""
		Allows the player to edit basic information about a character.
		This can only be opened for an existing character. 
		if you would like to create a new character please use >>character new
		"""
		def check(message):
			return message.author == ctx.message.author	
		member = ctx.author
		info_list = [("name", "Name"), ("race", "Race"), ("gender", "Gender"), ("age", "Age"), ("world", "World of Origin"), ("desc", "description", "description. Must be under 2000 characters"), ("avatar", "avatar url.")]
		char_info = await self.config.member(member).get_raw(name)
		charem = discord.Embed(name=char_info["name"], description="Character Sheet")
		charem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		charem.set_thumbnail(url=char_info["avatar"])
		charem.add_field(name="Name", value=char_info["name"], inline=True)
		charem.add_field(name="Race", value=char_info["race"], inline=True)
		charem.add_field(name="Gender", value=char_info["gender"], inline=True)
		charem.add_field(name="Age", value=char_info["age"], inline=True)
		charem.add_field(name="World of Origin", value=char_info["world"], inline=True)
		charem.add_field(name="Description", value=char_info["desc"], inline=False)
		charem.add_field(name="Avatar", value="Displayed to the right.", inline=False)
		sheet = await ctx.send(embed=charem)
		i = 0
		while i == 0:
			await ctx.send("What would you like to edit?")
			reply = await self.bot.wait_for('message', check=check)
			info = reply.content.lower()
			info_type = [
				t for t in info_list if info in t
				][0]
			await self.add_char_info_dict(ctx, info_type, member, name)
			await sheet.delete()
			char_info = await self.config.member(member).get_raw(name)
			charem = discord.Embed(name=char_info["name"], description="Character Sheet")
			charem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			charem.set_thumbnail(url=char_info["avatar"])
			charem.add_field(name="Name", value=char_info["name"], inline=True)
			charem.add_field(name="Race", value=char_info["race"], inline=True)
			charem.add_field(name="Gender", value=char_info["gender"], inline=True)
			charem.add_field(name="Age", value=char_info["age"], inline=True)
			charem.add_field(name="World of Origin", value=char_info["world"], inline=True)
			charem.add_field(name="Description", value=char_info["desc"], inline=False)
			charem.add_field(name="Avatar", value="Displayed to the right.", inline=False)
			sheet = await ctx.send(embed=charem)			
			await ctx.channel.purge(limit=100, after=sheet)
			ii = 0
			while ii == 0:
				await ctx.send("Would you like to edit another trait?")
				reply = await self.bot.wait_for('message', check=check)
				yn = reply.content.lower()
				if yn == "yes":
					i = 0
					ii = 1
				if yn == "no":
					i = 1
					ii = 1
					await ctx.send("Closing editor. . .")
					await asyncio.sleep(5)
					await ctx.channel.purge(limit=100, after=ctx.message)
					await ctx.message.delete()
### character sheet: basic info
	async def character_basic_info(self, ctx, member:discord.Member, name:str):
		char_info = await self.config.member(member).get_raw(name)
		charem = discord.Embed(name=char_info["name"], description="Character Sheet")
		charem.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		charem.set_thumbnail(url=char_info["avatar"])
		charem.add_field(name="Name", value=char_info["name"], inline=True)
		charem.add_field(name="Race", value=char_info["race"], inline=True)
		charem.add_field(name="Gender", value=char_info["gender"], inline=True)
		charem.add_field(name="Age", value=char_info["age"], inline=True)
		charem.add_field(name="World of Origin", value=char_info["world"], inline=True)
		charem.add_field(name="Description", value=char_info["desc"], inline=False)	
		return charem
### character sheet: stats
	async def character_stat_info(self, ctx, member:discord.Member, name:str):
		stat_list = await self.config.member(member).get_raw(name, "stats")
		character = await self.config.member(member).get_raw(name)
		statem = discord.Embed(name=name, description="{}: Level {} {} {}".format(character["name"], character["level"], character["race"], character["class"]))
		statem.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
		statem.set_thumbnail(url=character["avatar"])
		statem.add_field(name="__**Strength**__", value="{}\nMod: {}".format(stat_list["strength"], stat_list["STRmod"]), inline=True)#0
		statem.add_field(name="__**Dexterity**__", value="{}\nMod: {}".format(stat_list["dexterity"], stat_list["DEXmod"]), inline=True)#1
		statem.add_field(name="__**Intellect**__", value="{}\nMod: {}".format(stat_list["intellect"], stat_list["INTmod"]), inline=True)#2
		statem.add_field(name="__**Wisdom**__", value="{}\nMod: {}".format(stat_list["wisdom"], stat_list["WISmod"]), inline=True)#3
		statem.add_field(name="__**Charisma**__", value="{}\nMod: {}".format(stat_list["charisma"], stat_list["CHAmod"]), inline=True)#4
		statem.add_field(name="__**Vitality**__", value="{}\nMod: {}".format(stat_list["vitality"], stat_list["VITmod"]), inline=True)#5
		statem.add_field(name="**__Health__**", value="{}/{}".format(character["curHP"], character["maxHP"]), inline=True)#6
		statem.add_field(name="**__Experience__**", value="{}/{}".format(character["curXP"], character["xp_to_lv"]), inline=True)#7
		statem.add_field(name="\u200B", value="\u200B", inline=True)#8
		statem.add_field(name="**__Core Points__**", value="{}".format(character["core_points"]), inline=True)#9
		return statem
### call a character sheet
	@character.command(name="show", aliases=("s", "display"))
	async def show_me(self, ctx, member:discord.Member):
		"""
		Displays a list of the mentioned user's characters.
		A character name can be input into the channel to pull up information on that character.
		"""	
		def check(message):
			return message.author == ctx.message.author
		member = ctx.message.mentions[0]
		characters = await self.config.member(member).get_raw()
		keys = list(characters.keys())
		prompt = discord.Embed(name="Character Display", description=member.nick)
		prompt.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		prompt.set_thumbnail(url=member.avatar_url)
		prompt.add_field(name="Which character would you like to view?", value=keys, inline=False)
		msg = await ctx.send(embed=prompt)
		reply = await self.bot.wait_for('message', check=check)
		name = reply.content
		prompt.remove_field(0)
		await reply.delete()
		prompt.add_field(name="Fetching Data", value="Please Wait. . .", inline=False)
		await msg.edit(embed=prompt)
		await asyncio.sleep(3)
		charem = await self.character_basic_info(ctx, member, name)
		statem = await self.character_stat_info(ctx, member, name)
		await msg.edit(embed=charem)
		msg2 = await ctx.send(embed=statem)
### stat editor
	@character.group(name="stats",)
	async def character_stats(self, ctx):
		if ctx.invoked_subcommand is None:
			pass
### randomizer module for stat roles
	async def core_stat_roll(self, ctx):
		dice = [random.randint(1, 6) for _ in range(5)]        
		while len(dice) > 3:
			z = min(dice)
			dice.remove(z)        
		val = sum(dice)        
		return val
### function to get core stat values	
	async def get_core_vars(self, ctx, member:discord.Member, name:str):
		core_stats = await self.config.member(member).get_raw(name, "stats")
		return core_stats
### function chained off of >>char new <name> to set up stats. 
### need to remove the gif at the start, its kind of obnoxious	
	#@character_stats.command(name="setup", aliases=("set", "init"))
	async def set_stats(self, ctx, member:discord.Member, name:str):
		member = ctx.author
		def check(message):
			return message.author == ctx.message.author 
		##initilization stuff (mostly just flavor and the likes)
		inite = discord.Embed(name="Stat Editor", description="Loading . . ")
		inite.set_image(url="https://media.giphy.com/media/brncIHfCBUsmI/giphy.gif")
		initm = await ctx.send(embed=inite)
		await asyncio.sleep(6)
		await initm.delete()
		await asyncio.sleep(1)
		await self.get_core_vars(ctx, member, name)
		statem = await self.character_stat_info(ctx, member, name)
		post_stats = await ctx.send(embed=statem)
		await asyncio.sleep(1)
		d6 = self.bot.get_emoji(529502156714409994)
		d6x = self.bot.get_emoji(529504629105623041)
		statem.add_field(name="Rolling 5D6 for each stat. . .", value="{}{}{}{}{}".format(d6, d6, d6, d6, d6), inline=False)#9
		await post_stats.edit(embed=statem)
		await asyncio.sleep(2)
		statem.remove_field(9)
		statem.add_field(name="Dropping the lowest two values for each stat roll. . .", value="{}{}{}{}{}".format(d6, d6, d6, d6x, d6x), inline=False)#9
		await post_stats.edit(embed=statem)
		results = [await self.core_stat_roll(ctx) for _ in range(6)]
		statem.remove_field(9)
		statem.add_field(name="Results:", value=results, inline=False)#9
		await asyncio.sleep(2)
		await post_stats.edit(embed=statem)
		await asyncio.sleep(1)
		
		#list of stats formatted as such: ("stat config name", "stat mod name", "user end stat desc", "user end stat name" )
		info_list = [("strength", "STRmod", "physical ability", "Strength"), ("dexterity", "DEXmod", "agility", "Dexterity"), ("intellect", "INTmod", "reasoning, memory, and magical prowess.", "Intellect"),
		("wisdom", "WISmod", "perception and insight", "Wisdom"), ("charisma", "CHAmod", "strength of character", "Charisma"), ("vitality", "VITmod", "endurance", "Vitality")]
		#stat loop
		for info_type in info_list:
			statem.add_field(name="{}: the measure of your character's {}.".format(info_type[3], info_type[2]), value="Which value would you like to apply to your character's {}?".format(info_type[3]))
			await post_stats.edit(embed=statem)
			reply = await self.bot.wait_for('message', check=check)
			set_stat = int(reply.content)
			mod = (set_stat - 10)//2
			await self.config.member(member).set_raw(name, "stats", info_type[1], value=mod)
			await asyncio.sleep(1) 
			await self.config.member(member).set_raw(name, "stats", info_type[0], value=set_stat)
			await asyncio.sleep(1)
			statem = await self.character_stat_info(ctx, member, name)
			results.remove(set_stat)
			statem.add_field(name="Results:", value=results, inline=False)
			await reply.delete()
			await post_stats.delete()
			post_stats = await ctx.send(embed=statem)
			await asyncio.sleep(1)
		await self.config.member(member).set_raw(name, "stats", "has_stats", value=True)
		statem.remove_field(6)
		statem.add_field(name="Core stats complete!", value="Loading Part Two. . .")
		statem.set_image(url="https://cdn.discordapp.com/attachments/529449468572073987/529536382490902533/QazI.gif")
		await post_stats.edit(embed=statem)
		await asyncio.sleep(2)
		
		#health, XP, core points.
		statem.remove_field(9)
		statem.set_image(url="")
		statem.add_field(name="Health is calculated by the following equation:", value="10 + 1/2(Level) + VITmod. Decimals are rounded down.", inline=False)#9
		statem.add_field(name="XP needed to level is calculated by the following equation:", value="15 x Level.", inline=False)#10
		statem.add_field(name="Core points are used to increase the values of your core stats.", value="One core point will be added every five levels", inline=False)#11
		await post_stats.edit(embed=statem)
		spinner = self.bot.get_emoji(529506267719270420)
		spin = await ctx.send("{}".format(spinner))
		await asyncio.sleep(5)
		await spin.delete()
		character = await self.config.member(member).get_raw(name)
		stats = await self.config.member(member).get_raw(name, "stats")
		level = int(character["level"])
		VITmod = int(stats["VITmod"])
		HP = (10 + (level//2) + VITmod)
		XPL = (15 * level)
		await self.config.member(member).set_raw(name, "maxHP", value=HP)
		await self.config.member(member).set_raw(name, "curHP", value=HP)
		await self.config.member(member).set_raw(name, "xp_to_lv", value=XPL)
		statem = await self.character_stat_info(ctx, member, name)
		await post_stats.edit(embed=statem)

### on_message function to purge tulpa registration messages so the help message stays there
	async def on_message(self, message):
		purge_mark = discord.utils.snowflake_time(521409158348800000)
		channel = discord.utils.get(message.guild.channels, id=521404867957227541)
		if message.channel == channel:
			if message.author.bot:
				return
			else:
				await asyncio.sleep(25)
				await channel.send("Deleting messages. . .")
				await asyncio.sleep(1)
				await channel.purge(limit=100, after=purge_mark)

		



	########################
	###test commands here###

	#displays raw character data list
	@commands.command(name="getrawdat")
	async def get_raw_dat(self, ctx):
		data = await self.config.member(ctx.author).get_raw()
		await ctx.send(data)



	#deletes raw character data
	@commands.command(name="clearraw")
	async def del_raw_data(self, ctx):
		await self.config.member(ctx.author).clear_raw()
		m = await self.config.member(ctx.author).get_raw()
		await ctx.send("Done! {}".format(m))

	@commands.command(name="print")
	async def print_int(self, ctx, num:int):
		x = num
		await ctx.send(x)

	@commands.command(name="getcharstats")
	async def get_stat_info(self, ctx, name:str):
		member = ctx.author
		statem = await self.character_stat_info(ctx, member, name)
		await ctx.send(embed=statem)


