from imp import lock_held
from discord import TextChannel
from nextcord.ext import commands, tasks
from nextcord import Embed, Guild, PermissionOverwrite, utils
from googleapiclient.discovery import build
from checks.check_staff import check_staff


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._key = "API KEY HERE"
        self.yt = build("youtube", "v3", developerKey=self.key)

        self.keep_close = False
        self.live = True

        self.check_live.start()


    @property
    def key(self):
        return self._key

    @property
    def channel(self):
        return self.bot.get_channel("CHANNEL ID HERE")

    @property
    def announce_channel(self):
        return self.bot.get_channel("ANNOUNCEMENT CHANNEL ID HERE")
    
    @property
    def guild(self):
        return self.bot.get_guild("GUILD ID HERE")

    @property
    def role_id(self):
        return "ROLE ID HERE"

    @property
    def channel_state(self):
        role = utils.get(self.guild.roles, id=self.role_id)
        return self.channel.overwrites_for(role).send_messages

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
        await self.announce_channel.send(f"A new stream has started! {link}")


    async def edit_perm(self):
        role = utils.get(self.guild.roles, id=self.role_id)

        perm = self.channel.overwrites_for(role).send_messages

        if perm:
            await self.channel.set_permissions(role, send_messages=False)

        else:
            await self.channel.set_permissions(role, send_messages=True)

    @tasks.loop(seconds=5)
    async def check_live(self):
        live_state = self.is_live
        is_live = live_state[0]
        live_link = live_state[1]

        channel_state = self.channel_state
        force_lock = self.keep_close

        if is_live and not channel_state and not force_lock:
            await self.edit_perm()
            await self.send_message(f"https://www.youtube.com/watch?v={live_link}")

        elif not is_live and channel_state:
            await self.edit_perm()
            
        elif not is_live and not channel_state and force_lock:
            self.keep_close = False


    @check_live.before_loop
    async def before_live(self):
        await self.bot.wait_until_ready()


    @commands.command(name="lock")
    @commands.check(check_staff)
    async def lock_channel(self, ctx, arg_channel: TextChannel):
        role = utils.get(self.guild.roles, id=self.role_id)

        if arg_channel.id != self.channel.id:
            await arg_channel.set_permissions(role, send_messages = False)

        else:
            self.keep_close = True
            await self.channel.set_permissions(role, send_messages=False)

    
    @commands.command(name="unlock")
    @commands.check(check_staff)
    async def unlock_channel(self, ctx, arg_channel: TextChannel):
        role = utils.get(self.guild.roles, id=self.role_id)
        
        if arg_channel.id != self.channel.id:
            await arg_channel.set_permissions(role, send_messages = True)

        else:
            self.keep_close = False

            await self.channel.set_permissions(role, send_messages=True)




def setup(bot):
    bot.add_cog(Live(bot))
