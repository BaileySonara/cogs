from redbot.core import commands
from redbot.core import Config
import asyncio
import discord
from itertools import islice
import time
import datetime
from datetime import date
from discord import webhook
import random
from redbot.core.utils.chat_formatting import pagify

#bot init and confi variable set up
class magenta_core(commands.Cog):
    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1234)
        default_global = {
            "str": 0,
            "dex": 0,
            "int": 0,
            "wis": 0,
            "con": 0,
            "cha": 0,
            "pregger_threshold": 90,
            "ovualation_start": 9,
            "ovulation_end": 16,
            "ignored_channels":[],
            "stats": {
            },
            "actions": {
            }
        }
        default_member = {
        "aliases": {
            },
        "save_count": 0
        }
        self.config.register_guild(**default_global)
        self.config.register_member(**default_member)
        self.bot = bot

    async def timeoutmsg(self, ctx):
        await ctx.send("Timed out.")
        await asyncio.sleep(3)
        await ctx.channel.purge(after=ctx.message)
        await asyncio.sleep(.1)
        await ctx.message.delete()

    @commands.group()
    async def magenta(self,ctx):
        if ctx.invoked_subcommand is None:
            return

    @magenta.command()
    async def register(self, ctx):
        """
        Register a new character alias

        Walks you through the process of registering an alias, as well as shows
        you how to use the alias once it is registered.
        `>magenta register` - runs the command
        """
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        prompt = await ctx.send("Hiya! Welcome to the Megenta Character Alias Registration menu. I'll guide you through registering your character!\nBefore we start, I'll need you to go ahead and get some information ready for me!")
        prompt2 = await ctx.send("You will need:\n1.)Your character's name\n2.)Trigger symbol(s) to let me know you're trying to talk as your character in discord. These can be something like `%%`, `??`, `>>`, etc, etc. Please avoid using a single `>` as your trigger symbol because this is my command prefix in your discord and this will cause problems!\n3.)A direct image like to use for your character's alias image. This **must** be a direct image link ending in a file extension. If you do not have one available, you can always upload one to discord, right click the image and click copy image url!")
        prompt3 = await ctx.send("Once you've got all of this ready, let me know by sending a message that says 'ready'")
        i = 0
        while i == 0:
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if reply.content.lower() == "ready":
                i = 1
            else:
                await prompt3.edit(content="Whoops, I didn't recognize that response. Please enter `ready` when you've got everything you need!")
                await asyncio.sleep(3)
                await prompt3.edit(content="Once you've got all of this ready, let me know by sending a message that says 'ready'")
                i = 0
        await prompt2.delete()
        await prompt3.delete()
        await reply.delete()
        await prompt.edit(content="Alright! Lets get started! Just a moment while I build you a blank profile!")
        regem = discord.Embed(title="Alias Creator", description="\u200b", color=0x8B008B)
        ac = await ctx.send(embed=regem)
        await asyncio.sleep(1)
        regem.add_field(name="Character Name", value="\u200B")#0
        await ac.edit(embed=regem)
        await asyncio.sleep(1)
        regem.add_field(name="Trigger Symbol(s)", value="\u200B")#1
        await ac.edit(embed=regem)
        await asyncio.sleep(1)
        regem.set_thumbnail(url=ctx.author.avatar)
        await ac.edit(embed=regem)
        await prompt.delete()
        prompt = await ctx.send("Input your character's name.")
        try:
            reply = await self.bot.wait_for('message', check=check, timeout=120)
            char_name = reply.content.title()
        except asyncio.TimeoutError:
            await self.timeoutmsg(ctx)
            return
        char_name = reply.content.title()
        regem.set_field_at(0, name="Character Name", value=char_name)
        await ac.edit(embed=regem)
        await reply.delete()
        await asyncio.sleep(1)
        await prompt.edit(content="Now, lets input those symbols you decided on! Even if you're not entirely sure what these are for yet, go ahead and input them! I'll show you how to use them when we're done with registration!")
        try:
            reply = await self.bot.wait_for('message', check=check, timeout=120)
            syms = reply.content
        except asyncio.TimeoutError:
            await self.timeoutmsg(ctx)
            return
        regem.set_field_at(1, name="Trigger Symbol(s)", value=syms)
        await ac.edit(embed=regem)
        await reply.delete()
        await asyncio.sleep(1)
        await prompt.edit(content="And finally, its time for that direct image link I asked you to get earlier! Go ahead and paste that in and send it. This will serve as your character's avatar for the server! ^~^")
        try:
            reply = await self.bot.wait_for('message', check=check, timeout=120)
            avatar = reply.content
        except asyncio.TimeoutError:
            await self.timeoutmsg(ctx)
            return
        regem.set_thumbnail(url=avatar)
        await ac.edit(embed=regem)
        await reply.delete()
        await asyncio.sleep(1)
        i = 0
        while i == 0:
            await prompt.edit(content="You're all set! If you need to go back and change anything, go ahead and let me know now! You can respond with 'name', 'symbols', or 'avatar'. Otherwise, go ahead and enter 'save' and I'll save your character to my databank!")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if reply.content.lower() == "name":
                await prompt.edit(content="Input your character's name.")
                try:
                    await self.bot.wait_for('message', check=check, timeout=120)
                    char_name = reply.content.title()
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                await reply.delete()
                regem.set_field_at(0, name="Character Name", value=char_name)
                await ac.edit(embed=regem)
                i = 0
            elif reply.content.lower() == "symbols":
                await prompt.edit(content="Now, lets input those symbols you decided on! Even if you're not entirely sure what these are for yet, go ahead and input them! I'll show you how to use them when we're done with registration!")
                try:
                    syms = reply.content
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                await reply.delete()
                regem.set_field_at(1, name="Trigger Symbol(s)", value=syms)
                await ac.edit(embed=regem)
                i = 0
            elif reply.content.lower() == "avatar":
                await prompt.edit(content="And finally, its time for that direct image link I asked you to get earlier! Go ahead and paste that in and send it. This will serve as your character's avatar for the server! ^~^")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                    avatar = reply.content
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                await reply.delete()
                regem.set_thumbnail(url=avatar)
                await ac.edit(embed=regem)
                i = 0
            elif reply.content.lower() == "save":
                i = 1
        char_data = {"name":char_name, "symbols":syms, "avatar":avatar}
        await self.config.member(ctx.author).set_raw(char_name, value=char_data)
        await reply.delete()
        await ac.delete()
        await prompt.edit(content="Alright! I've got your alias all saved! Now lets show you how to use it!")
        await asyncio.sleep(1)
        await prompt.edit(content="To use your shiny new alias in the server, all you have to do is start your message off with {}!\n\nWhy don't you go ahead and give it a try! Send me a message starting off with {}.".format(syms, syms))
        i = 0
        while i == 0:
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if reply.content.startswith(syms) == False:
                await prompt.edit(content="Oops! Looks like you might have neglected to start your message off with those symbols of yours! Try that again but make sure you start your message off with {}.".format(syms))
                i = 0
            else:
                await prompt.edit(content="Awesome! Looks like you're all set! You can use your aliases in any channel within this server, but please remember they will not carry over to any other servers you might see me in!")
                return

    @magenta.command()
    async def aliases(self, ctx):
        """
        Returns a list of your registered aliases and their trigger Symbols

        `>magenta aliases` - runs the command
        """
        member = ctx.author
        char_dict = await self.config.member(member).get_raw()
        symbem = discord.Embed(title="{}'s Registered Aliases".format(ctx.author.display_name), description="\u200B", color=0x8B008B)
        symbem.set_thumbnail(url=ctx.author.avatar_url)
        aliem = await ctx.send(embed=symbem)
        for x in char_dict:
            try:
                y = await self.config.member(member).get_raw(x)
                symbem.add_field(name=y["name"], value=y["symbols"], inline=False)
                await aliem.edit(embed=symbem)
            except KeyError:
                pass
            except TypeError:
                pass

    @magenta.command()
    async def deregister(self, ctx):
        """
        Remove an alias from your list

        Step by step instructions for removing an alias from your list
        `>magenta deregister` -runs the command
        """
        member = ctx.author
        def check(msg):
            return ctx.author == msg. author and ctx.channel == msg.channel
        char_data = await self.config.member(member).get_raw()
        charem = discord.Embed(title="{}'s Registered Aliases".format(member.display_name), description="\u200B", color=0x8B008B)
        charem.set_thumbnail(url=member.avatar_url)
        charem.add_field(name="Character Name", value="\u200b")
        chem = await ctx.send(embed=charem)
        for x in char_data:
            try:
                y = await self.config.member(member).get_raw(x)
                charem.add_field(name="\u200B", value=y["name"], inline=False)
                await chem.edit(embed=charem)
            except KeyError:
                pass
        chars = list(char_data.keys())
        prompt = await ctx.send("Which character would you like to delete? Don't worry about capitalizing the names, I'll do it for you!")
        i = 0
        while i == 0:
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
                char_to_delete = reply.content.title()
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if char_to_delete not in chars:
                await prompt.edit(content="Whoops, I couldn't find that character, try that again!")
                await asyncio.sleep(3)
                await reply.delete()
                await prompt.edit(content="Which character would you like to delete? Don't worry about capitalizing the names, I'll do it for you!")
                i = 0
            else:
                await reply.delete()
                i = 1
            dlt = await self.config.member(member).get_raw(char_to_delete)
            charem2 = discord.Embed(title="{}'s Character".format(member.display_name), description="\u200b", color=0x8B008B)
            charem2.add_field(name="Character Name", value=dlt["name"])
            charem2.add_field(name="Trigger Symbol(s)", value=dlt["symbols"])
            charem2.set_thumbnail(url=dlt["avatar"])
            await chem.edit(embed=charem2)
            i = 0
            while i == 0:
                await prompt.edit(content="Are you sure you wish to deregister this character? This cannot be undone, however you can always register them again! Please respond only with 'yes' or 'no'.")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                if reply.content.lower() == "yes":
                    await self.config.member(member).clear_raw(dlt["name"])
                    await reply.delete()
                    await prompt.edit(content="1...2...3...POOF They're gone!")
                    i = 1
                elif reply.content.lower() == "no":
                    await prompt.edit(content="Okay! I'll leave them where they are in your list and terminate this function!")
                    i = 1
                    return
                else:
                    await prompt.edit(content="Whoops, that wasn't a valid response I'm afraid! Remember, 'yes' or 'no' only!")
                    await asyncio.sleep(2)
                    i = 0

    @magenta.command()
    async def edit(self, ctx):
        member = ctx.author
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        char_data = await self.config.member(member).get_raw()
        charem = discord.Embed(title="{}'s Registered Aliases".format(member.display_name), description="\u200B", color=0x8B008B)
        charem.set_thumbnail(url=member.avatar_url)
        charem.add_field(name="Character Name", value="\u200b")
        chem = await ctx.send(embed=charem)
        for x in char_data:
            try:
                y = await self.config.member(member).get_raw(x)
                charem.add_field(name="\u200B", value=y["name"], inline=False)
                await chem.edit(embed=charem)
            except KeyError:
                pass
            except TypeError:
                pass
        chars = list(char_data.keys())
        i = 0
        while i == 0:
            prompt = await ctx.send("Which character would you like to edit?")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            edt = reply.content.title()
            if edt not in chars:
                await reply.delete()
                await prompt.edit(content="Whoops! I can't seem to find that character. Try again!")
                i = 0
            else:
                i = 1
            char_data = await self.config.member(member).get_raw(edt)
            charem2 = discord.Embed(title="{}'s Character".format(member.display_name), description="\u200B", color=0x8B008B)
            charem2.set_thumbnail(url=char_data["avatar"])
            charem2.add_field(name="Character Name", value=char_data["name"])
            charem2.add_field(name="Trigger Symbol(s)", value=char_data["symbols"])
            await chem.edit(embed=charem2)
            await reply.delete()
            await prompt.edit(content="What would you like to edit? You may enter 'name', 'symbols', or 'avatar' only.")
                #lib variable name, text as it appears in the message, embed field number
            edit_vars = [("name", "Character Name", 0), ("symbols", "Trigger Symbol(s)", 1), ("avatar", "Avatar URL"), 2]

            i = 0
            while i == 0:
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                ev = None
                et = None
                for x in edit_vars:
                    try:
                        if reply.content.lower() == x[0]:
                            ev = x[0]
                            et = x[1]
                            y = x
                        else:
                            pass
                    except TypeError:
                        pass
                if ev == None and et == None:
                    await reply.delete()
                    await prompt.edit(content="Whoops, looks like that wasn't a valid response. Let's try that again!")
                    i = 0
                else:
                    i = 1
            await reply.delete()
            i = 0
            while i == 0:
                await prompt.edit(content="Please input your new {}".format(et))
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                nd = reply.content
                if ev == "symbols":
                    char_data2 = await self.config.member(member).get_raw()
                    syms_list = []
                    for x in char_data2.values():
                        try:
                            syms_list.append(x["symbols"])
                        except KeyError:
                            pass
                    if nd in syms_list:
                        await prompt.edit(content="Whoops! Looks like you've used those symbols for another character already! Lets try again!")
                        i = 0
                    else:
                        pass
                if ev == "avatar":
                    charem2.set_thumbnail(url=nd)
                    await chem.edit(embed=charem2)
                else:
                    charem2.set_field_at(y[2], name=y[1], value=nd)
                    await chem.edit(embed=charem2)
                await prompt.edit(content="Do(es) the updated {} look correct?".format(ev))
                try:
                    reply =  await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                if reply.content.lower() == "yes":
                    char_data = await self.config.member(member).get_raw()
                    char_data = await self.config.member(member).get_raw(edt)
                    print(char_data)
                    char_data[ev] = nd
                    print(char_data)
                    await self.config.member(member).set_raw(edt, value=char_data)
                    await prompt.edit(content="Alright! You're all saved and ready to go!")
                    i = 1
                elif reply.content.lower() == "no":
                    await prompt.edit(content="Whoops! Alright, lets try that again!")
                    await asyncio.sleep(2)
                    i = 0
            return

    @magenta.command()
    async def ignore(self, ctx):
        chan = ctx.channel
        guild = ctx.guild
        iglist = await self.config.guild(guild).get_raw()
        iglist = iglist["ignored_channels"]
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        if chan.id in iglist:
            i = 0
            while i == 0:
                prompt = await ctx.send("You want me to stop ignoring this channel? (Yes/No)")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=60)
                    if reply.content.lower() == "yes":
                        iglist.remove(chan.id)
                        await self.config.guild(guild).set_raw("ignored_channels", value=iglist)
                        await prompt.edit(content="Alright! You're all set, I'll no longer ignore this channel.")
                        i = 1
                    elif reply.content.lower() == "no":
                        await prompt.edit(content="Alright! I'll keep ignoring this channel!")
                        i = 1
                    else:
                        await prompt.edit(content="Whoops, I didn't understand that. Yes or no only please!")
                        await asyncio.sleep(3)
                        i = 0
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
        elif chan.id not in iglist:
            i = 0
            while i == 0:
                prompt = await ctx.send("You want me to stop listening to this channel? (Yes/No)")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=60)
                    if reply.content.lower() == "yes":
                        iglist.append(chan.id)
                        await self.config.guild(guild).ignored_channels.set(iglist)
                        await prompt.edit(content="Alright! You're all set, I'll stop listenening to this channel.")
                        i = 1
                    elif reply.content.lower() == "no":
                        await prompt.edit(content="Alright! I'll keep listening to this channel!")
                        i = 1
                    else:
                        await prompt.edit(content="Whoops, I didn't understand that. Yes or no only please!")
                        await asyncio.sleep(3)
                        i = 0
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
        await asyncio.sleep(5)
        await ctx.channel.purge(after=ctx.message)
        await asyncio.sleep(.5)
        await ctx.message.delete()




    @commands.command()
    async def roll(self, ctx, params:str):
        params = params.lower()
        iter, sides = params.split("d")
        bonus = 0
        try:
            try:
                sides, bonus = sides.split("+")
                op = 1
            except ValueError:
                sides, bonus = sides.split('-')
                op = 2
        except ValueError:
            op = 0
        iter = int(iter)
        sides = int(sides)
        bonus = int(bonus)
        results = []
        i = iter
        while i > 0:
            x = random.randint(1, sides)
            results.append(x)
            i = i - 1
        try:
            if op == 0:
                y = sum(results)
                await ctx.send("\n{} results:```py\n{}\nTotal:{}```".format(params,
                results, y))
            elif op == 1:
                y = sum(results) + bonus
                await ctx.send("\n{} results:```py\n{}\nTotal:{}```".format(params,
                results, y))
            elif op == 2:
                y = sum(results) - bonus
                await ctx.send("\n{} results:```py\n{}\nTotal:{}```".format(params,
                results, y))
        except ValueError:
            error = await ctx.send("Whoops, looks like I've encountered an error!")
            await asyncio.sleep(3)
            await error.delete()
            return

    @commands.Cog.listener()
    async def on_message(self, msg):
        iglist = await self.config.guild(msg.guild).get_raw()
        iglist = iglist["ignored_channels"]
        if msg.author.bot == True:
            return
        elif msg.channel.id in iglist:
            return
        else:
            hooks = await msg.channel.webhooks()
            i = 0
            e = False
            while i == 0:
                for x in hooks:
                    if x.name == "Magenta":
                        hook = x
                        i = 1
                        e = True
                    else:
                        pass
                if e == False:
                    new_hook = await msg.channel.create_webhook(name="Magenta", avatar=None, reason=None)
                    hook = await self.bot.fetch_webhook(new_hook.id)
                    i = 1
                else:
                    i = 1
            member = msg.author
            meminfo = await self.config.member(member).get_raw()
            for y in meminfo:
                try:
                    z = await self.config.member(member).get_raw(y)
                    if msg.content.startswith(z["symbols"]):
                        msgcontent = msg.content.replace(z["symbols"], "\u200b")
                        if len(msgcontent) > 2000:
                            for page in pagify(msgcontent, delims=["\n"], page_length=1800):
                                await hook.send(content=page, username=z["name"], avatar_url=z["avatar"])
                                await asyncio.sleep(1)
                        else:
                            await hook.send(content=msgcontent, username=z["name"], avatar_url=z["avatar"])
                        await asyncio.sleep(.5)
                        await msg.delete()
                except KeyError:
                    pass
                except TypeError:
                    pass
                except Exception as e: log.error("error in message listener", exc_info=e)
