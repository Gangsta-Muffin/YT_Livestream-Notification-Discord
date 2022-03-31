<h1>Youtube - Discord notifications</h1>

The Youtube Livestream notification is a notification system built to announce YouTube Livestreams (of the youtuber of your choice) to your Discord server! The original idea behind this code was to create a system for Zen World's music feedback streams in which a channel opens up (for people to send their music links in) whenever Zen World goes live (and then closes when he stops the stream). 

NOTE: Channel open and closing mechanism not included in this code!


<h3>Installation</h2>

For this code, you will need to follow the following installation steps:

1.  You will first need to install <a href="https://www.python.org/downloads/">Python</a>
2.  Next you will need to install Nextcord. To do this run the following command in your terminal: `pip install nextcord`
3.  Lastly, you will need to install the Youtube Api library (<a href="https://github.com/googleapis/google-api-python-client">view docs</a>). To do this, run the following command in your terminal: `pip install google-api-python-client`


Now you have installed all necessary libraries and software, it will be necessary for you to create your own discord bot account, as well as getting your own api key to request data from Youtube:

- Create a discord bot account <a href="https://discord.com/developers/docs/intro">here</a>
- Get your own Youtube API key <a href="https://console.cloud.google.com/apis/dashboard">here</a>

<h3>NOTICE</h3>
This version of the code is set up to be available for all users. Due to YouTube Data API's limitations, you can only request this data (`search()` live.py; line 48) 100 times per day (1 request = 100 units, quote = 10.000 units/day). If you wish to recieve a higher quote, you can contact YouTube Data API <a href="https://support.google.com/youtube/contact/yt_api_form">here</a>. Please note that applying for a higher quote doesn't guarantee that you will recieve it!


<h2>Setup</h2>

To set the code up properly, you will need to retrieve the id for your discord announcement channel. To do so, make sure you have `Developer Mode` enabled within the `Advanced` category in the discord user settings. From here on out you can right click any channel or guild and select `Copy ID` to get the id of that object. 


from here on out you are ready to paste the channel ID into the code (live.py file):
  ```python
    @property
    def announce_channel(self):
        return self.bot.get_channel("ANNOUNCEMENT CHANNEL ID HERE")
```
  
simply replace the string with the integer of the given value.

for example:
```python
    @property
    def channel(self):
        return self.bot.get_channel(2938708375455738419)
```
  
  Next, you will need to add your YouTube Data API key to the file aswell as define the Youtuber ID you wish the bot to follow:
```python
    self._key = "GASJE456EW45S-FDAS4"
    
    
    
    @property
    def is_live(self):
        request = self.yt.search().list(
            part="snippet",
            eventType = "live",
            type = "video",
            channelId = "FD4A45E"
        )

        response = request.execute()
        is_live = response['pageInfo']['totalResults']
        
        try:
            vid_id = response['items'][0]['id']['videoId']

        except:
            vid_id = 0
        
        return [is_live, vid_id]
    
```

Now you are just about finished. The last thing you need to do is input the bot token in the main.py file:
```python
bot.run("GJK4FA565SD54E6.FDA445A-FD7891")
```


<h2>Usage</h2>
Given the bot's simplicity, there is not much need for command implementation. Once you have followed the Stept provided in the Setup section, the bot is all ready to go. Just run the main.py file and the bot will be up and will begin checking for Livestreams! (beware that server implementation is not included in this code)



<h2>Results</h2>


![](https://user-images.githubusercontent.com/94480512/161152438-a5709424-47ce-4bb4-8595-ed647ed19811.png)
