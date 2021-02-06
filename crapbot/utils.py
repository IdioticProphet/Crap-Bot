import asyncio, tempfile, subprocess, filetype, random, sys, logging, requests, math, io, time, discord, os, yaml
import numpy as np
from .config import Config
from .exceptions import *
from PIL import Image    

def return_sound_maps():
    sound_file_dir = os.path.join(Config.BOT_DIRECTORY, "sound_commands.yaml")
    if not os.path.exists(sound_file_dir):
        open(sound_file_dir, "a").close()
    data = yaml.safe_load(open(sound_file_dir, "r"))
    if not data:
        return {}
    return data

def return_sound_player(filepath):
    logging.debug(filepath)
    sound_file=filepath
    logging.info(sound_file)
    if os.path.exists(sound_file):
        return discord.FFmpegPCMAudio(sound_file)
    else:
        raise FileNotFoundError

async def play_sound(voice_channel, source, bot_member):
    logging.debug(source)
    vc_client = await voice_channel.connect()
    if bot_member.voice.mute:
        await bot_member.edit(mute=False)
    vc_client.play(source)
    while vc_client.is_playing():
        await asyncio.sleep(1)
        if bot_member.voice.mute:
            await bot_member.edit(mute=False)
    vc_client.stop()
    await vc_client.disconnect()

def save_sound(link, file_name):
    """
    given a link, save the file in the static bot sounds
    """
    resp = requests.get(link)
    if not filetype.is_audio(resp.content):
        raise NotAudioException
    file_ext = filetype.guess(resp.content).extension
    logging.debug(file_ext)
    with tempfile.NamedTemporaryFile(suffix="."+file_ext) as tmpfile:
        tmpfile.write(resp.content)
        cmd = subprocess.Popen(f"ffmpeg -i {tmpfile.name} {os.path.join(Config.BOT_SOUND_DIR, file_name)}", shell=True)
        cmd.communicate()
        tmpfile.close()
    # Update the sound definitions
    current_dict = return_sound_maps()
    current_dict[file_name.split(".m4a")[0]] = file_name
    with open(os.path.join(Config.BOT_DIRECTORY, "sound_commands.yaml"), "w") as f:
        f.write(yaml.dump(current_dict))
        f.close()

def delete_sound(soundname):
    sound_maps = return_sound_maps()
    if soundname not in sound_maps.keys():
        raise SoundNotFound("That sound does not exist!")
    os.remove(os.path.join(Config.BOT_SOUND_DIR, soundname+".m4a"))
    sound_maps.pop(soundname)
    with open(os.path.join(Config.BOT_DIRECTORY, "sound_commands.yaml"), "w") as f:
        f.write(yaml.dump(sound_maps))
        f.close()
    
def help_msg(msg) -> str:
    return f"```\n{msg}\n```"

def create_debug_message(string) -> str:
    return f"[{time.time()}] {string}"

def exist_category(guild, category_name) -> bool:
    if discord.utils.get(guild.categories, name=category_name):
        return True
    return False

def exist_channel(guild, channel_name) -> bool:
    if discord.utils.get(guild.text_channels, name=channel_name):
        return True
    return False

class Asciiifier:
    def __init__(self, imgbytes, detail, cols, scale):
        imgFile = imgbytes
        
        logging.debug('generating ASCII art...')
        # convert image to ascii txt
        aimg = self.covertImageToAscii(imgFile, cols, scale, detail)
        self.ascii_art = "```\n"+"\n".join(aimg)+"```"

    def getAverageL(self, image):
        """
        Given PIL Image, return average value of grayscale value
        """
        im = np.array(image)
        w,h = im.shape
        return np.average(im.reshape(w*h))

    def covertImageToAscii(self, fileName, cols, scale, moreLevels):
        """
        Given Image and dims (rows, cols) returns an m*n list of Images 
        """
        gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^'. "
        gscale2 = '@%#*+=-:. '
        image = Image.open(io.BufferedReader(fileName)).convert('L')
        W, H = image.size[0], image.size[1]
        logging.debug("input image dims: %d x %d" % (W, H))
        w = W/cols
        h = w/scale
        rows = int(H/h)
        
        logging.debug("cols: %d, rows: %d" % (cols, rows))
        logging.debug("tile dims: %d x %d" % (w, h))
        # Too small
        if cols > W or rows > H:
            return("Image too small for specified cols!")

        aimg = []
        
        for j in range(rows):
            y1 = int(j*h)
            y2 = int((j+1)*h)
            if j == rows-1:
                y2 = H
            aimg.append("")
            for i in range(cols):
                x1 = int(i*w)
                x2 = int((i+1)*w)
                if i == cols-1:
                    x2 = W
                img = image.crop((x1, y1, x2, y2))
                avg = int(self.getAverageL(img))
                if moreLevels:
                    gsval = gscale1[int((avg*69)/255)]
                else:
                    gsval = gscale2[int((avg*9)/255)]
                aimg[j] += gsval

        return aimg

def owoifier(owo):
    substitution = {"r":"w",
    "l":"w",
    "R":"W",
    "L":"W",
    "no":"nu",
    "has":"haz",
    "have":"haz",
    "you":"uu",
    "the":"da",
    "R":"W",
    "The":"Da" }
    #Prefixes
    prefix = ["<3 ",
    "H-hewwo?? ",
    "HIIII! ",
    "Haiiii! ",
    "Huohhhh. ",
    "OWO ",
    "OwO ",
    "UwU ",
    "88w88",
    "H-h-hi",]
    #Suffixes
    suffix = [" :3",
    " UwU",
    " ʕʘ‿ʘʔ",
    " >_>",
    " ^_^",
    "..",
    " Huoh.",
    " ^-^",
    " ;_;",
    " xD",
    " x3",
    " :D",
    " :P",
    " ;3",
    " XDDD",
    ", fwendo",
    " ㅇㅅㅇ",
    " (人◕ω◕)",
    " （＾ｖ＾）",
    " Sigh.",
    " ._.",
    " >_<"
    "xD xD xD",
    ":D :D :D",]
    for word, initial in substitution.items():
        owo = owo.replace(word.lower(), initial)
    output = random.choice(prefix) + owo + random.choice(suffix)
    return(output)

def is_valid_link(string):
    import re
    regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, string) is not None:
        return True
    return False

def derp(string, n=False):
    string = string.lower()
    ret = []
    if " " in string:
        string = string.split(" ")
        for split in string:
            ret.append(derp(split))
    else:
        for letter in string:
            if not n:
                n = not n
                ret.append(letter.lower())
            elif n:
                n = not n
                ret.append(letter.upper())
        return "".join(ret)
    return " ".join(ret)