###test setup for an image gallery, might add this to the paradiso bot if I can get it to work


    @commands.group()
    async def gallery(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @gallery.command()
    async def show(self, ctx, member:discord.Member):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        user_data = await self.config.member(member).get_raw()
        charem = discord.Embed(title="{}'s Characters".format(member.display_name), description="\u200b")
        names = ", ".join(user_data.keys())
        charem.add_field(name="{}".format(names), value="\u200b")
        interface = await ctx.send(embed=charem)
        prompt = await ctx.send("Which character gallery would you like to view? Please be sure to type the name ***exactly*** as it appears in the embed above. Registered aliases that have more than one name (IE a given name and surname should be put in quotation marks.)")
        try:
            reply = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await self.timeoutmsg(ctx)
            return
        selection = reply.content
        try:
            char_data = await self.config.member(member).get_raw(selection)
        except KeyError:
            error = await ctx.send("Whoops! Couldn't find that character!")
        charem.remove_field(0)
        try:
            img_lib = char_data["img_lib"]
        except KeyError:
            img_lib = []
            await self.config.member(member).set_raw(char_data, value=[])
            print("successful")



"""
New Character Sheet module for testing###
"""
    @commands.group()
    async def sheet(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    async def user_inputs(self, ctx, user_end, key_name):
        #message check to prevent input from other users or channels
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        #timeout variable to pass back to command function
        to = False
        #first attempt to thwart the TypeError
        input_var = ""
        #loop to allow for changes in response before finalizing
        i = 0
        while i == 0:
            #secondary prompt init
            prompt = await ctx.send(content="What is the {} you would like to use for {}?".format(user_end, key_name))
            #try loop to implement timeout functionality
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                #timeout function (at top of hastebin page)
                await self.timeoutmsg(ctx)
                #sets the timeout variable to True to indicate main function should break loop and terminate
                to = True
                return input_var, to
            input_var = reply.content
            if user_end == "short description (100 characters or less)":
                if len(input_var) > 100:
                    await reply.delete()
                    await prompt.edit(content="Whoops, that was too long! Try to make it a bit shorter! (100 characters or less!)")
                    await asyncio.sleep(3)
                    await prompt.delete()
                    continue
            elif user_end == "base value (if none, input 0)":
                try:
                    input_var = int(input_var)
                except ValueError:
                    await reply.delete()
                    await prompt.edit(content="Whoops! I need that in integer format so I can do math with it later! (1, 2, 3, 4, etc)")
                    await asycio.sleep(3)
                    await prompt.delete()
                    continue
            await reply.delete()
            #confirmation prompt
            await prompt.edit(content="You entered {}. Is this correct? (Yes/No)".format(input_var))
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                to = True
                return input_var, to
            if reply.content.lower() == "yes":
                await reply.delete()
                await prompt.edit(content="Good, I'll get that saved!")
                await asyncio.sleep(2)
                await prompt.delete()
                i = 1
            elif reply.content.lower() == "no":
                await reply.delete()
                await prompt.edit(content="Whoops! We can try that again! Just a moment!")
                await asyncio.sleep(3)
                await prompt.delete()
                i = 0
            else:
                await reply.delete()
                await prompt.edit(content="I'm sorry, I didn't quite understand that. We can try that again. Just a moment!")
                await asyncio.sleep(3)
                await prompt.delete()
                i = 0
        return input_var, to

    @sheet.group()
    async def setup(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @setup.command()
    async def stats(self, ctx):
        """
        setup stats to be tracked

        `>sheet setup2 - runs the command. Allows administrator to set the stats that will be tracked`
        """
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        primary_stats = {}
        stat_completion_check = await self.config.guild(ctx.guild).stats_completion()
        #embed init
        sheetem = discord.Embed(title="Sheet Setup", description="\u200b")
#########primary_stats
        try:
            primary_check = stat_completion_check["primary_stats"]
            print(primary_check)
        except TypeError:
            primary_check = False
            print("TypeError occured")
        while primary_check == False:
            i = 0
            while i == 0:
                prompt = await ctx.send("Lets get started! First thing's first, Primary Stats; How many would you like to track?")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                try:
                    stat_num = int(reply.content)
                except ValueError:
                    await prompt.edit(content="Whoops, I need that to be in integer format please! (1, 2, 3, etc)")
                    await asyncio.sleep(2)
                    continue
                await reply.delete()
                i = 1
            counter = 1
            while counter <= stat_num:
                save_format = "stat{}".format(counter)
                user_format = "Stat {}".format(counter)
                primary_stats[save_format] = {}
                quieries = [
                    ("name", "name", user_format),
                    ("abbreviation", "abbreviation", user_format),
                    ("base value (if none, input 0)", "value", user_format),
                    ("short description (100 characters or less)", "short_desc", user_format)
                ]
                for x in quieries:
                    user_end = x[0]
                    save_var = x[1]
                    key_name = x[2]
                    input_var, to = await self.user_inputs(ctx, user_end, key_name)
                    if to == True:
                        break
                    else:
                        primary_stats[save_format][save_var] = input_var
                counter = counter + 1
                if to == True:
                    break
            if to == True:
                return
            else:
                pass
            field_value = ""
            field_format= ""
            stat_counter = 0
            for x in primary_stats.keys():
                stat_counter = stat_counter + 1
                if stat_counter % 2 == 0:
                    field_value = field_value + " {}: {}\n".format(primary_stats[x]["abbreviation"], primary_stats[x]["value"])
                else:
                    field_value= field_value + "{}: {}".format(primary_stats[x]["abbreviation"], primary_stats[x]["value"])
            field_value = "```{}```".format(field_value)
            sheetem.add_field(name="Primary Stats", value=field_value.format(field_format))
            await prompt.edit(content="\u200b", embed=sheetem)
            #create stats completion config variable
            stats_completion = {
                "primary_stats": True
            }
            #set primary completion to true
            await self.config.guild(ctx.guild).stats_completion.set(stats_completion)
            await asyncio.sleep(.5)
            #save stats to config
            stats = await self.config.guild(ctx.guild).stats()
            stats["primary_stats"] = primary_stats
            await self.config.guild(ctx.guild).stats.set(stats)
            #not sure why I did this, but it stays
            primary_check = await self.config.guild(ctx.guild).stats_completion(primary_stats)
            if primary_check == True:
                break
            else:
                continue
#########secondary stats
        try:
            secondary_check = await self.config.guild(ctx.guild).stats_completion()
            seconary_check = secondary_check["secondary_stats"]
        except KeyError:
            secondary_check = False
        while secondary_check == False:
            i = 0
            while i == 0:
                prompt2 = await ctx.send("Alright, primary stats are taken care of! Are there any secondary stats you'd like to track? (Yes/No)")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                if reply.content.lower() == "yes":
                    i = 1
                    sec_stats = True
                    await reply.delete()
                elif reply.content.lower() == "no":
                    i = 1
                    sec_stats = False
                    await reply.delete()
                else:
                    await reply.delete()
                    await prompt2.edit(content="Whoops, I didn't quite understand that. We can try again in a moment!")
                    await asyncio.sleep(1)
                    i = 0
            if sec_stats == True:
                i = 0
                while i == 0:
                    await prompt2.edit(content="Alright! How many would you like to track?")
                    try:
                        reply = await self.bot.wait_for('message', check=check, timeout = 15)
                    except asyncio.TimeoutError:
                        await self.timeoutmsg(ctx)
                        return
                    try:
                        stat_num = int(reply.content)
                        i = 1
                    except ValueError:
                        await prompt2.edit(content="Whoops, I need that to be in integer format please! (1, 2, 3, etc)")
                        await asyncio.sleep(2)
                        i = 0
                counter = 1
                secondary_stats = {}
                while counter <= stat_num:
                    save_format = "stat{}".format(counter)
                    user_format = "Stat {}".format(counter)
                    secondary_stats[save_format] = {}
                    quieries = [
                        ("name", "name", user_format),
                        ("abbreviation", "abbreviation", user_format),
                        ("base value (if none, input 0)", "value", user_format),
                        ("short description (100 characters or less)", "short_desc", user_format)
                    ]
                    for x in quieries:
                        user_end = x[0]
                        save_var = x[1]
                        key_name = x[2]
                        input_var, to = await self.user_inputs(ctx, user_end, key_name)
                        if to == True:
                            break
                        else:
                            secondary_stats[save_format][save_var] = input_var
                    counter = counter + 1
                    if to == True:
                        break
                if to == True:
                    return
                else:
                    pass

                field_value = ""
                stat_counter = 0
                for x in secondary_stats.keys():
                    stat_counter = stat_counter + 1
                    if stat_counter % 2 == 0:
                        field_value = field_value + " {}: {}\n".format(secondary_stats[x]["abbreviation"], secondary_stats[x]["value"])
                    else:
                        field_value = field_value + "{}: {}".format(secondary_stats[x]["abbreviation"], secondary_stats[x]["value"])
                field_value = "```{}```".format(field_value)
                sheetem.add_field(name="Secondary Stats", value=field_value)
                try:
                    await prompt.edit(embed=sheetem)
                except UnboundLocalError:
                    stat_counter = 0
                    primary_field_value = ""
                    primay_stats = await self.config.guild(ctx.guild).stats.primary_stats()
                    print(primary_stats)
                    for x in primary_stats.keys():
                        stat_counter = stat_counter + 1
                        if stat_counter % 2 == 0:
                            primary_field_value = primary_field_value + "{}: {}\n".format(primary_stats[x]["abbreviation"], primary_stats[x]["value"])
                        else:
                            primary_field_value = primary_field_value + "{}: {}".format(primary_stats[x]["abbreviation"], primary_stats[x]["value"])
                    primary_field_value = "```{}```".format(primary_field_value)
                    sheetem = discord.Embed(title="Sheet Setup", description="\u200b")
                    sheetem.add_field(name="Primary Stats", value=primary_field_value)
                    sheetem.add_field(name="Secondary Stats", value=field_value)
                    prompt = await ctx.send(embed=sheetem)

                #set secondary stats completion to true
                stats_completion = await self.config.guild(ctx.guild).stats_completion()
                stats_completion["secondary_stats"] = True
                #save stats to config
                stats = await self.config.guild(ctx.guild).stats()
                stats["secondary_stats"] = secondary_stats
                await self.config.guild(ctx.guild).stats.set(stats)
                #not really sure what I did this for, but we're going to keep it just in case its doing something important
                await self.config.guild(ctx.guild).stats_completion.set(stats_completion)
                await asyncio.sleep(.5)
                secondary_check = await self.config.guild(ctx.guild).stats_completion(secondary_stats)
                ##########
                if secondary_check == True:
                    break
                else:
                    continue
#########other stats
        try:
            #pull config data
            other_check = await self.config.guild(ctx.guild).stats_completion()
            #attempt to check for other_stats variable
            other_check = other_check["other_stats"]
        except KeyError:
            #no variable exists, set other_check to false
            other_check = False
        try:
            await prompt2.delete()
        except UnboundLocalError:
            pass
        while other_check == False:
            i = 0
            while i == 0:
                #prompt2 was deleted above for previous segment, restarting it here for continuances
                #and starting it for the first time if this category is come back to.
                prompt2 = await ctx.send("Do you have any other stats you would like to keep track of? (Yes/No)")
                #attain user response
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)#need to change timeouts back to 120 when
                except asyncio.TimeoutError:                                           #all is said and done
                    #terminate function upon timeout
                    await self.timeoutmsg(ctx)
                    return
                #user response options.
                if reply.content.lower() == "yes":
                    await reply.delete()
                    i = 1
                elif reply.content.lower() == "no":
                    await reply.delete()
                    await prompt2.edit(content="Alright, let me clean up a bit!")
                    await asyncio.sleep(3)
                    await ctx.channel.purge(after=ctx.message)
                    await ctx.message.delete()
                    return
                else:
                    await reply.delete()
                    await prompt2.edit(content="Whoops, I didn't quite understand that. Lets try again in a moment!")
                    await asyncio.sleep(2)
                    await prompt2.delete()
                    i = 0
            #obtain category name from user
            await prompt2.edit(content="Alright! Let's get started! What would you like to name this stat category?")
            #user response
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            #create the user-end display for the category name
            stat_cat_user = reply.content.title()
            #create the config end category name
            stat_cat_save = reply.content.lower()
            stat_cat_save = reply.content.replace(" ", "_")
            #pull other stats from config for later use
            stats_dict = await self.config.guild(ctx.guild).stats()
            #create new sub dict for user entered stat category
            stats_dict[stat_cat_save] = {}
            await self.config.guild(ctx.guild).stats.set(stats_dict)
            await asyncio.sleep(1)
            stats_dict = await self.config.guild(ctx.guild).stats()
            await reply.delete()
            #change prompt to retrieve number of stats to be tracked for this category
            i = 0
            while i == 0:
                await prompt2.edit(content="{} it is! How many stats will you be tracking in this category?".format(stat_cat_user))
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=120)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                try:
                    stat_num = int(reply.content)
                    await reply.delete()
                    i = 1
                except ValueError:
                    await reply.delete()
                    await prompt2.edit(content="Whoops! I need that in integer format! (1, 2, 3, etc) We can try again in a moment!")
                    await asyncio.sleep(2)
                    i = 0
            counter = 1
            while counter <= stat_num:
                save_format = "stat{}".format(counter)
                user_format = "Stat {}".format(counter)
                stats_dict[stat_cat_save][save_format] = {}
                quieries = [
                    ("name", "name", user_format),
                    ("abbreviation", "abbreviation", user_format),
                    ("base value (if none, input 0)", "value", user_format),
                    ("short description (100 characters or less)", "short_desc", user_format)
                ]
                for x in quieries:
                    user_end = x[0]
                    save_var = x[1]
                    key_name = x[2]
                    input_var, to = await self.user_inputs(ctx, user_end, key_name)
                    if to == True:
                        break
                    else:
                        stats_dict[stat_cat_save][save_format][save_var] = input_var
                counter = counter + 1
                if to == True:
                    return
            await self.config.guild(ctx.guild).stats.set(stats_dict)
            field_value = ""
            field_format = ""
            stat_counter = 0
            sheetem = discord.Embed(title="Sheet Setup", description="\u200b")
            stats = await self.config.guild(ctx.guild).stats()
            for x in stats:
                for y in stats[x]:
                    field_value = ""
                    field_name = x.replace("_", " ")
                    field_name = field_name.title()
                    stat_counter = stat_counter + 1
                    if stat_counter % 2 == 0:
                        field_value = field_value + " {}: {}\n".format(stats[x][y]["abbreviation"], stats[x][y]["value"])
                    else:
                        field_value= field_value + "{}: {}".format(stats[x][y]["abbreviation"], stats[x][y]["value"])
                    field_value = "```{}```".format(field_value)
                sheetem.add_field(name=field_name.title(), value=field_value.format(field_format))
            try:
                await prompt.delete()
            except UnboundLocalError:
                pass
            await ctx.channel.purge(after=ctx.message)
            sheetemsend = await ctx.send(embed=sheetem)
            prompt = await ctx.send("Do you have any other stats you would like to keep track of? (If yes, this prompt will repeat)")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=120)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if reply.content.lower() == "yes":
                other_check = False
            else:
                other_check = True


        await ctx.send("All of your stats are set up!")

    async def abort(self, ctx):
        await ctx.channel.purge(after=ctx.message)
        await ctx.message.delete()
        return

    @setup.command()
    async def actions(self, ctx):
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        prompt = await ctx.send("Alright, this one might take a bit of time so know that I'll be saving your data every time you complete every action so if you need to stop at any point, you can either let me time out or enter 'abort' at any prompt and I'll save and terminate." )
        prompt_ctn = await ctx.send(
        "So, lets dive into this one head first shall we?! What are actions? These would be your players' abilities, their spells, their attacks, etc. Everything that you want to have a preset dice roll for should be set in here. (Don't worry, you'll be able to edit these dice rolls as you go!)")
        prompt_ctn2 = await ctx.send("This part might take a while so I'd suggest getting everything ready before you start, but as I said above, if you need to stop you can either let me time out or enter 'abort' at the end of any action input section. When you're ready to start you can let me know by entering 'ready' Any other input will terminate this function.")
        try:
            ctn = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await self.timeoutmsg(ctx)
            return
        if ctn.content.lower() == "ready":
            await ctn.delete()
            await prompt_ctn.delete()
            await prompt_ctn2.delete()
        else:
            await self.abort(ctx)
            return
        new_action = True
        action_counter = 1
        while new_action == True:
            user_format = "Ability {}".format(action_counter)
            save_format = "ability{}".format(action_counter)
            i = 0
            while i == 0:
                await prompt.edit(content="What would you like to name {}".format(user_format))
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await timeoutmsg(ctx)
                    return
                action_name = reply.content.title()
                await reply.delete()
                await prompt.edit(content="You entered {}. Is this correct? (Yes/No)")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=60)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                if reply.content.lower() == "yes":
                    await reply.delete()
                    i = 1
                elif reply.content.lower() == "no":
                    await prompt.edit(content="Whoops! No worries, we can try that again in just a moment!")
                    await reply.delete()
                    await asyncio.sleep(2)
                    i = 0
                else:
                    await prompt.edit(content="Sorry, I didn't understand that. We can try again in just a moment.")
                    await reply.delete()
                    await asyncio.sleep(2)
                    i = 0
                actionem = discord.Embed(title=action_name, description="Action Card")
                action_card = await ctx.send(embed=actionem)
                prompt_data = [
                ("short description", "short_desc", save_format),
                ("dice string (ex.: 1d6 + STR)", "dice_value", save_format),
                ("action icon (this must be a direct image link, if you do not have one handy simply enter 'None' and you can edit this later)", "icon", save_format)
                ]
                action_dict = await self.config.guild(ctx.guild).actions()
                for x in prompt_data:
                    user_end = x[0]
                    save_var = x[1]
                    key_name = x[2]
                    input_var, to = await self.user_inputs(ctx, user_end, key_name)
                    if to == True:
                        return
                    else:
                        action_dict[save_format][save_var] = input_var
                action_counter = action_counter + 1
                print(action_dict)
                new_action = True


    @commands.command
    async def distest(self, ctx):
        field_value = ""
        field_format = ""
        stat_counter = 0
        sheetem = discord.Embed(title="Sheet Setup", description="\u200b")
        stats = await self.config.guild(ctx.guild).stats()
        for x in stats:
            for y in stats[x]:
                field_value = ""
                field_name = x.replace("_", " ")
                stat_counter = stat_counter + 1
                if stat_counter % 2 == 0:
                    field_value = field_value + " {}: {}\n".format(stats[x][y]["abbreviation"], stats[x][y]["value"])
                else:
                    field_value= field_value + "{}: {}".format(stats[x][y]["abbreviation"], stats[x][y]["value"])
                field_value = "```{}```".format(field_value)
            sheetem.add_field(name=field_name.title(), value=field_value.format(field_format))
        await ctx.send(embed=sheetem)


    @commands.command()
    async def getconf(self, ctx):
        conf = await self.config.guild(ctx.guild).get_raw()
        await ctx.send(conf)

    @commands.command()
    async def clearconf(self, ctx):
        await self.config.guild(ctx.guild).clear()
        await asyncio.sleep(.5)
        conf = await self.config.guild(ctx.guild).all()

    @commands.command()
    async def getprimary(self, ctx):
        ps2 = await self.config.guild(ctx.guild).stats.primary_stats()
        await ctx.send("Pull 2 = {}".format(ps2))

    @commands.command()
    async def setsecfalse(self, ctx):
        a = await self.config.guild(ctx.guild).stats_completion()
        a["secondary_stats"] = False
        await self.config.guild(ctx.guild).stats_completion.set(a)

    @commands.command()
    async def preggercheck(self, ctx):
        condom_used = False
        condom_break = False
        ovulating = False
        position = None
        variable_offset = 0
        pregger_threshold = await self.config.guild(ctx.guild).pregger_threshold()
        def check(msg):
            return ctx.author == msg.author and ctx.channel == msg.channel
        prompt = await ctx.send("Time to see if she's pregnant!\nhttps://cdn.discordapp.com/attachments/724556110694055967/864414419152928768/tumblr_nu12bgdadu1tvoimto1_500.gif")
        await asyncio.sleep(3)
