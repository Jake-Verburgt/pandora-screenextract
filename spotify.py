import requests
from time import sleep
from urllib.parse import urlencode
import base64
import webbrowser


def get_token(client_id, client_secret, 
              scope = "user-library-modify user-read-private user-library-read",
              redirect_uri="http://localhost:7777/callback/"):
    
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }

    # response = requests.post("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    # print(response.text)
    # exit()

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    code = input("Enter the URL you were directed to: ")
    code = code.partition("code=")[-1]

    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"}

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:7777/callback/"}

    response = requests.post("https://accounts.spotify.com/api/token", 
                            data=token_data, headers=token_headers)
    token = response.json()["access_token"]
    return token



def search_song(song_name, artist, token):
    sleep(0.1) #Don't spam their api, wait a bit

    string = f"{song_name} {artist}"
    response = requests.get("https://api.spotify.com/v1/search", 
                           headers={"Authorization": f"Bearer {token}"},
                           params = {"q":string, "type":"track"})
    if response.ok:
        try:
            top_hit = response.json()["tracks"]["items"][0]
            return top_hit
        except(KeyError, IndexError):
            return None #Sometimes shit don't work
    else:
        raise Exception("Spotify API returned Bad Response! ")


def add_to_liked_songs(song_id:str, token:str):
    response = requests.put("https://api.spotify.com/v1/me/tracks/",
                             headers={"Authorization": f"Bearer {token}"}, 
                             params={"ids":song_id}
                            )
    if response.ok:
        return
    else:
        raise Exception(response.text)

