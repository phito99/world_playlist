import spotify_secrets
import requests
import base64


def get_access_token():
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


def get_playlists(access_token):
    header = {"Authorization": "Bearer " + access_token}
    user_id = spotify_secrets.user_id
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url=url, headers=header)
    return response.json()


def find_world_playlist(data):
    for item in data["items"]:
        if item["name"] == "2025 around the world":
            playlist = item
    return playlist


def main():
    access_token = get_access_token()
    data = get_playlists(access_token)
    playlist = find_world_playlist(data)
    print(playlist)


if __name__ == "__main__":
    main()