"""
condom check
"""
        i = 0
        while i == 0:
            await prompt.edit(content="Was a condom used?")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            if reply.content.lower() == "yes":
                await reply.delete()
                condom_used = True
                variable_offset = variable_offset + 1
                i = 1
            elif reply.content.lower() == "no":
                await reply.delete()
                condom_used = False
                variable_offset = variable_offset + 20
                i = 1
            else:
                await reply.delete()
                await prompt.edit(content="Yes or no only you goof!")
                i = 0
        await asyncio.sleep(1)
"""
###comdom used
"""
        if condom_used == True:
"""
###roughness
"""
            ii = 0
            while ii == 0:
                await prompt.edit(content="On a scale of 1 to 10, how rough was it?")
                try:
                    reply = await self.bot.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    await self.timeoutmsg(ctx)
                    return
                try:
                    roughness = int(reply.content)
                    await reply.delete()
                    ii = 1
                except ValueError:
                    await reply.delete()
                    await prompt.edit(content="Whoops, needs to be an integer. (1, 2, 3, etc)")
                    await asyncio.sleep(3)
                    ii = 0
            if 5 >= roughness >= 1:
                condom_break_threshold = 90
            elif 8 >= roughness >= 6:
                condom_break_threshold = 60
            else:
                condom_break_threshold = 50
            break_check = random.randint(1, 100)
            if break_check > condom_break_threshold:
                condom_break = True
            if condom_break == True:
                await prompt.edit(content="Well, looks like those two had some pretty rough sex. The condom broke. Whoops!")
        await asyncio.sleep(5)
