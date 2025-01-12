import requests
import base64
import spotify_secrets


def get_access_token() -> str:
    secret_str = spotify_secrets.SPOTIFY_CLIENT_ID + \
        ":" + spotify_secrets.SPOTIFY_CLIENT_SECRET
    b64_secret = str(base64.b64encode(secret_str.encode("utf-8")), "utf-8")

    header = {
        "Authorization": "Basic " + b64_secret,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {"grant_type": "client_credentials"}
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url=url, headers=header, data=body)
    data = response.json()
    return data['access_token']


def get_playlists(access_token: str) -> dict:
    header = {"Authorization": "Bearer " + access_token}
    user_id = spotify_secrets.user_id
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url=url, headers=header)
    return response.json()


def find_world_playlist(data: dict) -> dict:
    for item in data["items"]:
        if item["name"] == "2025 around the world":
            playlist = item
    return playlist


def get_tracks_from_playlist(playlist: dict, access_token: str):
    play_id = playlist["id"]
    header = {"Authorization": "Bearer " + access_token}
    url = f"https://api.spotify.com/v1/playlists/{play_id}/tracks"
    filters = {
        "fields": "items(!is_local, !added_by, track(name,external_ids,id,uri))"
    }
    response = requests.get(url=url, headers=header, params=filters)
    data = response.json()
    return data["items"]


def parse_country_codes_from_track(tracks: list[dict], show: bool = False) -> list[str]:
    id_list = []
    for item in tracks:
        track = item["track"]
        name = track["name"]
        if "external_ids" not in track.keys():
            continue
        if "isrc" not in track["external_ids"].keys():
            continue
        country_code = track["external_ids"]["isrc"][0:2]
        id_list.append(country_code)
        if show:
            print(name + "\t" + country_code)

    return id_list
