from .utils import *
from .exceptions import *
from .config import Config
import tempfile, os, re


class SoundHelpers:
    async def sound_play(ctx, *args):
        """
        When arriving at this function, args should be length of 1
        The argument should also be the soundname.
        """
        sound_maps=return_sound_maps()
        if args[0] not in sound_maps.keys():
            raise SoundNotFound("Sound Doesnt Exist.")
        try:
            voice_channel = ctx.message.author.voice.channel
        except AttributeError as e:
            if "'NoneType' object has no attribute 'channel'" in repr(e):
                raise NotInVoice("You are not in a voice channel.")
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        try:
            source = return_sound_player(os.path.join(Config.BOT_SOUND_DIR, sound_maps[args[0]]))
        except FileNotFoundError:
            raise SoundNotFound("Couldn't find sound file... This shouldn't happen!")
        await play_sound(voice_channel, source, bot_member)
        return
        
    async def sound_list(ctx, *args):
        """
        Lists the sounds that are listed in the config.
        """
        sound_maps = return_sound_maps()
        if not sound_maps.keys():
            await ctx.send("I dont know any sounds yet! Teach me.")
            return
        await ctx.send(f'Sounds that I Know:\n{", ".join(sound_maps.keys())}')
        return
    
    async def sound_add(ctx, *args):
        # TODO: Add support for youtube links
        sound_maps = return_sound_maps()
        if args[0] in sound_maps.keys():
            raise ExistsError("Sound Already Exists!")
        sound_name = args[0]
        sound_link = args[1]
        if not is_valid_link(sound_link):
            logging.debug(sound_link)
            raise InvalidLink("The Link you provided was not correct.")
        if not sound_name.isalnum():
            logging.debug(sound_name)
            raise InvaildName("The name you gave was not Alpha Numeric.")
        sound_name += ".m4a"
        logging.info("saving sound")
        save_sound(sound_link, sound_name)
        await ctx.send("Sound was saved successfully!")

    async def sound_tts(ctx, *args):
        """
        Queries and makes the TTS message, then plays it.
        """
        try:
            voice_channel = ctx.message.author.voice.channel
        except AttributeError as e:
            if "'NoneType' object has no attribute 'channel'" in repr(e):
                raise NotInVoice("You are not in a voice channel.")
        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        tts_message = args[-1].replace("\n", " ").strip('')
        voice_person = "Brian"
        link = f"https://api.streamelements.com/kappa/v2/speech?voice={voice_person}&text="+tts_message
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmpfile:
            resp = requests.get(link)
            tmpfile.write(resp.content)
            source = return_sound_player(tmpfile.name)
            await play_sound(voice_channel, source, bot_member)
            tmpfile.close()
            
    async def sound_remove(ctx, *args):
        """
        Removes sound from list, 
        """
        if args[0] not in return_sound_maps().keys():
            raise SoundNotFound("That sound does not exist!")
        try:
            delete_sound(args[0])
        except:
            raise
        await ctx.send("Sound Was Deleted Successfully.")
        

        