"""
ovulation check
"""
        iii = 0
        while iii == 0:
            await prompt.edit(content="Lets see if she was ovulating...what is the numerical value for today's date? (If the date is 06/09/21, enter 09 or 9)")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            try:
                date = int(reply.content)
                await reply.delete()
                iii = 1
            except ValueError:
                await reply.delete()
                await prompt.edit(content="I SAID JUST THE NUMBER YOU FEEBLE FOOL!")
                await asyncio.sleep(3)
                iii = 0
        ovustart = await self.config.guild(ctx.guild).ovualation_start()
        ovuend = await self.config.guild(ctx.guild).ovulation_end()
        if ovuend >= date >= ovustart:
            ovulating = True
            variable_offset = variable_offset + 10
        if ovulating == True and condom_break == True:
            await prompt.edit(content="Ooof. Welp, not only did the condom break, but she was ovulating. It's not looking good for her, champ.")
        elif ovulating == True and condom_break == False:
            await prompt.edit(content="Well it's a good thing the condom didn't break, cuz this bitch be ovulating!")
        elif ovulating == False and condom_break == True:
            await prompt.edit(content="Well, good news is, she wasn't ovulating...")
        elif ovulating == False and condom_break == False:
            await prompt.edit(content="You're double lucky. Intact condom, no ovulation")
        await asyncio.sleep(5)
