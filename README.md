# Youtube To Spotify Automator
Python script that takes a playlist from youtube and converts it to a spotify playlist without using youtube_dl

Time: 8/17/2020, One Day Project

## Sites
* [Google Dev API]
* [Youtube Data API v3]
* [Spotify Web API]
* [Requests Library v 2.22.0]

## How to use:

1) Install all dependencies 
`pip3 install -r requirements.txt`
2) Get Spotify User ID (Profile>Account>Username), the Oauth Token from Spotify (click on "get Token" at [Spotify Oauth Token]) and your desired playlist's iD (google "find playlist id youtube") and add it to secrets.py file
3) Create a project in Google APIs, enable Youtube Data API v3 and create Oauth 2.0 client ID and download the Oauth json file (rename it client_secret.json)
4) Run program
`python3 create_playlist.py`
5) Copy and paste the google authentication site to web browser
6) Get auth key and paste it back into program
7) Check out your favorite youtube songs now in your spotify :)


   [Google Dev API]: <https://console.developers.google.com/apis>
   [Youtube Data API v3]: <https://developers.google.com/youtube/v3>
   [Spotify Web API]: <https://developer.spotify.com/documentation/web-api/>
   [Requests Library v 2.22.0]: <https://requests.readthedocs.io/en/master/>
   [Spotify Oauth Token]: <https://developer.spotify.com/console/post-playlists/>
   
## Credit:
Inspiration and some code from https://github.com/TheComeUpCode/SpotifyGeneratePlaylist
