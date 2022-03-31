from nextcord import TextChannel
from nextcord.ext import commands, tasks
from nextcord import Embed, Guild, PermissionOverwrite, utils
from googleapiclient.discovery import build
from checks.check_staff import check_staff


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notified = False
        self.check_live.start()
        
        self._key = "API KEY HERE"
        self.yt = build("youtube", "v3", developerKey=self.key)

       
    @property
    def key(self):
        return self._key

    @property
    def announce_channel(self):
        return self.bot.get_channel("ANNOUNCEMENT CHANNEL ID HERE")

    @property
    def is_live(self):
        request = self.yt.search().list(
            part="snippet",
            eventType = "live",
            type = "video",
            channelId = "YOUTUBE CHANNEL ID HERE"
        )

        response = request.execute()
        is_live = response['pageInfo']['totalResults']
        
        try:
            vid_id = response['items'][0]['id']['videoId']

        except:
            vid_id = 0
        
        return [is_live, vid_id]


    async def send_message(self, link):
        await self.announce_channel.send(f"@everyone A new stream has started! {link}")

        
    @tasks.loop(minutes=15)
    async def check_live(self):
        live_state = self.is_live
        is_live = live_state[0]
        live_link = live_state[1]

        sent_link = self.notified
        
        if is_live and not sent_link:
            await self.send_message(f"https://www.youtube.com/watch?v={live_link}")
            self.notified = True
            
        elif not is_live and sent_link:
            self.notified = False


    @check_live.before_loop
    async def before_live(self):
        await self.bot.wait_until_ready()
       
        

def setup(bot):
    bot.add_cog(Live(bot))