"""
position check
"""
        iiii = 0
        while iiii == 0:
            await prompt.edit(content="Alright, last question! What position was she in when the deed was done? If you don't see it listed here, just use the closest one to it! Enter the number only.")
            options = await ctx.send("1.) Missionary\n2.) Doggy\n3.) Mating Press\n4.) Cowgirl\n5.) Reverse Cowgirl\n6.) Back Against the wall")
            try:
                reply = await self.bot.wait_for('message', check=check, timeout=30)
            except asyncio.TimeoutError:
                await self.timeoutmsg(ctx)
                return
            try:
                position = int(reply.content)
                await reply.delete()
                await options.delete()
                iiii = 1
            except ValueError:
                await reply.delete()
                await options.delete()
                await prompt.edit(content="I SAID JUST THE NUMBER GODDAMNIT")
                await asyncio.sleep(3)
                iiii = 0
        if position == 1:
            variable_offset = variable_offset + 10
        elif position == 2:
            variable_offset = variable_offset + 10
        elif position == 3:
            variable_offset = variable_offset + 15
        elif position == 4:
            variable_offset = variable_offset + 5
        elif position == 5:
            variable_offset = variable_offset + 5
        elif position == 6:
            variable_offset = variable_offset + 5
        pregger_threshold = pregger_threshold - variable_offset
        final_check = random.randint(1, 100)
        if final_check > pregger_threshold or final_check == 69:
            await prompt.edit(content="Better start buying diapers, because that bitch be preggers!")
        else:
            await prompt.edit(content="You lucked out this time kid, no bun in the oven!")
































































