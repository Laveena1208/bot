from pickle import FALSE
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
# from discord import FFmpegPCMAudio

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        # all the music related stuff
        self.is_playing = False

        # 2D array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': "bestaudio"}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc=""
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item)["entries"] [0]
            except Exception:
                return False

            return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0] [0] ['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            # vc = await channel.connect()
            self.vc.play(discord.FFmpegPCMAudio(executable="C:/path/ffmpeg.exe", source="mp3.mp3"))
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0] [0] ['source']

            # try to connect the voice channel if you are not already connected
            if self.vc == "" or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                self.vc = await self.client.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # remove the first element as you are currently playing it

            self.music_queue.pop(0)
            print(self.music_queue.pop(0))

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    @commands.command()
    async def p(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # you need to be connected so the bot knows where to go
            await ctx.send("connect to a voice channel")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("could not download the song.")
            else:
                await ctx.send("song added to the queue")
                self.music_queue.append([song,voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            #try to play next in the queue if it exist
            await self.play_music()






    # def setup(client):
    # client.add_cog(music(client))




#     @commands.command()
#     async def join(self, ctx):
#         if ctx.author.voice is None:
#             await ctx.send("You're not in Voice Channel!")
#         voice_channel = ctx.author.voice.channel
#         if ctx.voice_client is None:
#             await voice_channel.connect()
#         else:
#             await ctx.voice_client.move_to(voice_channel)

#     @commands.command()
#     async def disconnect(self, ctx):
#         await ctx.voice_client.disconnect()

#     @commands.command()
#     async def play(self,ctx,url):
#         ctx.voice_client.stop()
#         FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#         YDL_OPTIONS = {'format': "bestaudio"}
#         vc = ctx.voice_client

#         with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
#             info = ydl.extract_info(url, download=False)
#             url2 = info['formats'][0] ['url']
#             source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
#             vc.play(source)

#     @commands.command()
#     async def pause(self,ctx):
#         await ctx.voice_client.pause()
#         await ctx.send("paused")

#     @commands.command()
#     async def resume(self,ctx):
#         await ctx.voice_client.resume()
#         await ctx.send("resumed")



