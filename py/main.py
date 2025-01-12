import spotify_api as sp


def main():
    access_token = sp.get_access_token()
    data = sp.get_playlists(access_token)
    playlist = sp.find_world_playlist(data)
    tracks = sp.get_tracks_from_playlist(playlist, access_token)
    # for track in tracks:
    #     print(track["track"]["name"])


if __name__ == "__main__":
    main()