#            v1 = [random.randint(1, 6) for i in range(5)]
#            v1.remove(min(v1))
#            v1.remove(min(v1))
#            v1 = sum(v1)
#            if v1 < 8:
#                v1 = 8
#            v2 = [random.randint(1, 6) for i in range(5)]
#            v2.remove(min(v2))
#            v2.remove(min(v2))
#            v2 = sum(v2)
#            if v2 < 8:
#                v2 = 8
#            v3 = [random.randint(1, 6) for i in range(5)]
#            v3.remove(min(v3))
#            v3.remove(min(v3))
#            v3 = sum(v3)
#            if v3 < 8:
#                v3 = 8
#            v4 = [random.randint(1, 6) for i in range(5)]
#            v4.remove(min(v4))
#            v4.remove(min(v4))
#            v4=sum(v4)
#            if v4 < 8:
#                v4 = 8
#            v5 = [random.randint(1, 6) for i in range(5)]
#            v5.remove(min(v5))
#            v5.remove(min(v5))
#            v5 = sum(v5)
#            if v5 < 8:
#                v5 = 8
#            v6 = [random.randint(1, 6) for i in range(5)]
##            v6.remove(min(v6))
#            v6 = sum(v6)
#            if v6 < 8:
#                v6 = 8

#        results = [v1, v2, v3, v4, v5, v6]
