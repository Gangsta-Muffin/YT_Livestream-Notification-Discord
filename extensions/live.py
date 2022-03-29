from imp import lock_held
from discord import TextChannel
from nextcord.ext import commands, tasks
from nextcord import Embed, Guild, PermissionOverwrite, utils
from googleapiclient.discovery import build
from checks.check_staff import check_staff


class Live(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._key = "AIzaSyAhV0rPsAaI7NK3SbWXseah7_c2kqz0InM"
        self.yt = build("youtube", "v3", developerKey=self.key)

        self.keep_close = False
        self.live = True

        self.check_live.start()


    @property
    def key(self):
        return self._key

    @property
    def channel(self):
        return self.bot.get_channel(913507302651330581)
    
    @property
    def guild(self):
        return self.bot.get_guild(852600631994220585)

    @property
    def role_id(self):
        return 915330052495933471

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
            # channelId = "UCSJ4gkVC6NrvII8umztf0Ow"
            channelId = "UCa10nxShhzNrCE1o2ZOPztg"
            # channelId="UCNRD06rR7bR0Xwd-7gAKDEA"
        )

        response = request.execute()
        is_live = response['pageInfo']['totalResults']

        return is_live

    async def stop_force(self):
        self.keep_close = False


    async def send_message(self, message):
        send_message = Embed(title="New Embed", description=message)

        await self.channel.send(embed=send_message)


    async def edit_perm(self):
        role = utils.get(self.guild.roles, id=self.role_id)

        perm = self.channel.overwrites_for(role).send_messages

        if perm:
            await self.channel.set_permissions(role, send_messages=False)

        else:
            await self.channel.set_permissions(role, send_messages=True)

    @tasks.loop(seconds=5)
    async def check_live(self):
        live = self.live
        # live = self.is_live
        channel_state = self.channel_state
        force_lock = self.keep_close

        if live and not channel_state and not force_lock:
            await self.edit_perm()
            print(f"Keep locked was is set to {force_lock}")

        elif not live and channel_state:
            await self.edit_perm()
            
        elif not live and not channel_state and force_lock:
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


    @commands.command(name="live")
    async def set_live(self, ctx):
        if self.live:
            self.live = False

        else:
            self.live = True




def setup(bot):
    bot.add_cog(Live(bot))
