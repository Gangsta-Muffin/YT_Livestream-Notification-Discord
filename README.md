<h1>Youtube - Discord notifications</h1>

The Youtube Livestream notification is a notification system built to announce YouTube Livestreams (of the youtuber of your choice) to your Discord server! The original idea behind this code was to create a system for Zen World's music feedback streams. As it stands today, he uses a discord channel as a "feedback request" channel. The main issue within the server was, that people would send their music in (for feedback) before the stream started. This was supposed to fix that issue


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

To set the code up properly, you will need to retrieve the id for your discord announcement channel. To do so, make sure you have `Developer Mode` enabled within the `Advanced` category in the settings. From here on out you can right click any channel or guild and select `Copy ID` to get the id of that object. 
