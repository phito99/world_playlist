import spotify_api as sp
import world_plot as wp


def main():
    access_token = sp.get_access_token()
    data = sp.get_playlists(access_token)
    playlist = sp.find_world_playlist(data)
    tracks = sp.get_tracks_from_playlist(playlist, access_token)
    country_codes = sp.parse_country_codes_from_track(tracks)
    country_codes = wp.convert_alpha2_to_alpha3(country_codes)
    data = wp.group_country_code_list(country_codes=country_codes)
    wp.generate_map(data)


if __name__ == "__main__":
    main()
