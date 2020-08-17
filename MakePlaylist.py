"""
Step 1: Log Into Youtube
    https://console.developers.google.com/apis/credentials?project=project1-286715
    Set up Google Project and Youtube API; make API Key and OAuth 2.0 Client IDs + download json file
    (Follow this https://developers.google.com/youtube/v3/quickstart/python?hl=en_US)
    Then Copy Pasta https://developers.google.com/youtube/v3/docs/channels/list?apix=true
Step 2: Get Liked Videos
Step 3: Create a New Playlist in Spotify
https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/
    https://developer.spotify.com/console/post-playlists/
    ->Renew OAuth Token if not working
Step 4: Search for song in Spotify
https://developer.spotify.com/documentation/web-api/reference/search/search/
    https://developer.spotify.com/console/get-search-item/?q=tania+bowra&type=artist
Optional: Sort Songs?
Step 5: Add song to spotify playlist
"""
import json
import requests
import os
import re

from secrets import spotify_token, spotify_user_id, youtube_playlist_id
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class CreatePlaylist:

    def __init__(self):
        # self.user_id = spotify_user_id
        # self.spotify_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info= {}
    # Step 1: Log Into Youtube
    def get_youtube_client(self):
        # Copied from https://developers.google.com/youtube/v3/docs/channels/list?apix=true
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Step 2: Get Liked Videos
    def get_liked_videos(self):
        # request = self.youtube_client.videos().list(
        #     part="snippet,contentDetails,statistics",
        #     myRating="like"
        # )
        request = self.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId=youtube_playlist_id
        )
        response = request.execute()

        # collect each video and get info
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["snippet"]["resourceId"]["videoId"])

            #use youtube_DL library to collect song name and artist name... youtube_DL Library sucks. nvm
            # video = youtube_dl.YoutubeDL({}).extract_info(
            #     youtube_url, download=False)
            #song_name = video["title"]


            # Need to find a way to make it easy to search the video title bc it contains artist ANd song

            # This only works with youtube titles of ARTIST - TITLE ( BLEH BLEH)
            temp = re.split(r"[-,(]", video_title)
            artist = temp[0]
            song_name = temp[1]
            #print(artist, song_name)
            if artist is not None and song_name is not None:
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # add the uri, easy to get song to put into playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
                }

    # Step 3: Create a New Playlist in Spotify
    def create_playlist(self):
        # jason.dumps() converts Python object into a json string
        request_body = json.dumps({
            "name": "Project Playlist",
            "description": "proj 1",
            "public": True
        })
        # endpoint is https://api.spotify.com/v1/users/{user_id}/playlists
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        # Notes: seems like .format(X) puts X into the {}
        # response_json = response.json()

        # playlist id
        return response.json()["id"]

    # Step 4: Search for song in Spotify
    def get_spotify_uri(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?q={}&type=track".format(
            song_name
            #artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song?
        uri = songs[0]["uri"]
        return uri

    # Step 5: Add song to spotify playlist
    def add_song_to_playlist(self):
        # Step 5.1: populate our song's dictionary
        self.get_liked_videos()

        # Step 5.2: collect all uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        # Step 5.3: create playlist
        playlist_id = self.create_playlist()

        # Step 5.3: move into playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        return response_json

# makes it executable
if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()

