import os
import logging
import time
from discord.ext import commands, flags
from .utils import *
from .command_helpers import SoundHelpers

#TODO: Readd on_ready related functions
#TODO: Readd shitpost functions (saying nword bad)


class SoundsCog(commands.Cog, name="Make the bot make noise."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sound(self, ctx, *args):
        sound_maps = return_sound_maps()
        maps = {
            "play": SoundHelpers.sound_play,
            "add": SoundHelpers.sound_add,
            "list": SoundHelpers.sound_list,
            "tts": SoundHelpers.sound_tts,
            "remove": SoundHelpers.sound_remove
            }
        
        if args[0] == "help" or args[0] not in maps.keys():
            msg = "!sound <soundname> : Plays the sound(if I know it)\n!sound add <sound name(No spaces)> <mp3link> : Downloads a soundfile and saves the definition to play it later \n!sound list : Lists the sounds I know \n!sound tts [--voice Brain/Amy/...] \"Text Goes Here\""
            await ctx.send(help_msg(msg))
            
        elif args[0] in maps.keys():
                await maps[args[0]](ctx, *args[1:])
                
    @sound.error
    async def info_error(self, ctx, error):
        if "message" in dir(error.original):
            await ctx.send(error.original.message)
        else:
            logging.info(error)
            await ctx.send("An error has occured. Sorry can't be less secure. ask the developer.")

class MiscCog(commands.Cog, name="Miscellaneous functions"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener(name="on_member_update")
    async def bigcockalarm(self, before, after):
        if 321054194054201344 == before._user.id and before.nick != after.nick:
            await after.guild.get_member(321054194054201344).edit(nick=config.BOTNAME)
        limp_dicks = []

        if 719058425241272411 in [role.id for role in before.roles] and 719058425241272411 not in [role.id for role in after.roles]:
            response = f"@everyone <@{after._user.id}> HAS GOTTEN HARD!"
            await after.guild.get_channel(700170332551774282).send(response)

        # if it was in after but not in before 
        elif 719057975645306930 in [role.id for role in after.roles] and 719057975645306930 not in [role.id for role in before.roles]:
            if after._user.id in limp_dicks:
                await after.remove_roles(after.guild.get_role(719057975645306930))
                await after.add_roles(after.guild.get_role(719058425241272411))
                response = f"<@{after._user.id}> Tried to be added to the big cock role! but was added to limp penis instead" 
                await after.guild.get_channel(700170332551774282).send(response)
            else:
                response = f"@everyone BIG COCK ALARM! <@{after._user.id}> WOULD LIKE YOU TO KNOW THAT HE HAS A BIG COCK! BIG COCK ALARM!"
                await after.guild.get_channel(700170332551774282).send(response)

    @commands.command()
    async def quiplash(self, ctx, *args):
        response = f"@everyone ITS QUIPLASH TIME EVERYBODY, CAN I GET ANY QUIPLASHERS IN THE CHAT"
        for x in range(0,5):
            await ctx.send(response)
            time.sleep(1.2)
        return


    @commands.command(name="eval")
    async def evaluate(self, ctx, *, msg: str):
        if ctx.author.id != 216321712067706881:
            return
        message = msg.split("```")[1]
        if message.startswith("py"): message = message[2:]
        if message.startswith("\n"): message = message[1:]
        wrapper = f"async def _eval_exp():"
        for line in message.splitlines():
            wrapper += (f"\n\t{line}")
        env = {"ctx": ctx}
        exec(compile(wrapper, "trashname", "exec"), env)
        await eval("_eval_exp()", env)
        return


    @commands.command()
    async def owo(self, ctx, *args):
        await ctx.send(owoifier(" ".join(args)))
    
    @commands.command()
    async def ascii(self, ctx, *args):
        valid_filetypes = ["jpeg", "png", "jpg"]
        filename = ctx.message.attachments[0].filename.split(".")[1]
        if filename not in valid_filetypes:
            raise InvalidArguments("You used a bad picture.")
        flags = {"--more-detail": False, "--cols": 60, "--scale": .43}
        for index, item in enumerate(args):
            if item[0:2] == "--":
                if item not in flags.keys():
                    raise IvalidArguments
                    return
                else:
                    flags[item] = args[index+1]
        try:
            flags = {"--more-detail": bool(flags["--more-detail"]), "--cols": int(flags["--cols"]), "--scale": float(flags["--scale"])}
        except:
            InvalidArguments("The Flags you passed had an invalid datatype")
        picture = io.BytesIO()
        await ctx.message.attachments[0].save(picture)
        art = Asciiifier(picture, flags["--more-detail"], flags["--cols"], flags["--scale"])
        await ctx.send(art.ascii_art)

    @commands.command(name="derp", aliases=["d", "twitter"])
    async def derpify(self, ctx, *, string):
        from random import choice
        await ctx.send(derp(string, choice([True, False])))
        

    @commands.command(name="annoyjosh")
    @commands.max_concurrency(1, wait=True)
    async def uhoh(self, ctx, youtube_link):
        josh = False
        if ctx.message.author.id == 216321712067706881:
            josh = True
        import re
        pattern = re.compile(r"^(http(s)??\:\/\/)?(www\.)?((youtube\.com\/watch\?v=)|(youtu.be\/))([a-zA-Z0-9\-_])+")
        if pattern.match(youtube_link):
            import requests
            import youtube_dl
            with youtube_dl.YoutubeDL() as ydl:
                length = ydl.extract_info(youtube_link, download=False).get("duration") 
                if length > 31 and not josh:
                    await ctx.send(f"Too Long, length was {length}")
                    return
            message = await ctx.send("Sending message")
            resp = requests.post(f"http://192.168.86.69/alert?url={youtube_link}&is_josh={josh}&password=L5FwBEZNxBE")
            
            logging_channel = discord.utils.get(ctx.guild.channels, name="bot-logs")
            await logging_channel.send(f"{ctx.author} sent a message\n{youtube_link}")

            await message.delete()
            await ctx.message.delete()
            return
        await ctx.send("Didn't match a youtube link")


    @flags.add_flag("--previous", type=bool, default=False)
    @flags.add_flag("--limit", type=int, default=50)
    @flags.add_flag("--message", type=int, default=0)
    @flags.command(name="purge")
    @commands.max_concurrency(1, wait=True)
    async def purge(self, ctx, member: discord.Member, **flags):
        if ctx.author.id != 216321712067706881:
            return 

        previous_message = None
        tagged_message = None 

        if flags["previous"] and flags["message"]:
            await ctx.send("Previous and Message are mutually exclusive. Use one or the other dipshit.")
            return

        if flags["message"] != 0:
            tagged_message = await ctx.channel.fetch_message(flags["message"])
            if not tagged_message:
                await ctx.send(f"Could not find message wit that ID.")
                return
        
        if flags["previous"]:
            async for message in ctx.history(limit=flags["limit"]):
                if message.author == member:
                    previous_message = message
                    break
        if flags["previous"] and not previous_message:
            await ctx.send(f"Could not find a message by {member.name}, try running the command with with a higher --limit.")
        count = 0
        async for message in ctx.history(limit=flags["limit"]):
            if message.author == member:
                if flags["previous"] and previous_message == message:
                    await message.delete(delay=1)
                    count += 1
                elif flags["previous"] and previous_message != message:
                    continue
                elif tagged_message:
                    if message.content == tagged_message.content:
                        await message.delete(delay=1)
                        count += 1
                else:
                    await message.delete(delay=1)
                    count += 1

        await ctx.send(f"Deleted {count} messages")


    @ascii.error
    async def info_error(self, ctx, error):
        if "message" in dir(error.original):
            await ctx.send(error.original.message)
        else:
            logging.info(error)
            await ctx.send("An error has occured. Sorry can't be less secure. ask the developer.")


